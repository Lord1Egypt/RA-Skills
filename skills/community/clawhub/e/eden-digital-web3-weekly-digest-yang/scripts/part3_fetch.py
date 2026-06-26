#!/usr/bin/env python3
import subprocess, re, sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime

INCLUDE_KW = [
    '监管','法案','SEC','CFTC','FDIC','立法','合规','禁止','政策',
    '证监','金融局','央行','MiCA','GENIUS','CLARITY','国会','议会',
    '金管局','证监会','整治','处罚','执法','调查','合法化','许可',
    '牌照','VASP','FSB','FATF','反洗钱','稳定币立法','虚拟资产条例'
]
EXCLUDE_KW = ['价格','涨幅','跌幅','清算','链上数据','空投奖励','回购销毁','行情','日报','早报','研报','教程','攻略','巨鲸']

def fetch_rss(page):
    r = subprocess.run(['curl','-s','-L','--max-time','15',
        f'https://www.techflowpost.com/api/client/common/rss.xml?page={page}'],
        capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ''

def parse_rss(xml_text):
    try: root = ET.fromstring(xml_text)
    except ET.ParseError: return []
    items = []
    for item in root.iter('item'):
        title = item.findtext('title','').strip()
        desc  = re.sub(r'<[^>]+>','',item.findtext('description','')).strip()
        pubdate = item.findtext('pubDate','').strip()
        link  = item.findtext('link','').strip()
        try: dt = parsedate_to_datetime(pubdate)
        except: continue
        items.append({'title':title,'desc':desc,'dt':dt,'link':link})
    return items

if __name__ == '__main__':
    one_week_ago = datetime.now().astimezone() - timedelta(days=7)
    results, seen = [], set()
    for page in range(1, 6):
        xml_text = fetch_rss(page)
        if not xml_text: break
        items = parse_rss(xml_text)
        if not items: break
        hit_old = False
        for item in items:
            if item['dt'] < one_week_ago: hit_old = True; continue
            text = item['title'] + item['desc']
            if any(k in text for k in INCLUDE_KW) and not any(k in item['title'] for k in EXCLUDE_KW) and item['title'] not in seen:
                seen.add(item['title']); results.append(item)
        if hit_old: break
    print(f"共抓取 {len(results)} 条监管/行业新闻\n")
    for r in results:
        print(f"[{r['dt'].strftime('%m/%d')}] {r['title']}\n  {r['link']}\n")
