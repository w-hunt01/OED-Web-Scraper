# The purpose of this script is to demonstrate a method for a Pythonic web bot to scrape all applicable historical definitions #
#   of a given word from the the Oxford English Dictionary (OED). #
# There is a standard script for navigating to the main webpage whereby the OED may be accesssed, and then three functions for #
#   scraping the historical definitions, etymology, and frequency from the OED (contingent on user objectives). # 
# In it's current iteration, this script was made to take a a single input before line 168 #
import os
import traceback
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import TimeoutException
import PasswordEncoder as E
# The encoder is a simple cipher, used to mask the user name and password # 
import os
import time
import csv
from datetime import datetime

browser = webdriver.Safari()

browser.get("https://aspen.greenvillelibrary.org/MyAccount/Home")

browser.implicitly_wait(10)
time.sleep(1)

username = browser.find_element("name","username")
password = browser.find_element("name","password")

username.send_keys(E.encoder(E.username_gclOED))
WebDriverWait(webdriver,10)
time.sleep(1)
password.send_keys(E.encoder(E.pw_gclOED))
WebDriverWait(webdriver,10)
time.sleep(1)

loginbox = browser.find_element("name","submit")
WebDriverWait(webdriver,10)
loginbox.send_keys(Keys.RETURN)
time.sleep(1)
browser.implicitly_wait(10)
WebDriverWait(webdriver,10)

browser.get("https://gcls.idm.oclc.org/login?url=https://www.oed.com")

time.sleep(2)
browser.implicitly_wait(10)
WebDriverWait(webdriver,30)

username2 = browser.find_element("name","user")
password2 = browser.find_element("name","pass")

username2.send_keys(E.encoder(E.username_gclOED))
WebDriverWait(webdriver,30)
time.sleep(1)
password2.send_keys(E.encoder(E.pw_gclOED))
password2.send_keys(Keys.RETURN)
WebDriverWait(webdriver,10)
time.sleep(1)

# This function is for scraping the historical definitions of a given word, and should work for however many defitions may exist, #
#   whether this is numbered in tens, hundreds, or thousands # 
def LOOKUP(word):
    searchbox = browser.find_element("name","q")
    searchbox.clear()
    searchbox.send_keys(word)
    searchbox.send_keys(Keys.RETURN)
    WebDriverWait(webdriver, 30)
    time.sleep(2)

# The href should follow a conventional format, in which the word in quesiton occupies a set space within the hypertext #     
    try:
        meaningshref = f"https://www.oed.com/search/advanced/Meanings?textTermText0={word}&textTermOpt0=WordPhrase"
        browser.get(meaningshref)
        time.sleep(5)
    except: NoSuchElementException
    else: pass

    WebDriverWait(webdriver,5)
    time.sleep(1)

# Should this method fail, then the web bot will try a more brute-force method of selecting where the appropriate link should exist on the web page # 
    try:

        totalmeanings = browser.find_element("xpath","//*[@id='wordsAndPhrasesResultsTab']/div/div[2]/div[1]/div[1]/span[1]/span[3]")
        print(word, " | ", totalmeanings.text)
        time.sleep(1)
        browser.refresh()

    except: NoSuchElementException
    else: pass

# This funciton should look up and record all historical definitions within the OED for a given word #
def ZLOOKUP(word, hyperlink):
    time.sleep(2)

# The hyperlink should follow a conventional format (as seen above)# 
    browser.get(hyperlink)
    time.sleep(3)

# There may be multiple OED pages for any word referenced; those pages, however, will follow a systematic syntax #
# Declare variables i1 and i2 so that they are reflexive; element numbering will be incrimental over however many pages of definitions #
#   occur, but this syntax should make the Pythonic reflexive in anticipating which numeric value those elements take on the web page #
    i0 = browser.find_element("xpath","//*[@id='wordsAndPhrasesResultsTab']/div/div[2]/div[1]/div[1]/span[1]/span[2]").text
    ii = browser.find_element("xpath","//*[@id='wordsAndPhrasesResultsTab']/div/div[2]/div[1]/div[1]/span[1]/span[1]").text
    i1 = (int(i0) - int(ii) + int(2))
    i2 = int(1)

# This list format should create a loop in which the Pythonic web bot will continue collecting definitions as long as conditions are met #
#   (i.e., there continue to be definitions on the web page). #
    for i in range(i2,i1):
        dateranges = browser.find_elements("xpath",f"//*[@id='wordsAndPhrasesMCS']/div[{i}]/div[1]/span")
        for b in dateranges:
                meanings = browser.find_elements("xpath",f"//*[@id='wordsAndPhrasesMCS']/div[{i}]/div[2]/h3/a/span[1]")
                for c in meanings:
                    grammarians = browser.find_elements("xpath",f"//*[@id='wordsAndPhrasesMCS']/div[{i}]/div[2]/h3/a/span[3]")
                    for g in grammarians:
                        definitions = browser.find_elements("xpath",f"//*[@id='wordsAndPhrasesMCS']/div[{i}]/div[2]/div")
                        for h in definitions: 
                            print(word, " | ", b.text, " | ", c.text, " | ", g.text, " | " , h.text)
    
    time.sleep(1)
    browser.refresh()
    time.sleep(1)

# This method is used for scraping the part of speech for a given word #
# This method uses the hyperlink for a specific word, which should follow a systematic convention based on the word itself # 
def ELOOKUP(Word, PartOfSpeech, hyperlink):
    time.sleep(2)

    browser.get(hyperlink)

    time.sleep(5)

    try:
        Summary = browser.find_element("xpath","//*[@id='etymology']/div[2]/div/div/div[1]")
        EtymologyText = browser.find_element("xpath","//*//*[@id='etymology']/div[2]/div/div")
# For the output file, a special character '~' is used to seperate text sections #         
        print(Word, " ~ ", PartOfSpeech, " ~ ", Summary.text, " ~ ", EtymologyText.text)

        browser.refresh()
        time.sleep(2)

    except: NoSuchElementException
    else: pass

    
def RLOOKUP(Word, PartOfSpeech, hyperlink):
    time.sleep(2)

    browser.get(hyperlink)

    time.sleep(4)

    try:
        FrequencyAria = browser.find_element("xpath","//*[@id='frequency']/div[2]/div/div/div")
        print(Word, ' ~ ', PartOfSpeech, ' ~ ', FrequencyAria.text)
        browser.refresh()
        time.sleep(2)
    except: NoSuchElementException
    else: pass

print('Lookup Successful')

browser.close()
