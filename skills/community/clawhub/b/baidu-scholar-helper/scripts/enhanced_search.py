#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版学术论文搜索工具 - 带引用量功能
功能：
- 搜索arXiv论文
- 获取Semantic Scholar引用量
- 按引用量排序
- 提取核心工作和创新点
- 自动下载PDF
"""

import os
import re
import sys
import time
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote

# 配置
SAVE_DIR = os.path.expanduser("~/Desktop/papers/社区检测")
os.makedirs(SAVE_DIR, exist_ok=True)

# API端点
ARXIV_API = "http://export.arxiv.org/api/query"
SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"

def clean_filename(title):
    """清理文件名"""
    return re.sub(r'[\\/*?:"<>|]', "", title)[:80]

def get_paper_type_from_categories(categories):
    """根据arXiv分类判断论文类型（期刊J或会议C）"""
    if not categories:
        return "J"  # 默认期刊
    
    # 会议相关的分类或关键词
    conf_indicators = [
        'CVPR', 'ICCV', 'ECCV',  # 计算机视觉
        'NeurIPS', 'ICML', 'ICLR', 'AAAI', 'IJCAI',  # 机器学习
        'ACL', 'EMNLP', 'NAACL', 'COLING',  # 自然语言处理
        'KDD', 'WWW', 'SIGIR', 'WSDM', 'CIKM',  # 数据挖掘
        'SIGGRAPH', 'SIGMOD', 'VLDB',  # 图形/数据库
        'INFOCOM', 'SIGCOMM', 'MOBICOM',  # 网络
    ]
    
    # 检查分类中是否包含会议关键词
    for cat in categories:
        cat_upper = cat.upper()
        for indicator in conf_indicators:
            if indicator.upper() in cat_upper:
                return "C"
    
    # 如果分类中包含这些关键词，也可能是会议
    conf_keywords = ['conference', 'symposium', 'workshop', 'proceedings']
    for cat in categories:
        cat_lower = cat.lower()
        if any(kw in cat_lower for kw in conf_keywords):
            return "C"
    
    return "J"  # 默认期刊

def get_citations_from_semantic_scholar(title, authors=None):
    """从Semantic Scholar获取引用量"""
    try:
        # 构建查询
        query = title
        
        params = {
            "query": query,
            "limit": 1,
            "fields": "title,year,citationCount,authors,url"
        }
        
        headers = {"User-Agent": "OpenClaw-Scholar-Bot/1.0"}
        
        resp = requests.get(SEMANTIC_SCHOLAR_API, params=params, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            if data.get('data') and len(data['data']) > 0:
                paper = data['data'][0]
                # 验证标题匹配度
                found_title = paper.get('title', '').lower()
                query_title = title.lower()
                
                # 简单的标题匹配检查
                if any(word in found_title for word in query_title.split()[:3]):
                    return {
                        'citations': paper.get('citationCount', 0),
                        'year': paper.get('year'),
                        'url': paper.get('url'),
                        'matched': True
                    }
        
        return {'citations': 0, 'matched': False}
        
    except Exception as e:
        print(f"    ⚠️  获取引用量失败: {e}")
        return {'citations': 0, 'matched': False}

def search_arxiv(keyword, max_results=10):
    """搜索arXiv"""
    print(f"\n{'='*80}")
    print(f"🔍 arXiv搜索：{keyword}")
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
        print("📊 正在获取引用量数据...\n")
        
        papers = []
        for idx, entry in enumerate(entries, 1):
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
            
            print(f"  [{idx}/{len(entries)}] 获取: {title[:50]}...")
            
            # 获取引用量
            citation_data = get_citations_from_semantic_scholar(title, authors)
            
            papers.append({
                "id": arxiv_id,
                "title": title,
                "authors": authors,
                "abstract": abstract_text,
                "year": year,
                "date": pub_date,
                "categories": categories,
                "link": f"https://arxiv.org/abs/{arxiv_id}",
                "pdf": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                "citations": citation_data.get('citations', 0),
                "citation_matched": citation_data.get('matched', False)
            })
            
            # API速率限制
            time.sleep(0.5)
        
        # 按引用量排序（从高到低）
        papers = sorted(papers, key=lambda x: x['citations'], reverse=True)
        
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
                               'improve', 'achieve', 'demonstrate', 'show', 'outperform',
                               'develop', 'design', 'create', 'build']
        
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
                return filename
            else:
                os.remove(path)
        
        return None
        
    except Exception as e:
        return None

def display_results(papers, download=True):
    """显示结果"""
    for idx, p in enumerate(papers, 1):
        print(f"{'━'*80}")
        
        # 引用量显示
        citation_str = f"⭐{p['citations']}" if p['citations'] > 0 else "N/A"
        print(f"📄 【论文 {idx}】引用量：{citation_str}")
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
        print(f"   {work[:280]}{'...' if len(work) > 280 else ''}")
        
        print(f"\n💡 【创新点】")
        print(f"   {innovation[:280]}{'...' if len(innovation) > 280 else ''}")
        
        # 下载PDF
        if download:
            print(f"\n⬇️  PDF下载...")
            pdf_name = download_pdf(p['id'], p['title'], p['year'])
            if pdf_name:
                print(f"    ✅ 已下载: {pdf_name}")
            else:
                print(f"    📥 手动下载: {p['pdf']}")
        
        print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n使用方法：")
        print("  python enhanced_search.py <关键词> [数量]")
        print("\n示例：")
        print("  python enhanced_search.py 'community detection' 10")
        print("\n功能：")
        print("  - 搜索arXiv论文")
        print("  - 获取Semantic Scholar引用量")
        print("  - 按引用量排序")
        print("  - 提取核心工作和创新点")
        print("  - 自动下载PDF")
        sys.exit(1)
    
    keyword = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) >= 3 else 10
    
    papers = search_arxiv(keyword, max_results)
    
    if papers:
        display_results(papers, download=True)
        
        print(f"\n{'='*80}")
        print(f"✅ 搜索完成！共 {len(papers)} 篇论文（按引用量排序）")
        print(f"📂 PDF保存位置：{SAVE_DIR}")
        
        # 显示引用量统计
        total_citations = sum(p['citations'] for p in papers)
        avg_citations = total_citations // len(papers) if papers else 0
        max_citations = max(p['citations'] for p in papers) if papers else 0
        
        print(f"\n📊 引用量统计：")
        print(f"   总引用量：{total_citations}")
        print(f"   平均引用量：{avg_citations}")
        print(f"   最高引用量：{max_citations}")
        
        print(f"{'='*80}\n")
    else:
        print("\n❌ 未找到论文或搜索失败\n")
