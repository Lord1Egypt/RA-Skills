#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arXiv论文搜索和下载工具
"""

import os
import re
import sys
import time
import requests
from urllib.parse import quote

SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "papers")
os.makedirs(SAVE_DIR, exist_ok=True)

def clean_filename(title):
    """清理文件名"""
    return re.sub(r'[\\/*?:"<>|]', "", title)[:80]

def search_arxiv(keyword, max_results=5):
    """搜索arXiv"""
    print(f"\n{'='*70}")
    print(f"🔍 arXiv搜索：{keyword}")
    print(f"{'='*70}\n")
    
    # 使用arXiv API
    api_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{keyword}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance"
    }
    
    try:
        resp = requests.get(api_url, params=params, timeout=30)
        
        # 解析XML
        import xml.etree.ElementTree as ET
        root = ET.fromstring(resp.content)
        
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        entries = root.findall('atom:entry', ns)
        
        if not entries:
            print("❌ 未找到相关论文")
            return []
        
        print(f"📊 找到 {len(entries)} 篇相关论文\n")
        
        papers = []
        for entry in entries:
            title = entry.find('atom:title', ns).text.strip()
            arxiv_id = entry.find('atom:id', ns).text.split("/")[-1]
            
            authors = []
            for author in entry.findall('atom:author', ns):
                name = author.find('atom:name', ns)
                if name is not None:
                    authors.append(name.text)
            
            abstract = entry.find('atom:summary', ns)
            abstract_text = abstract.text.strip() if abstract is not None else ""
            
            published = entry.find('atom:published', ns)
            pub_date = published.text[:10] if published is not None else ""
            year = pub_date[:4] if pub_date else "unknown"
            
            papers.append({
                "id": arxiv_id,
                "title": title,
                "authors": authors,
                "abstract": abstract_text[:300] + "...",
                "year": year,
                "date": pub_date,
                "link": f"https://arxiv.org/abs/{arxiv_id}",
                "pdf": f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            })
        
        return papers
        
    except Exception as e:
        print(f"❌ 搜索失败: {e}")
        return []

def download_pdf(arxiv_id, title, year):
    """下载PDF"""
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    
    try:
        print(f"    ⬇️  下载中：{pdf_url}")
        time.sleep(1)
        
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        }
        
        resp = requests.get(pdf_url, headers=headers, timeout=60, stream=True)
        
        if resp.status_code == 200:
            filename = f"{clean_filename(title)}_{year}_arXiv.pdf"
            path = os.path.join(SAVE_DIR, filename)
            
            with open(path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            file_size = os.path.getsize(path)
            if file_size > 50000:
                print(f"    ✅ 下载成功：{filename} ({file_size//1024}KB)")
                return filename
            else:
                os.remove(path)
        
        print(f"    ⚠️  下载失败")
        return None
        
    except Exception as e:
        print(f"    ❌ 下载出错: {e}")
        return None

def display_results(papers, download=True):
    """显示搜索结果"""
    for idx, p in enumerate(papers):
        print(f"{'─'*70}")
        print(f"📄 【论文 {idx+1}】{p['id']}")
        print(f"{'─'*70}")
        print(f"📌 标题：{p['title']}")
        print(f"👥 作者：{', '.join(p['authors'][:3])}")
        if len(p['authors']) > 3:
            print(f"         等 {len(p['authors'])} 位作者")
        print(f"📅 发布：{p['date']}")
        print(f"🔗 链接：{p['link']}")
        print(f"\n📝 摘要：{p['abstract']}")
        
        if download:
            print(f"\n⬇️  正在下载PDF...")
            download_pdf(p['id'], p['title'], p['year'])
        
        print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n使用方法：")
        print("  python simple_arxiv.py <关键词> [数量]")
        print("\n示例：")
        print("  python simple_arxiv.py 'community detection' 5")
        sys.exit(1)
    
    keyword = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) >= 3 else 5
    
    papers = search_arxiv(keyword, max_results)
    if papers:
        display_results(papers, download=True)
        print(f"\n{'='*70}")
        print(f"✅ 完成！PDF保存在：{SAVE_DIR}")
        print(f"{'='*70}\n")
