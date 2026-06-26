#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arXiv科研助手 V4.0
功能：搜索arXiv、PDF自动下载、工作总结+创新点、模型图显示
新增：按论文方向创建文件夹、规范命名、桌面papers目录
"""

import os
import re
import sys
import time
import random
import requests
import xml.etree.ElementTree as ET

# ========== 配置 ==========
# 桌面papers目录
DESKTOP_DIR = os.path.expanduser("~/Desktop/papers")
os.makedirs(DESKTOP_DIR, exist_ok=True)

# 固定User-Agent
DEFAULT_UA = "OpenClaw-Scholar-Bot/1.0 (Educational Research)"

# arXiv API配置
ARXIV_API_URL = "https://export.arxiv.org/api/query"
MAX_RETRIES = 3
RETRY_DELAY = 30  # 增加到30秒避免限流
API_TIMEOUT = 60
PDF_TIMEOUT = 120

def clean_filename(title):
    """清理文件名，移除非法字符"""
    title = re.sub(r'[\\/*?:"<>|]', "", title)
    title = title.replace('\n', ' ').strip()
    return title[:80]

def api_request_with_retry(params, max_retries=MAX_RETRIES):
    """带重试的API请求"""
    headers = {"User-Agent": DEFAULT_UA}
    
    for attempt in range(max_retries):
        try:
            print(f"📡 请求arXiv API (第{attempt+1}次)...")
            resp = requests.get(ARXIV_API_URL, params=params, headers=headers, timeout=API_TIMEOUT)
            
            if resp.status_code == 200:
                return resp
            elif resp.status_code == 429:
                wait_time = RETRY_DELAY * (attempt + 2)
                print(f"⚠️  API速率限制，等待 {wait_time} 秒...")
                time.sleep(wait_time)
            else:
                print(f"⚠️  状态码: {resp.status_code}")
                time.sleep(RETRY_DELAY)
                
        except requests.exceptions.Timeout:
            print(f"⚠️  请求超时，重试中...")
            time.sleep(RETRY_DELAY)
        except requests.exceptions.ConnectionError as e:
            print(f"⚠️  连接错误，重试中...")
            time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"⚠️  错误: {e}")
            time.sleep(RETRY_DELAY)
    
    return None

def get_paper_type_from_categories(categories):
    """根据arXiv分类判断论文类型"""
    if not categories:
        return "J"
    
    # 会议相关的分类
    conf_indicators = ['CVPR', 'ICCV', 'NeurIPS', 'ICML', 'ACL', 'EMNLP', 'AAAI', 'IJCAI', 
                       'ICLR', 'KDD', 'WWW', 'SIGIR', 'SIGGRAPH', 'ECCV']
    
    for cat in categories:
        cat_upper = cat.upper()
        for indicator in conf_indicators:
            if indicator in cat_upper:
                return "C"
    
    # 默认为期刊/预印本
    return "J"

def download_arxiv_pdf(arxiv_id, title, year, save_dir, paper_type="J"):
    """下载arXiv PDF到指定目录"""
    try:
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        print(f"    ⬇️  下载: {arxiv_id}")
        
        headers = {
            "User-Agent": DEFAULT_UA,
            "Accept": "application/pdf,*/*"
        }
        
        time.sleep(random.uniform(0.5, 1.5))
        
        resp = requests.get(pdf_url, headers=headers, timeout=PDF_TIMEOUT, stream=True)
        
        if resp.status_code == 200:
            filename = f"{clean_filename(title)}_{year}_{paper_type}.pdf"
            path = os.path.join(save_dir, filename)
            
            # 检查是否已存在
            if os.path.exists(path) and os.path.getsize(path) > 10000:
                print(f"    ✅ 已存在: {filename}")
                return filename
            
            with open(path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            file_size = os.path.getsize(path)
            if file_size > 10000:
                print(f"    ✅ 下载成功: {filename} ({file_size//1024}KB)")
                return filename
            else:
                os.remove(path)
                print(f"    ⚠️  文件太小")
        else:
            print(f"    ⚠️  状态码: {resp.status_code}")
            
    except requests.exceptions.Timeout:
        print(f"    ⚠️  下载超时")
    except Exception as e:
        print(f"    ❌ 下载出错: {e}")
    
    return None

def extract_work_and_innovation(abstract):
    """从摘要提取核心工作和创新点"""
    if not abstract:
        return "（需查看原文）", "（需查看原文）"
    
    abstract = abstract.replace('\n', ' ').strip()
    
    sentences = re.split(r'(?<=[.!?])\s+', abstract)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
    
    if len(sentences) >= 3:
        work = " ".join(sentences[:2])
        innovation = " ".join(sentences[-2:]) if len(sentences) > 2 else sentences[-1]
        
        # 查找包含关键词的句子作为创新点
        for s in reversed(sentences):
            if any(kw in s.lower() for kw in ['contribution', 'novel', 'propose', 'innovative', 'new method', 'first']):
                innovation = s
                break
    elif len(sentences) >= 2:
        work = sentences[0]
        innovation = sentences[-1]
    else:
        work = abstract[:200] + "..." if len(abstract) > 200 else abstract
        innovation = work
    
    return work[:200], innovation[:200]

def extract_paper_categories(categories):
    """转换arXiv分类为可读名称"""
    category_names = {
        'cs.AI': '人工智能',
        'cs.CL': '计算语言学',
        'cs.CV': '计算机视觉',
        'cs.LG': '机器学习',
        'cs.NE': '神经网络',
        'cs.RO': '机器人',
        'cs.SE': '软件工程',
        'cs.IR': '信息检索',
        'cs.HC': '人机交互',
        'math.ST': '统计',
        'stat.ML': '统计机器学习',
        'physics.comp-ph': '计算物理',
        'q-bio': '定量生物学',
        'econ.GN': '经济学',
    }
    
    result = []
    for cat in categories[:3]:
        if cat in category_names:
            result.append(category_names[cat])
        else:
            # 提取主分类
            main = cat.split('.')[0] if '.' in cat else cat
            result.append(main.upper())
    
    return ', '.join(result)

def search_arxiv(keyword, max_results=10):
    """搜索arXiv论文"""
    print(f"\n{'='*70}")
    print(f"🔍 arXiv 搜索: {keyword}")
    print(f"{'='*70}\n")
    
    # 构建API请求参数
    params = {
        "search_query": f"all:{keyword}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }
    
    # 发送请求
    resp = api_request_with_retry(params)
    
    if not resp:
        print("❌ API请求失败，请稍后重试")
        return []
    
    # 解析XML
    try:
        root = ET.fromstring(resp.content)
    except ET.ParseError as e:
        print(f"❌ XML解析错误: {e}")
        return []
    
    # 命名空间
    ns = {
        'atom': 'http://www.w3.org/2005/Atom',
        'arxiv': 'http://arxiv.org/schemas/atom'
    }
    
    entries = root.findall('atom:entry', ns)
    
    if not entries:
        print("❌ 未找到相关论文")
        return []
    
    print(f"📊 找到 {len(entries)} 篇论文\n")
    
    papers = []
    
    for entry in entries:
        try:
            # 标题
            title_elem = entry.find('atom:title', ns)
            title = title_elem.text.strip().replace('\n', ' ') if title_elem is not None else "未知标题"
            
            # arXiv ID
            id_elem = entry.find('atom:id', ns)
            arxiv_url = id_elem.text if id_elem is not None else ""
            arxiv_id = arxiv_url.split("/")[-1]
            
            # 作者
            authors = []
            for author in entry.findall('atom:author', ns):
                name = author.find('atom:name', ns)
                if name is not None:
                    authors.append(name.text)
            
            # 摘要
            abstract_elem = entry.find('atom:summary', ns)
            abstract = abstract_elem.text.strip() if abstract_elem is not None else None
            
            # 发布日期
            published = entry.find('atom:published', ns)
            pub_date = published.text[:10] if published is not None else "未知日期"
            year = pub_date[:4] if pub_date else "unknown"
            
            # 分类
            categories = []
            for cat in entry.findall('atom:category', ns):
                term = cat.get('term')
                if term:
                    categories.append(term)
            
            # 尝试获取引用量（arXiv没有直接提供，用相关度代替排序）
            papers.append({
                "id": arxiv_id,
                "title": title,
                "authors": authors,
                "abstract": abstract,
                "date": pub_date,
                "year": year,
                "categories": categories,
                "link": f"https://arxiv.org/abs/{arxiv_id}",
                "pdf": f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            })
            
        except Exception as e:
            print(f"⚠️  解析论文失败: {e}")
            continue
    
    # 创建保存目录（以关键词命名）
    folder_name = clean_filename(keyword)
    save_dir = os.path.join(DESKTOP_DIR, folder_name)
    os.makedirs(save_dir, exist_ok=True)
    print(f"📂 PDF保存目录：{save_dir}\n")
    
    # 输出结果
    print(f"{'='*70}")
    print(f"📚 arXiv 搜索结果（共{len(papers)}篇）")
    print(f"{'='*70}\n")
    
    downloaded_count = 0
    
    for idx, p in enumerate(papers):
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"📄 【{idx+1}】ID: {p['id']}")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"📌 标题：{p['title']}")
        
        # 作者（只显示前3位）
        author_str = ', '.join(p['authors'][:3])
        if len(p['authors']) > 3:
            author_str += f" 等{len(p['authors'])}位"
        print(f"👥 作者：{author_str}")
        
        # 分类
        cat_str = extract_paper_categories(p['categories'])
        print(f"🏷️ 分类：{cat_str}")
        print(f"📅 发布：{p['date']}")
        print(f"🔗 链接：{p['link']}")
        
        # 分析摘要
        if p['abstract']:
            work, innovation = extract_work_and_innovation(p['abstract'])
            print(f"\n🧠 【核心工作】")
            print(f"   {work}")
            print(f"\n💡 【创新点】")
            print(f"   {innovation}")
        
        # 下载PDF
        print(f"\n⬇️  下载PDF...")
        paper_type = get_paper_type_from_categories(p['categories'])
        pdf_name = download_arxiv_pdf(p['id'], p['title'], p['year'], save_dir, paper_type)
        if pdf_name:
            downloaded_count += 1
        else:
            print(f"📥 手动下载：{p['pdf']}")
        
        print()
    
    # 汇总
    print(f"\n{'='*70}")
    print(f"✅ 完成！共处理 {len(papers)} 篇论文，下载 {downloaded_count} 篇PDF")
    print(f"📂 PDF保存位置: {save_dir}")
    print(f"{'='*70}\n")
    
    return papers


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
╔══════════════════════════════════════════════════════════════════╗
║           arXiv 科研助手 V4.0                                     ║
╚══════════════════════════════════════════════════════════════════╝

使用方法：
  python arxiv_search_v2.py <关键词> [数量]

示例：
  python arxiv_search_v2.py transformer
  python arxiv_search_v2.py "deep learning" 5
  python arxiv_search_v2.py GPT 10

功能：
  ✅ 按相关度排序
  ✅ 自动提取核心工作和创新点
  ✅ 显示arXiv分类
  ✅ 自动下载PDF到 ~/Desktop/papers/<关键词>/
  ✅ PDF命名：标题_年份_arXiv.pdf
""")
        sys.exit(1)
    
    keyword = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) >= 3 else 10
    
    search_arxiv(keyword, max_results)
