#!/usr/bin/env python3
"""
cn-readability-extractor: 网页内容提取器
从任意网页提取干净正文，去除广告/导航/脚本
用法: python readability.py <URL>
"""

import sys
import re
import urllib.request
import html.parser
from pathlib import Path

# 简单的HTML标签清理器
class HTMLCleaner(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip_tags = {'script', 'style', 'nav', 'header', 'footer', 'aside', 'form', 'button'}
        self.current_skip = False
        self.skip_depth = 0
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag in self.skip_tags:
            self.current_skip = True
            self.skip_depth += 1
        # 换行标签
        if tag in ('p', 'div', 'br', 'h1', 'h2', 'h3', 'h4', 'li', 'tr'):
            self.text_parts.append('\n')
    
    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip_depth -= 1
            if self.skip_depth <= 0:
                self.current_skip = False
                self.skip_depth = 0
        if tag in ('p', 'div', 'br', 'h1', 'h2', 'h3', 'h4', 'li', 'tr'):
            self.text_parts.append('\n')
    
    def handle_data(self, data):
        if not self.current_skip:
            text = data.strip()
            if text:
                self.text_parts.append(text + ' ')
    
    def get_text(self):
        # 清理多余空行
        text = ''.join(self.text_parts)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)
        return text.strip()


def extract_title(html):
    """提取<title>和<meta>描述"""
    title_match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
    desc_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
    h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', html, re.IGNORECASE)
    
    return {
        'title': title_match.group(1).strip() if title_match else '',
        'description': desc_match.group(1).strip() if desc_match else '',
        'h1': h1_match.group(1).strip() if h1_match else '',
    }


def extract_readable_content(html):
    """提取干净正文"""
    cleaner = HTMLCleaner()
    try:
        cleaner.feed(html)
        return cleaner.get_text()
    except Exception as e:
        return f"解析失败: {e}"


def extract(url):
    """从URL提取内容"""
    html = None
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
    except urllib.error.URLError as e:
        return {'error': f"请求失败: {e}"}
    except Exception as e:
        return {'error': f"请求失败: {e}"}
    
    if html is None:
        return {'error': '获取内容失败'}
    
    meta = extract_title(html)
    content = extract_readable_content(html)
    
    # 截断过长内容
    if len(content) > 5000:
        content = content[:5000] + '\n\n... [内容过长，已截断]'
    
    return {
        'url': url,
        'title': meta['title'],
        'description': meta['description'],
        'content': content,
        'word_count': len(content.split())
    }


def main():
    if len(sys.argv) < 2:
        print("用法: python readability.py <URL>")
        print("示例:")
        print("  python readability.py https://example.com/article")
        print("  python readability.py https://news.ycombinator.com/item?id=123")
        sys.exit(1)
    
    url = sys.argv[1]
    result = extract(url)
    
    if 'error' in result:
        print(f"❌ {result['error']}")
        sys.exit(1)
    
    print(f"📄 {result['title']}")
    print(f"🔗 {result['url']}")
    if result['description']:
        print(f"📝 {result['description']}")
    print(f"\n{'='*40}")
    print(result['content'])
    print(f"\n{'='*40}")
    print(f"📊 字数: {result['word_count']} 字")


if __name__ == '__main__':
    main()
