#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-11-30 14:48:36
# Project: demo1
# Author: Feng L.

from pyspider.libs.base_handler import *
import os



class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.cur_pn = 1
        self.total_pn = 500
        self.page_step = 30;
        self.counter = 0

        self.filename = 'questions-1'

        path = "F:\\questionsdata\\"
        exists = os.path.exists(path)

        if not exists:
            os.makedirs(path)

        self.fobj = open(path + self.filename, 'w');

        self.headers_1 = {
            "Host": "zhidao.baidu.com",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Referer": "https://zhidao.baidu.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "IK_CID_78=1; IK_CID_1101=1; IK_CID_1=1; __cfduid=d8fde44e32a25045eaaa3e905d16a0d841508469708; IK_CID_77=6; IK_CID_95=1; IK_CID_1031=3; IK_CID_80=2; IK_CID_84=7; IK_CID_82=6; IK_CID_83=8; IK_083BA8BD123ED95CBB0A1F2D638ECFCF=1; IK_CID_74=28; isColumnClick=click; ZHIDAO_UHOME_MSGGUID=1; BAIDUID=A2D4ECDCB211F8623E1BD0CC849C9717:FG=1; BIDUPSID=A2D4ECDCB211F8623E1BD0CC849C9717; PSTM=1512095223; BDRCVFR[uS-dYPoyvhY]=mk3SLVN4HKm; PSINO=2; H_PS_PSSID=1443_24868_21097_25178_22074; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; Hm_lvt_6859ce5aaf00fb00387e6434e4fcc925=1512041860,1512051214,1512053700,1512098633; Hm_lpvt_6859ce5aaf00fb00387e6434e4fcc925=1512099044"
        }

    @every(minutes=24 * 60)
    def on_start(self):
        pn = 0;
        while self.cur_pn <= self.total_pn:
            pn = pn + self.page_step
            self.cur_pn += 1

            url_hot = "https://zhidao.baidu.com/list?type=hot&pn=" + str(
                pn) + "&ie=utf8&_pjax=%23j-question-list-pjax-container"
            url_highscore = "https://zhidao.baidu.com/list?type=highScore&pn=" + str(
                pn) + "&ie=utf8&_pjax=%23j-question-list-pjax-container"

            print(url_hot)
            print(url_highscore)

            self.crawl(url_hot, headers=self.headers_1, callback=self.index_page, validate_cert=False)
            self.crawl(url_highscore, headers=self.headers_1, callback=self.index_page, validate_cert=False)
        self.cur_pn = 1

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('div.question-title-section').items():
            question = each.find('div.question-title > a')
            taglist = each.find('div.question-tags a').items()
            tags = []
            for tag in taglist:
                tags.append(tag.text())
            self.counter = self.counter + 1
            print("get question", self.counter, ':', question.text(), "tags:", tags)

            self.fobj.write(question.text() + '    tags:' + str(tags) + '\n')
        return {
            "counter": self.counter
        }

    @config(priority=2)
    def processing2(self, response):
        pass

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }






