#!/usr/bin/env python3
"""
Web Fetcher - 免费网页抓取工具
功能：支持JS渲染 + 正文提取 + 结构化输出
"""

import sys
import json
import re
import time
import random
from pathlib import Path

def fetch_page(url: str, domain: str = "general", timeout: int = 30) -> dict:
    """抓取网页，返回结构化内容"""
    
    result = {
        "url": url,
        "success": False,
        "title": None,
        "author": None,
        "published_date": None,
        "content_text": None,
        "content_html": None,
        "word_count": 0,
        "error": None
    }
    
    try:
        from playwright.sync_api import sync_playwright
        from readability import Document
        from lxml import html, etree
        
        with sync_playwright() as p:
            # 启动浏览器
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                viewport={"width": 1280, "height": 800}
            )
            page = context.new_page()
            
            # 访问页面
            page.goto(url, wait_until="networkidle", timeout=timeout*1000)
            
            # 获取HTML
            html_content = page.content()
            
            # Readability提取正文
            doc = Document(html_content)
            result["title"] = doc.title()
            result["content_html"] = doc.summary()
            
            # 从HTML中提取纯文本
            try:
                text_tree = html.fromstring(result["content_html"])
                result["content_text"] = text_tree.text_content()
                result["word_count"] = len(result["content_text"].split())
            except:
                # 如果解析失败，使用简单文本提取
                import re
                result["content_text"] = re.sub(r'<[^>]+>', '', result["content_html"])
                result["word_count"] = len(result["content_text"].split())
            
            # 提取元数据
            meta_tree = html.fromstring(html_content)
            
            # 作者
            author = meta_tree.xpath('//meta[@name="author"]/@content') or \
                    meta_tree.xpath('//meta[@property="article:author"]/@content')
            if author:
                result["author"] = author[0].strip()
            
            # 发布时间
            pub_date = meta_tree.xpath('//meta[@property="article:published_time"]/@content') or \
                      meta_tree.xpath('//time[@datetime]/@datetime')
            if pub_date:
                result["published_date"] = pub_date[0]
            
            browser.close()
            result["success"] = True
            
    except Exception as e:
        result["error"] = str(e)
    
    return result


def extract_metrics(text: str, domain: str = "general") -> dict:
    """从正文提取关键指标"""
    metrics = {}
    text_lower = text.lower()
    
    # 通用指标提取
    if domain in ["healthcare", "medical", "insurance"]:
        # 样本量
        sample_match = re.search(r'(\d{1,3}(?:,\d{3})*)\s*(?:patients?|subjects?|participants?)', text_lower)
        if sample_match:
            metrics['sample_size'] = sample_match.group(1)
        
        # AUC
        auc_match = re.search(r'auc\s*[=:of]*\s*(0\.\d{2,3})', text_lower)
        if auc_match:
            metrics['auc'] = float(auc_match.group(1))
        
        # 准确率
        acc_match = re.search(r'accurac(?:y|ies)\s*[=:]*\s*(\d{1,2}\.\d?)%?', text_lower)
        if acc_match:
            metrics['accuracy'] = float(acc_match.group(1))
    
    # 成本相关
    cost_match = re.search(r'(\d+\.?\d*)\s*%?\s*(?:cost|saving|reduction)', text_lower)
    if cost_match:
        metrics['cost_data'] = cost_match.group(1)
    
    return metrics


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python web-fetcher.py <url> [--domain <domain>]")
        print("示例: python web-fetcher.py 'https://arxiv.org/abs/2301.12345' --domain 'machine learning'")
        sys.exit(1)
    
    url = sys.argv[1]
    domain = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == "--domain" else "general"
    
    # 抓取
    result = fetch_page(url, domain)
    
    # 提取指标
    if result["success"] and result["content_text"]:
        result["extracted_metrics"] = extract_metrics(result["content_text"], domain)
    
    # 输出JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))
