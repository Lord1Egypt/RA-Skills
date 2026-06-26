#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
社区检测论文搜索工具 - 专门优化版
功能：搜索、显示引用量、提取创新点、下载PDF
"""

import os
import re
import sys
import time
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# 配置
SAVE_DIR = os.path.expanduser("~/Desktop/papers/社区检测")
os.makedirs(SAVE_DIR, exist_ok=True)

ARXIV_API = "http://export.arxiv.org/api/query"

def clean_filename(title):
    """清理文件名"""
    return re.sub(r'[\\/*?:"<>|]', "", title)[:80]

def search_papers(keyword, max_results=8):
    """搜索论文"""
    print(f"\n{'='*80}")
    print(f"🔍 搜索：{keyword}")
    print(f"{'='*80}\n")
    
    params = {
        "search_query": f"all:{keyword}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance"
    }
    
    try:
        print("📡 正在请求arXiv API...")
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(ARXIV_API, params=params, headers=headers, timeout=30)
        
        if resp.status_code != 200:
            print(f"❌ API请求失败: {resp.status_code}")
            return []
        
        root = ET.fromstring(resp.content)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        entries = root.findall('atom:entry', ns)
        
        print(f"✅ 找到 {len(entries)} 篇论文\n")
        
        papers = []
        for entry in entries:
            # 提取基本信息
            title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
            arxiv_id = entry.find('atom:id', ns).text.split("/")[-1]
            
            # 作者
            authors = []
            for author in entry.findall('atom:author', ns):
                name = author.find('atom:name', ns)
                if name is not None:
                    authors.append(name.text)
            
            # 摘要
            abstract = entry.find('atom:summary', ns)
            abstract_text = abstract.text.strip() if abstract is not None else ""
            
            # 日期
            published = entry.find('atom:published', ns)
            pub_date = published.text[:10] if published is not None else ""
            year = pub_date[:4] if pub_date else "unknown"
            
            # 分类
            categories = []
            for cat in entry.findall('atom:category', ns):
                term = cat.get('term')
                if term:
                    categories.append(term)
            
            papers.append({
                "id": arxiv_id,
                "title": title,
                "authors": authors,
                "abstract": abstract_text,
                "year": year,
                "date": pub_date,
                "categories": categories,
                "link": f"https://arxiv.org/abs/{arxiv_id}",
                "pdf": f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            })
        
        return papers
        
    except Exception as e:
        print(f"❌ 搜索出错: {e}")
        return []

def extract_innovation(abstract):
    """提取创新点"""
    if not abstract:
        return "（需查看原文）", "（需查看原文）"
    
    # 按句子分割
    sentences = re.split(r'[.!?]\s+', abstract)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
    
    if len(sentences) >= 4:
        # 核心工作：前2-3句
        work = ". ".join(sentences[:3]) + "."
        
        # 创新点：寻找关键词
        innovation_keywords = ['propose', 'introduce', 'present', 'novel', 'new', 'first', 
                               'improve', 'achieve', 'demonstrate', 'show', 'outperform']
        
        innovation_sentences = []
        for sent in sentences[2:]:
            sent_lower = sent.lower()
            if any(kw in sent_lower for kw in innovation_keywords):
                innovation_sentences.append(sent)
        
        if innovation_sentences:
            innovation = ". ".join(innovation_sentences[:2]) + "."
        else:
            innovation = ". ".join(sentences[-2:]) + "."
            
    elif len(sentences) >= 2:
        work = sentences[0] + "."
        innovation = sentences[-1] + "."
    else:
        work = abstract[:300] + "..." if len(abstract) > 300 else abstract
        innovation = work
    
    return work, innovation

def download_pdf(arxiv_id, title, year):
    """下载PDF"""
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    
    try:
        print(f"    ⬇️  正在下载...")
        time.sleep(0.5)
        
        headers = {"User-Agent": "Mozilla/5.0"}
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
                print(f"    ✅ 已下载: {filename} ({file_size//1024}KB)")
                return filename
            else:
                os.remove(path)
        
        print(f"    ⚠️  下载失败，手动下载: {pdf_url}")
        return None
        
    except Exception as e:
        print(f"    ❌ 下载出错: {e}")
        return None

def display_results(papers):
    """显示结果"""
    for idx, p in enumerate(papers, 1):
        print(f"{'━'*80}")
        print(f"📄 【论文 {idx}】{p['id']}")
        print(f"{'━'*80}")
        print(f"📌 标题：{p['title']}")
        print(f"👥 作者：{', '.join(p['authors'][:3])}")
        if len(p['authors']) > 3:
            print(f"         等 {len(p['authors'])} 位作者")
        print(f"📅 发布：{p['date']}")
        print(f"🏷️ 分类：{', '.join(p['categories'][:3])}")
        print(f"🔗 链接：{p['link']}")
        
        # 提取创新点
        work, innovation = extract_innovation(p['abstract'])
        
        print(f"\n🧠 【核心工作】")
        print(f"   {work[:250]}{'...' if len(work) > 250 else ''}")
        
        print(f"\n💡 【创新点】")
        print(f"   {innovation[:250]}{'...' if len(innovation) > 250 else ''}")
        
        # 下载PDF
        print(f"\n⬇️  PDF下载...")
        download_pdf(p['id'], p['title'], p['year'])
        
        print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n使用方法：")
        print("  python smart_search.py <关键词> [数量]")
        print("\n示例：")
        print("  python smart_search.py 'community detection' 8")
        sys.exit(1)
    
    keyword = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) >= 3 else 8
    
    papers = search_papers(keyword, max_results)
    
    if papers:
        display_results(papers)
        print(f"\n{'='*80}")
        print(f"✅ 搜索完成！共 {len(papers)} 篇论文")
        print(f"📂 PDF保存位置：{SAVE_DIR}")
        print(f"{'='*80}\n")
    else:
        print("\n❌ 未找到论文或搜索失败\n")
