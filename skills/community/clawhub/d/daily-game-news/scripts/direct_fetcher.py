#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct Website Fetcher
直接爬取网站 HTML 内容（需要为每个网站定制解析规则）
"""

import sys
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def fetch_gamersky():
    """爬取游民星空"""
    url = "https://www.gamersky.com/news/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'gbk'  # 游民星空使用 GBK 编码
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        # 游民星空新闻列表选择器
        for item in soup.select('.newslist li, .topnews')[:10]:
            title_elem = item.select_one('a')
            time_elem = item.select_one('.time, .datetime')
            
            if title_elem:
                articles.append({
                    'title': title_elem.get('title', title_elem.get_text(strip=True)),
                    'url': title_elem.get('href', ''),
                    'published': time_elem.get_text(strip=True) if time_elem else '',
                    'content': ''
                })
        
        return articles
    except Exception as e:
        return []


def fetch_gcores():
    """爬取机核"""
    url = "https://www.gcores.com/news"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        for item in soup.select('.original.am_card')[:10]:
            title_elem = item.select_one('h3 a')
            time_elem = item.select_one('time')
            
            if title_elem:
                articles.append({
                    'title': title_elem.get_text(strip=True),
                    'url': 'https://www.gcores.com' + title_elem.get('href', ''),
                    'published': time_elem.get('datetime', '') if time_elem else '',
                    'content': ''
                })
        
        return articles
    except Exception as e:
        return []


def fetch_yystv():
    """爬取游研社"""
    url = "https://www.yystv.cn/docs"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        for item in soup.select('.article-item')[:10]:
            title_elem = item.select_one('a')
            time_elem = item.select_one('.time')
            
            if title_elem:
                articles.append({
                    'title': title_elem.get_text(strip=True),
                    'url': 'https://www.yystv.cn' + title_elem.get('href', ''),
                    'published': time_elem.get_text(strip=True) if time_elem else '',
                    'content': ''
                })
        
        return articles
    except Exception as e:
        return []


def fetch_website(site_id, base_url):
    """根据网站 ID 选择对应的爬取函数"""
    fetchers = {
        'gamersky': fetch_gamersky,
        'gcores': fetch_gcores,
        'yystv': fetch_yystv,
    }
    
    fetcher = fetchers.get(site_id)
    if fetcher:
        return fetcher()
    return []


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(json.dumps({'error': 'Missing arguments. Usage: script.py <site_id> <base_url>'}))
        sys.exit(1)
    
    site_id = sys.argv[1]
    base_url = sys.argv[2]
    
    articles = fetch_website(site_id, base_url)
    
    print(json.dumps({
        'site_id': site_id,
        'articles': articles
    }, ensure_ascii=False, indent=2))
