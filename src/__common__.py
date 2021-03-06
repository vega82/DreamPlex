# -*- coding: utf-8 -*-
'''
DreamPlex Plugin by DonDavici, 2012
 
https://github.com/DonDavici/DreamPlex

Some of the code is from other plugins:
all credits to the coders :-)

DreamPlex Plugin is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

DreamPlex Plugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
'''
#===============================================================================
# IMPORT
#===============================================================================
import sys
import os
import datetime

from enigma import getDesktop, addFont
from skin import loadSkin
from Components.config import config

from DPH_Singleton import Singleton

#===============================================================================
# GLOBAL
#===============================================================================
gConnectivity = None
gLogFile = None

# ****************************** VERBOSITY Level *******************************
VERB_ERROR       = 0  # "E" shows error
VERB_INFORMATION = 0  # "I" shows important highlights to have better overview if something really happening or not

VERB_WARNING     = 1  # "W" shows warning

VERB_DEBUG 		 = 2  # "D" shows additional debug information

VERB_STARTING    = 3  # "S" shows started functions/classes etc.
VERB_CLOSING     = 3  # "C" shows closing functions/classes etc.

VERB_EXTENDED	 = 4  # "X" shows information that are not really needed at all can only be activated by hand

STARTING_MESSAGE = "ENTERING"
CLOSING_MESSAGE = "LEAVING"

#===============================================================================
# 
#===============================================================================
def printl2 (string, parent=None, dmode= "U"):
	'''
	ConfigSelection(default="0", choices = [("0", _("Silent")),("1", _("Normal")),("2", _("High")),("3", _("All"))])
	
	@param string: 
	@param parent:
	@param dmode: default = "U" undefined 
							"E" shows error
							"W" shows warning
							"I" shows important information to have better overview if something really happening or not
							"D" shows additional debug information for better debugging
							"S" shows started functions/classes etc.
							"C" shows closing functions/classes etc.
	@return: none
	'''

	debugMode = int(config.plugins.dreamplex.debugMode.value)
	
	
	#TODO change before making new version
	#debugMode = 2 
	
	out = ""
	
	if parent is None:
		out = str(string)
	else:
		classname = str(parent.__class__).rsplit(".", 1)
		if len(classname) == 2:
			classname = classname[1]
			classname = classname.rstrip("\'>")
			classname += "::"
			out = str(classname) + str(sys._getframe(1).f_code.co_name) +" -> " + str(string)
		else:
			classname = ""
			out = str(parent) + " -> " + str(string)

	if dmode == "E" :
		verbLevel = VERB_ERROR
		if verbLevel <= debugMode:
			print "[DreamPlex] " + "E" + "  " + str(out)
			writeToLog(dmode, out)
	
	elif dmode == "W":
		verbLevel = VERB_WARNING
		if verbLevel <= debugMode:
			print "[DreamPlex] " + "W" + "  " + str(out)
			writeToLog(dmode, out)
	
	elif dmode == "I":
		verbLevel = VERB_INFORMATION
		if verbLevel <= debugMode:
			print "[DreamPlex] " + "I" + "  " + str(out)
			writeToLog(dmode, out)
	
	elif dmode == "D":
		verbLevel = VERB_DEBUG
		if verbLevel <= debugMode:
			print "[DreamPlex] " + "D" + "  " + str(out)	
			writeToLog(dmode, out)
	
	elif dmode == "S":
		verbLevel = VERB_STARTING
		if verbLevel <= debugMode:
			print "[DreamPlex] " + "S" + "  " + str(out) + STARTING_MESSAGE
			writeToLog(dmode, out)
	
	elif dmode == "C":
		verbLevel = VERB_CLOSING
		if verbLevel <= debugMode:
			print "[DreamPlex] " + "C" + "  " + str(out) +  CLOSING_MESSAGE
			writeToLog(dmode, out)
	
	elif dmode == "U":
		print "[DreamPlex] " + "U  specify me!!!!!" + "  " + str(out)
		writeToLog(dmode, out)
		
	elif dmode == "X":
		verbLevel = VERB_EXTENDED
		if verbLevel <= debugMode:
			print "[DreamPlex] " + "D" + "  " + str(out)	
			writeToLog(dmode, out)
		
	else:
		print "[DreamPlex] " + "OLD CHARACTER CHANGE ME !!!!!" + "  " + str(out)
	


#===============================================================================
# 
#===============================================================================
def writeToLog(dmode, out):
	'''
	singleton handler for the log file
	
	@param dmode: E, W, S, H, A, C, I
	@param out: message string
	@return: none
	'''
	try:
		#=======================================================================
		# if gLogFile is None:
		#	openLogFile()
		#=======================================================================
		instance = Singleton()
		if instance.getLogFileInstance() is "":
			openLogFile()
			gLogFile = instance.getLogFileInstance()
			gLogFile.truncate()
		else:
			gLogFile = instance.getLogFileInstance()
			
		now = datetime.datetime.now()
		gLogFile.write("%02d:%02d:%02d.%07d " % (now.hour, now.minute, now.second, now.microsecond) + " >>> " + str(dmode) + " <<<  " + str(out) + "\n")
		gLogFile.flush()
	
	except Exception, ex:
		printl2("Exception(" + str(type(ex)) + "): " + str(ex), "__common__::writeToLog", "E")


#===============================================================================
# 
#===============================================================================
def openLogFile():
	'''
	singleton instance for logfile
	
	@param: none
	@return: none
	'''
	#printl2("", "openLogFile", "S")
	
	logDir = config.plugins.dreamplex.logfolderpath.value
	
	now = datetime.datetime.now()
	try:
		instance = Singleton()
		instance.getLogFileInstance(open(logDir + "dreamplex.log", "w"))
		
	except Exception, ex:
		printl2("Exception(" + str(type(ex)) + "): " + str(ex), "openLogFile", "E")
	
	#printl2("", "openLogFile", "C")

#===============================================================================
# 
#===============================================================================
def testInetConnectivity(target = "http://www.google.com"):
	'''
	test if we get an answer from the specified url
	
	@param url:
	@return: bool
	'''
	printl2("", "__common__::testInetConnectivity", "S")
	
	import urllib2
	from   sys import version_info
	import socket
	
	try:
		opener = urllib2.build_opener()
		page = None
		if version_info[1] >= 6:
			page = opener.open(target, timeout=2)
		else:
			socket.setdefaulttimeout(2)
			page = opener.open(target)
		if page is not None:
			
			printl2("","__common__::testInetConnectivity", "C")
			return True
		else:
			
			printl2("","__common__::testInetConnectivity", "C")
			return False
	except:
		
		printl2("", "__common__::testInetConnectivity", "C")
		return False

#===============================================================================
# 
#===============================================================================
def testPlexConnectivity(ip, port):
	'''
	test if the plex server is online on the specified port
	
	@param ip: e.g. 192.168.0.1
	@param port: e.g. 32400
	@return: bool
	'''
	printl2("", "__common__::testPlexConnectivity", "S")
	
	import socket
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	printl2("IP => " + str(ip), "__common__::testPlexConnectivity", "I")
	printl2("PORT => " + str(port), "__common__::testPlexConnectivity","I")
	
	try:
		sock.connect((ip, port))
		sock.close()
		
		printl2("", "__common__::testPlexConnectivity", "C")
		return True
	except socket.error, e:
		printl2("Strange error creating socket: %s" % e, "__common__::testPlexConnectivity", "E")
		sock.close()
		
		printl2("", "__common__::testPlexConnectivity", "C")
		return False


#===============================================================================
# 
#===============================================================================	
def registerPlexFonts():
	'''
	registers fonts for skins
	
	@param: none 
	@return none
	'''
	printl2("", "__common__::registerPlexFonts", "S")
	
	printl2("adding fonts", "registerPlexFonts", "I")

	addFont("/usr/lib/enigma2/python/Plugins/Extensions/DreamPlex/skins/mayatypeuitvg.ttf", "Modern", 100, False)
	printl2("added => mayatypeuitvg.ttf", "registerPlexFonts", "I")
	
	addFont("/usr/lib/enigma2/python/Plugins/Extensions/DreamPlex/skins/goodtime.ttf", "Named", 100, False)
	printl2("added => goodtime.ttf", "registerPlexFonts", "I")
	
	printl2("", "__common__::registerPlexFonts", "C")

#===============================================================================
# 
#===============================================================================
def loadPlexSkin():
	'''
	loads depending on the desktop size the corresponding skin.xml file
	
	@param: none 
	@return none
	'''
	printl2("", "__common__::loadPlexSkin", "S")
	
	skin = None
	desktop = getDesktop(0).size().width()
	if desktop == 720:
		skin = "/usr/lib/enigma2/python/Plugins/Extensions/DreamPlex/skins/blackDon/720x576/skin.xml"
	elif desktop == 1024:
		skin = "/usr/lib/enigma2/python/Plugins/Extensions/DreamPlex/skins/blackDon/1024x576/skin.xml"
	elif desktop == 1280:
		skin = "/usr/lib/enigma2/python/Plugins/Extensions/DreamPlex/skins/blackDon/1280x720/skin.xml"
	
	if skin:
		loadSkin(skin)
		
	printl2("", "__common__::loadPlexSkin", "C")
#===============================================================================
# 
#===============================================================================
def checkPlexEnvironment():
	'''
	checks needed file structure for plex
	
	@param: none 
	@return none	
	'''
	printl2("","__common__::checkPlexEnvironment", "S")
	
	playerTempFolder = config.plugins.dreamplex.playerTempPath.value
	logFolder = config.plugins.dreamplex.logfolderpath.value
	mediaFolder = config.plugins.dreamplex.mediafolderpath.value
	
	checkDirectory(playerTempFolder)
	checkDirectory(logFolder)
	checkDirectory(mediaFolder)
	
	printl2("","__common__::checkPlexEnvironment", "C")
	
#===============================================================================
# 
#===============================================================================
def checkDirectory(directory):
	'''
	checks if dir exists. if not it is added
	
	@param directory: e.g. /media/hdd/
	@return: none
	'''
	printl2("", "__common__::checkDirectory", "S")
	printl2("checking ... " + directory, "__common__::checkDirectory", "D")
	
	try:
		if not os.path.exists(directory):
			os.makedirs(directory)
			printl2("directory not found ... added", "__common__::checkDirectory", "D")
		else:
			printl2("directory found ... nothing to do", "__common__::checkDirectory", "D")
		
	except Exception, ex:
		printl2("Exception(" + str(type(ex)) + "): " + str(ex), "__common__::checkDirectory", "E")
	
	printl2("","__common__::checkDirectory", "C")

#===============================================================================
# 
#===============================================================================		
def getServerFromURL(url ): # CHECKED
	'''
	Simply split the URL up and get the server portion, sans port
	
	@param url: with or without protocol
	@return: the server URL
	'''
	printl2("","__common__::getServerFromURL", "S")
	
	if url[0:4] == "http" or url[0:4] == "plex":
		
		printl2("", "__common__::getServerFromURL", "C")
		return url.split('/')[2]
	else:
		
		printl2("", "__common__::getServerFromURL", "C")
		return url.split('/')[0]
	
