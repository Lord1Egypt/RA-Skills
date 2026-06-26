#!/usr/bin/env python3
"""
Article Extract - 网页文章内容提取工具
支持微信公众号、博客、新闻等网页的正文提取
"""

import sys
import re
import urllib.request
from html.parser import HTMLParser


class TextExtractor(HTMLParser):
    """HTML 文本提取器 - 过滤脚本和样式标签"""
    
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = 0
        self.skip_tags = {'script', 'style', 'nav', 'footer', 'header', 'aside'}
    
    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip += 1
    
    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip -= 1
    
    def handle_data(self, data):
        if self.skip <= 0:
            self.text.append(data)
    
    def get_text(self):
        return ' '.join(self.text)


def fetch_url(url):
    """抓取网页内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching URL: {e}", file=sys.stderr)
        return None


def extract_text(html):
    """从 HTML 中提取纯文本"""
    # 移除 script 和 style 标签（预处理）
    html = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', ' ', html, flags=re.DOTALL | re.IGNORECASE)
    
    # 解析 HTML
    parser = TextExtractor()
    try:
        parser.feed(html)
        text = parser.get_text()
    except Exception:
        # 备用方案：正则提取
        text = re.sub(r'<[^>]+>', ' ', html)
    
    # 清理文本
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def main():
    if len(sys.argv) < 2:
        print("Usage: extract.py <url>", file=sys.stderr)
        print("Example: extract.py 'https://mp.weixin.qq.com/s/...'", file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[1]
    
    print(f"Fetching: {url}", file=sys.stderr)
    html = fetch_url(url)
    
    if not html:
        sys.exit(1)
    
    text = extract_text(html)
    
    # 输出结果
    print(text)


if __name__ == "__main__":
    main()
