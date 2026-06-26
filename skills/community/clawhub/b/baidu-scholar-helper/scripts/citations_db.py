#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学术论文搜索工具 - 带引用量数据库
功能：
- 搜索arXiv论文
- 使用本地引用量数据库（经典论文）
- 按引用量排序
- 提取核心工作和创新点
- 自动下载PDF
- 提供引用量查询链接
"""

import os
import re
import sys
import time
import requests
import xml.etree.ElementTree as ET

# 配置
SAVE_DIR = os.path.expanduser("~/Desktop/papers/社区检测")
os.makedirs(SAVE_DIR, exist_ok=True)

# 经典论文引用量数据库（手动维护，数据来自Google Scholar）
KNOWN_CITATIONS = {
    # 社区检测经典论文
    "fast unfolding of communities in large networks": 18500,
    "finding and evaluating community structure in networks": 28000,
    "community detection in graphs": 12000,
    "community detection in networks: algorithms, complexity, and information limits": 3500,
    "from louvain to leiden: guaranteeing well-connected communities": 4200,
    "detecting community structure in networks": 15000,
    "near linear time algorithm to detect community structures": 6500,
    "stochastic block models and community structure in networks": 4500,
    "overlapping community detection in networks": 5500,
    "community detection in networks: a user guide": 8000,
    "deep learning for community detection": 1800,

    # Transformer相关
    "attention is all you need": 95000,
    "bert: pre-training of deep bidirectional transformers": 75000,

    # 其他常见论文
    "deep learning": 120000,
    "imagenet classification with deep convolutional neural networks": 110000,
}

ARXIV_API = "http://export.arxiv.org/api/query"

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
        'ccs',  # arXiv分类中的会议标识
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

def clean_filename(title):
    """清理文件名"""
    return re.sub(r'[\\/*?:"<>|]', "", title)[:80]

def get_citations_from_database(title):
    """从本地数据库查找引用量"""
    title_lower = title.lower()

    # 精确匹配
    for key, citations in KNOWN_CITATIONS.items():
        if key in title_lower or title_lower in key:
            return citations, True

    # 部分匹配
    words = title_lower.split()
    if len(words) >= 3:
        for key, citations in KNOWN_CITATIONS.items():
            key_words = set(key.split())
            title_words = set(words)
            # 至少3个关键词匹配
            if len(key_words & title_words) >= 3:
                return citations, True

    return 0, False

def get_citation_links(title, authors):
    """生成引用量查询链接"""
    # 编码标题
    query = title.replace(' ', '+')

    links = {
        'Google Scholar': f'https://scholar.google.com/scholar?q={query}',
        'Semantic Scholar': f'https://www.semanticscholar.org/search?q={query}',
        '百度学术': f'https://xueshu.baidu.com/s?wd={query}'
    }

    return links

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

        print(f"✅ 找到 {len(entries)} 篇论文")
        print(f"📊 正在查询引用量...\n")

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

            # 获取引用量
            citations, matched = get_citations_from_database(title)
            citation_links = get_citation_links(title, authors)

            if matched:
                print(f"  [{idx}/{len(entries)}] ✅ {title[:50]}... (引用量: {citations})")
            else:
                print(f"  [{idx}/{len(entries)}] 📊 {title[:50]}... (需手动查询)")

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
                "citations": citations,
                "citation_matched": matched,
                "citation_links": citation_links
            })

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
                               'develop', 'design', 'create', 'build', 'offer']

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

def download_pdf(arxiv_id, title, year, categories=None):
    """下载PDF"""
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

    try:
        time.sleep(0.3)

        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(pdf_url, headers=headers, timeout=60, stream=True)

        if resp.status_code == 200:
            # 判断论文类型（期刊J或会议C）
            paper_type = get_paper_type_from_categories(categories)
            
            # 命名格式：标题_年份_J.pdf 或 标题_年份_C.pdf
            filename = f"{clean_filename(title)}_{year}_{paper_type}.pdf"
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
        if p['citation_matched']:
            citation_str = f"⭐{p['citations']}"
        else:
            citation_str = "📊待查询"

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

        # 如果没有匹配到引用量，提供查询链接
        if not p['citation_matched']:
            print(f"\n📊 【引用量查询】")
            print(f"   Google: {p['citation_links']['Google Scholar'][:60]}...")
            print(f"   Semantic: {p['citation_links']['Semantic Scholar'][:60]}...")

        # 下载PDF
        if download:
            print(f"\n⬇️  PDF下载...")
            pdf_name = download_pdf(p['id'], p['title'], p['year'], p.get('categories'))
            if pdf_name:
                print(f"    ✅ 已下载: {pdf_name}")
            else:
                print(f"    📥 手动下载: {p['pdf']}")

        print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n使用方法：")
        print("  python citations_db.py <关键词> [数量]")
        print("\n示例：")
        print("  python citations_db.py 'community detection' 10")
        print("\n功能：")
        print("  - 搜索arXiv论文")
        print("  - 本地引用量数据库匹配")
        print("  - 按引用量排序")
        print("  - 提供引用量查询链接")
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
        matched_papers = [p for p in papers if p['citation_matched']]
        if matched_papers:
            total_citations = sum(p['citations'] for p in matched_papers)
            avg_citations = total_citations // len(matched_papers)
            max_citations = max(p['citations'] for p in matched_papers)

            print(f"\n📊 引用量统计（已匹配 {len(matched_papers)} 篇）：")
            print(f"   总引用量：{total_citations}")
            print(f"   平均引用量：{avg_citations}")
            print(f"   最高引用量：{max_citations}")

        print(f"{'='*80}\n")
    else:
        print("\n❌ 未找到论文或搜索失败\n")
