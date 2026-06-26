import os
import sys
import json
import datetime
import urllib.request
import re

# 严格锁定的第一梯队精准栏目页
SOURCES = [
    {"title": "The Batch", "url": "https://www.deeplearning.ai/the-batch/rss/", "type": "rss"},
    {"title": "Ben's Bites", "url": "https://www.bensbites.co/rss", "type": "rss"},
    {"title": "Banking Dive", "url": "https://www.bankingdive.com/feeds/news/", "type": "rss"},
    {"title": "中国金融电脑-科技资讯", "url": "https://www.fcc.com.cn/art/kjzx/", "type": "html_list", "base_url": "https://www.fcc.com.cn"},
    {"title": "中国电子银行网-数字银行", "url": "https://www.cebnet.com.cn/szyh/", "type": "html_list", "base_url": "https://www.cebnet.com.cn"},
    {"title": "中国电子银行网-金融AI", "url": "https://www.cebnet.com.cn/financialai/", "type": "html_list", "base_url": "https://www.cebnet.com.cn"},
    {"title": "移动支付网-首页", "url": "https://www.mpaypass.com.cn/", "type": "html_list", "base_url": "https://www.mpaypass.com.cn"},
    {"title": "移动支付网-金科专栏", "url": "https://www.mpaypass.com.cn/authordefault.asp?id=80115", "type": "html_list", "base_url": "https://www.mpaypass.com.cn"}
]

# 核心初筛关键词：只有列表页标题包含这些词，才值得爬取详情页全文
FILTER_KEYWORDS = r"(银行|智能|风控|大模型|分布式|数字化|金融科技|AI|算法|深度学习|核心系统|架构)"

def fetch_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.read().decode(r.headers.get_content_charset() or 'utf-8', errors='ignore')
    except Exception:
        return ""

def extract_pure_text(html_content):
    """通用正文提取：剥离脚本、样式表及HTML标签，留下高密度文本"""
    text = re.sub(r'<script[^>]*>([\s\S]*?)</script>', '', html_content)
    text = re.sub(r'<style[^>]*>([\s\S]*?)</style>', '', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:2500] # 每篇详情页限制前 2500 字，防止大模型爆 Token

def main():
    final_payload = []
    
    for src in SOURCES:
        html = fetch_html(src["url"])
        if not html: continue
        
        links_to_crawl = []
        
        # A阶：解析列表页/RSS列表
        if src["type"] == "rss":
            # RSS 自带了部分正文或摘要，直接视为详情
            items = re.findall(r'<item>([\s\S]*?)</item>', html)[:5]
            for item in items:
                title = (re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', item) or re.findall(r'<title>(.*?)</title>', item) or [""])[0]
                desc = (re.findall(r'<description><!\[CDATA\[(.*?)\]\]></description>', item) or re.findall(r'<description>(.*?)</description>', item) or [""])[0]
                if re.search(FILTER_KEYWORDS, title + desc, re.I):
                    final_payload.append({"source": src["title"], "title": title, "content": extract_pure_text(desc)})
        
        elif src["type"] == "html_list":
            # 匹配经典的超链接格式 href="path"
            raw_links = re.findall(r'href=["\']([^"\']+\.html[^"\']*)["\'][^>]*>([\s\S]*?)</a>', html)
            seen_urls = set()
            
            for url, anchor_text in raw_links:
                clean_title = extract_pure_text(anchor_text)
                if len(clean_title) < 6 or not re.search(FILTER_KEYWORDS, clean_title):
                    continue
                
                # 补全相对路径 URL
                full_url = url if url.startswith("http") else src["base_url"] + ("/" + url if not url.startswith("/") else url)
                if full_url in seen_urls: continue
                seen_urls.add(full_url)
                
                links_to_crawl.append({"title": clean_title, "url": full_url})
            
            # B阶：深入详情页抓取全文（每个网站每天最多精读最新的 3 篇，防封锁）
            for item in links_to_crawl[:3]:
                detail_html = fetch_html(item["url"])
                if detail_html:
                    # 尝试定位主流正文容器，如果没有则提取全页纯文本
                    body_match = re.search(r'(<article[\s\S]*?</article>|<div[^>]+(?:content|article|body|text)[\s\S]*?>[\s\S]*?</div>)', detail_html)
                    target_html = body_match.group(1) if body_match else detail_html
                    pure_text = extract_pure_text(target_html)
                    
                    final_payload.append({
                        "source": src["title"],
                        "title": item["title"],
                        "content": pure_text
                    })

    print(json.dumps({"status": "success", "articles": final_payload}, ensure_ascii=False))

if __name__ == "__main__":
    main()