import os
import re
import sys
import cv2
import time
import glob
import shutil
import urllib
import os.path
import requests
import linecache
import pyautogui
import subprocess
import pytesseract
from os import path
from PIL import Image
from io import StringIO
from selenium import webdriver
from subprocess import Popen, PIPE
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options



# browser instance
options = Options()
options.add_argument("--headless=new")
options.add_argument("--start-maximized")
browser = webdriver.Firefox(options=options)
browser.maximize_window()
action = ActionChains(browser)

##screenWidth, screenHeight = pyautogui.size()
##print(screenWidth)
##print(screenHeight)

# target URL
mainURL = 'https://portal.digitalsabah.gov.my/'
browser.get(mainURL)
time.sleep(3)

# admin login
penjawat_awam = browser.find_element("xpath", '//*[@id="dgd"]')
penjawat_awam.click()
time.sleep(1)

myKad = '880621125761' # your own ga'damn ic
pswd = '#'  # your own ga'daman password

ic = browser.find_element("xpath", '//*[@id="dgdlogin"]')
klaluan = browser.find_element("xpath", '//*[@id="dgdpassword"]')

ic.send_keys(myKad)
klaluan.send_keys(pswd)

# execute login 
log_masuk = browser.find_element("xpath", '//*[@id="DGDLogin"]')
log_masuk.click()

#navigate to konfigurasi > kelulusan pertukaran email
# let the page load : adjust depends on load speed
time.sleep(7)

konfigurasi = browser.find_element("xpath", '/html/body/div[2]/header/ul[1]/div/nav/ul[2]/li[2]/a/div/span')  
konfigurasi.click()
time.sleep(1)
pertukaran = browser.find_element("xpath", '/html/body/div[2]/header/ul[1]/div/nav/ul[2]/li[2]/ul/li[6]/a')
pertukaran.click()
time.sleep(3)
view = browser.find_element("xpath", '/html/body/div[3]/div[5]/div[1]/div[2]/div/div/div/div[2]/table/tbody/tr[1]/td[2]/input')
view.click()
time.sleep(7)
#support_docs = browser.find_element("xpath", '/html/body/div[3]/div[5]/div[1]/div[2]/div/form/div/div[3]/div/div/div[1]/div/a')
# /html/body/div[3]/div[5]/div[1]/div[2]/div/form/div/div[3]/div/div/div[1]/div/a
# /html/body/div[3]/div[5]/div[1]/div[2]/div/form/div/div[3]/div/div/div[1]/div/a/div/p/svg
#support_docs.click()
#URL = browser.find_element('css selector', 'pointer')
#print(URL)

#find the element and get the attribute value of onclick
onClickValue = browser.find_element("xpath","/html/body/div[3]/div[5]/div[1]/div[2]/div/form/div/div[4]/div/div/div[1]/div/a").get_attribute("onclick")

# check if uploaded document is image or pdf
check_format_type = browser.find_element("xpath", '/html/body/div[3]/div[5]/div[1]/div[2]/div/form/div/div[4]/div/div/div[1]/div/a/div/p').text
subString = "pdf"

#extract link / remove unwanted parameters
filter_01 = onClickValue.replace('window.open', '')
filter_02 = filter_01.replace('Lampiran', '')
filter_03 = filter_02.replace('width=300', '')
filter_04 = filter_03.replace('height=300', '')
filter_05 = filter_04.replace(',', '')
filter_06 = filter_05.replace("'", '')
filter_07 = filter_06.replace("(", '')
filter_08 = filter_07.replace(")", '')

IMGrepo = mainURL + filter_08
print(IMGrepo)

browser.get(IMGrepo)
time.sleep(7)

if subString in check_format_type:
    print("do page screenshot")

    #take page screenshot
    fullpageshot = browser.get_screenshot_as_file("screenshot_01.png")
else:
    print("do old-skool")
    
    #old-skool method save image 
    pyautogui.moveTo(500, 500, duration=1)
    pyautogui.rightClick()
    time.sleep(1)
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('enter')
    pyautogui.moveTo(300, 50, duration=1)
    pyautogui.leftClick()
    pyautogui.write('Desktop\Py_ValidatorMail\download_images')
    pyautogui.press('enter')
    pyautogui.keyDown('alt')
    time.sleep(3)
    pyautogui.keyDown('s')
    pyautogui.keyUp('alt')
    pyautogui.keyUp('s')

#custom handle for filetype other than images, use page screenshot; otherwise use old-kool method


#response = requests.get(IMGrepo)
##response = requests.get(
##    IMGrepo, 
##    headers = {
##        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
##    },
##    stream = True
##)

# Function below couldn't save page as image; require right-click and save as emulation ?

#with open("image.png", "wb") as imageFile:
#    imageFile.write(response.content)
#    print('Image download completed.')

#inBrowser_img = browser.find_element("xpath", '/html')

time.sleep(9)
browser.back()

#img_url = 'https://blog.finxter.com/wp-content/uploads/2022/04/greenland_02a.jpg'
#img = Image.open(requests.get(IMGrepo, stream = True).raw)
#img.save('IMG_02a.png')


#########################################################################################################################################################


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
root_dir = r'C:\Users\Fauzi\Desktop\Py_ValidatorMail\download_images'


file_format = ".png" #change format globally , eg: .png/.jpeg/.jpg
regex_1 = "\d{6}"
regex_2 = "\d{2}"
regex_3 = "\d{4}"

for filename in glob.iglob(root_dir + '**/*' + file_format, recursive=True):
    #adjusting contrast on the image for better read
    
    standard_img = Image.open(filename)
    #bw_img = standard_img.convert('1')
    standard_img.save('result.png')


    current_img = cv2.imread('result.png')
    gray_image = cv2.cvtColor(current_img, cv2.COLOR_BGR2GRAY) 
    alpha = 1.0 # Contrast control (1.0-3.0)
    beta = 0 # Brightness control (0-100)
    adjusted = cv2.convertScaleAbs(gray_image, alpha=alpha, beta=beta)
    #open window adjusted image
    cv2.imshow('processed image', adjusted)
    #adjusted.save('final_result.png')
    
    while True:
        try:
            textImg = pytesseract.image_to_string(adjusted)
            #find_ic = re.findall(r'_(\d{6})', textImg)
            #filter_filler = textImg.split("PENDAFTARAN NEGARA",1)[1]
            #exclude_filler01 = filter_filler[0:17]
            #exclude_filler02 = exclude_filler01.replace(" ", '')
            #applicant_ic = exclude_filler02.replace("-", '')
            #print(applicant_ic)
            #print(find_ic)
            break
        except ValueError:
            print("Oops!  file is corrupted! ")
            pass

    #textImg = pytesseract.image_to_string(filename)
    text = str(textImg.strip())

    #print(textImg)
    print(text)

    #find a way to extract ic from ocr results
    regex_prefix = re.findall(regex_1, text)
    regex_mid = re.findall(regex_2, text)
    regex_suffix = re.findall(regex_3, text)
    print(regex_prefix)
    print(regex_mid)
    print(regex_suffix)
    find_ic = str(regex_prefix) 


    ic_pemohon = browser.find_element("xpath", '/html/body/div[3]/div[5]/div[1]/div[2]/div/form/div/div[1]/div/div/div[1]/div/input').get_attribute('value')
    nama_pemohon = browser.find_element("xpath", '/html/body/div[3]/div[5]/div[1]/div[2]/div/form/div/div[1]/div/div/div[2]/div/input').get_attribute('value')
    print("Nama Pemohon: " + nama_pemohon + " No IC Pemohon: " + ic_pemohon)
    print(len(ic_pemohon))
    print(len(find_ic))
    print("penama dokumen: " + find_ic)
    ic_applicant = ic_pemohon[0:6]
    time.sleep(3)

    if str(find_ic.strip()) == str(ic_applicant.strip()):
        approve_btn = browser.find_element("xpath", '//*[@id="Approve"]')
        print("boleh approve")
        #approve_btn.click()
        complete_btn = browser.find_element("xpath", '/html/body/div[4]/div/div[3]/button[1]')
        #complete_btn.click()
    else:
        to_listname = browser.find_element("xpath", '//*[@id="Return"]')
        print("documents enda ngam")
        #to_listname.click()
        
    
    
    
