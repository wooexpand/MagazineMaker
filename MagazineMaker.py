# -*- coding: utf-8 -*-
import os
import re
from PIL import Image
import img2pdf
import yaml

def cut_images(work_path):

    with open(work_path + '\\' + 'setting.yml', 'r') as yml:
        setting = yaml.safe_load(yml)

    # get filelist from workpath
    png_file_list=[]
    for files in os.listdir(work_path):
        if(files[-4:] == '.PNG') :
            png_file_list.append(files)

    print(png_file_list)

    # one function to get all files from a determinded folder
    # _, _, filenames = next(walk(mypath))
    for file_name in png_file_list:

        im_crop_outside = Image.open(work_path+"\\"+file_name)
        # 0,558 - 1283,2250
        im_crop_outside = im_crop_outside.crop((setting['cut']['fromX'],
                                                setting['cut']['fromY'],
                                                setting['cut']['toX'],
                                                setting['cut']['toY']))

        im_crop_outside = im_crop_outside.convert('RGB')  # Change RGBA(png) to RGB(jpg)
        im_crop_outside.save(work_path + '\\' + 'PDF_' + file_name[:-4] + '.jpg', quality=95)

def join_pdf(work_path):
    with open(work_path + '\\' + 'setting.yml', 'r') as yml:
        setting = yaml.safe_load(yml)

    myfilelist2 = []
    for files in os.listdir(work_path):
        if(files[-4:] == '.jpg' and files[:4] == 'PDF_'):
            filepath = os.path.join(work_path, files)
            myfilelist2.append(filepath)
    # layout_ = img2pdf.get_layout_fun('1283,1692')
    a4inpt = (img2pdf.mm_to_pt(setting['pagesize']['wide']),
              img2pdf.mm_to_pt(setting['pagesize']['heigh']))
    layout_ = img2pdf.get_layout_fun(a4inpt)
    with open(work_path + '\\' + setting['pdffilename'], "wb") as aPDF:
        aPDF.write(img2pdf.convert(myfilelist2, layout_fun=layout_))



if __name__ == '__main__':

    with open('config/setting.yml', 'r') as yml:
        setting = yaml.safe_load(yml)

    cut_images(setting['work_folder'])

    join_pdf(setting['work_folder'])
