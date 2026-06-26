#!/usr/bin/env python3
# arXiv 每日论文精选 - Python 执行脚本 (v5 - 带机构数据库)

import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import re
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AFFILIATIONS_DB = os.path.join(SCRIPT_DIR, 'affiliations_db.json')
ARXIV_API = "http://export.arxiv.org/api/query"

SEARCH_CONFIGS = [
    {"query": "cat:cs.AI AND all:large language model", "label": "LLM", "max": 3},
    {"query": "cat:cs.CL AND all:retrieval augmented generation", "label": "RAG", "max": 2},
    {"query": "cat:cs.AI AND all:agent", "label": "Agent", "max": 3},
    {"query": "cat:cs.LG AND all:transformer", "label": "Transformer", "max": 2},
    {"query": "cat:cs.AI AND all:harness", "label": "Harness", "max": 2},
    {"query": "cat:cs.AI AND all:reasoning", "label": "Reasoning", "max": 2},
]

def load_affiliations_db():
    """加载机构数据库"""
    if os.path.exists(AFFILIATIONS_DB):
        try:
            with open(AFFILIATIONS_DB, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('affiliations', {})
        except:
            pass
    return {}

def save_affiliations_db(affiliations):
    """保存机构数据库"""
    data = {
        'description': 'arXiv 论文机构信息数据库（自动累积）',
        'updated': datetime.now().strftime('%Y-%m-%d'),
        'affiliations': affiliations
    }
    try:
        with open(AFFILIATIONS_DB, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 机构数据库已更新：{len(affiliations)} 条记录")
    except Exception as e:
        print(f"⚠️  保存机构数据库失败：{e}")

def fetch_papers(query, max_results=5):
    url = f"{ARXIV_API}?search_query={query.replace(' ', '+')}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"❌ 获取失败：{e}")
        return None

def parse_arxiv_xml(xml_content):
    papers = []
    ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
    
    try:
        root = ET.fromstring(xml_content)
        entries = root.findall('atom:entry', ns)
        
        for entry in entries:
            title_elem = entry.find('atom:title', ns)
            id_elem = entry.find('atom:id', ns)
            published_elem = entry.find('atom:published', ns)
            summary_elem = entry.find('atom:summary', ns)
            
            authors = []
            for author in entry.findall('atom:author', ns):
                name_elem = author.find('atom:name', ns)
                if name_elem is not None:
                    authors.append(name_elem.text)
            
            categories = []
            for cat in entry.findall('atom:category', ns):
                term = cat.get('term')
                if term:
                    categories.append(term)
            
            if title_elem is not None and id_elem is not None:
                papers.append({
                    'title': ' '.join(title_elem.text.split()),
                    'id': id_elem.text,
                    'arxiv_id': id_elem.text.split('/')[-1],
                    'published': published_elem.text[:10] if published_elem is not None else 'Unknown',
                    'summary': ' '.join(summary_elem.text.split()) if summary_elem is not None else '',
                    'authors': authors,
                    'categories': categories,
                })
    except Exception as e:
        print(f"❌ 解析失败：{e}")
    
    return papers

def extract_affiliations_from_html(arxiv_id):
    """从 arXiv HTML 页面提取机构信息"""
    try:
        url = f"https://arxiv.org/abs/{arxiv_id}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        affiliations = []
        top_institutions = {
            'Tsinghua': 'Tsinghua University', 'Peking': 'Peking University',
            'Shanghai Jiao Tong': 'Shanghai Jiao Tong University', 'Zhejiang': 'Zhejiang University',
            'Stanford': 'Stanford University', 'MIT': 'Massachusetts Institute of Technology',
            'Berkeley': 'UC Berkeley', 'Carnegie Mellon': 'Carnegie Mellon University',
            'Harvard': 'Harvard University', 'Google': 'Google Research',
            'Microsoft': 'Microsoft Research', 'Meta': 'Meta AI', 'OpenAI': 'OpenAI',
            'Anthropic': 'Anthropic', 'DeepMind': 'DeepMind',
            'Huawei': 'Huawei Technologies Co., Ltd.', 'Tencent': 'Tencent',
            'Alibaba': 'Alibaba', 'Baidu': 'Baidu', 'ByteDance': 'ByteDance',
            'Intel': 'Intel AI', 'Amazon': 'Amazon', 'Apple': 'Apple ML',
            'University of Michigan': 'University of Michigan', 'Rice': 'Rice University',
            'USC': 'University of Southern California',
        }
        
        for keyword, full_name in top_institutions.items():
            if keyword.lower() in html.lower():
                if full_name not in affiliations:
                    affiliations.append(full_name)
        
        # 查找 GitHub 仓库
        github_match = re.search(r'github\.com/([^/\s"]+/[^/\s"]+)', html)
        if github_match:
            repo = github_match.group(1).lower()
            if 'thunlp' in repo and 'Tsinghua University' not in affiliations:
                affiliations.insert(0, 'Tsinghua University')
        
        return affiliations[:3]
    except:
        return []

def get_affiliations(arxiv_id, db=None, auto_fetch=True):
    """获取论文机构信息"""
    if db is None:
        db = load_affiliations_db()
    
    base_id = arxiv_id.split('v')[0]
    
    # 尝试数据库匹配
    if base_id in db:
        return db[base_id]
    
    for known_id, affils in db.items():
        if base_id.startswith(known_id) or known_id.startswith(base_id):
            return affils
    
    # 自动从 HTML 提取
    if auto_fetch:
        affils = extract_affiliations_from_html(base_id)
        if affils:
            # 保存到数据库
            db[base_id] = affils
            save_affiliations_db(db)
            return affils
    
    return []

def filter_recent_papers(papers, days=3):
    cutoff = datetime.now() - timedelta(days=days)
    recent = []
    for paper in papers:
        try:
            pub_date = datetime.strptime(paper['published'], '%Y-%m-%d')
            if pub_date >= cutoff:
                recent.append(paper)
        except:
            recent.append(paper)
    return recent

def analyze_paper_simple(paper):
    summary = paper['summary']
    analysis = {'problem': '', 'innovation': '', 'importance': '', 'limitation': ''}
    
    innovation_patterns = [r'we propose (.*?)\.', r'we introduce (.*?)\.', r'we present (.*?)\.']
    for pattern in innovation_patterns:
        match = re.search(pattern, summary, re.IGNORECASE)
        if match:
            analysis['innovation'] = match.group(0)[:200]
            break
    
    if not analysis['problem']:
        analysis['problem'] = f"论文针对 {paper['categories'][0] if paper['categories'] else '相关领域'} 中的问题提出改进方案"
    if not analysis['innovation']:
        analysis['innovation'] = "提出了新的方法/框架/模型"
    analysis['importance'] = f"对 {paper['categories'][0] if paper['categories'] else '相关'} 研究有参考价值"
    analysis['limitation'] = "需要进一步实验验证效果"
    
    return analysis

def format_output(papers, detailed=False, db=None):
    output = []
    date_str = datetime.now().strftime('%Y-%m-%d')
    output.append(f"# 📚 今日 ArXiv 论文推送 ({date_str})")
    output.append("")
    
    output.append("## 📋 目录")
    for i, paper in enumerate(papers[:10], 1):
        output.append(f"{i}. {paper['title']}")
    output.append("")
    output.append("---")
    output.append("")
    
    if detailed:
        output.append("## 📖 论文详解")
        output.append("")
        
        for i, paper in enumerate(papers[:5], 1):
            analysis = analyze_paper_simple(paper)
            affils = get_affiliations(paper['arxiv_id'], db=db, auto_fetch=True)
            affil_str = " | " + " + ".join(affils) if affils else ""
            
            output.append(f"### {i}. {paper['title']}")
            output.append(f"**arXiv**: {paper['arxiv_id']} | {paper['published']}{affil_str}")
            output.append(f"**作者**: {', '.join(paper['authors'][:3])}{' et al.' if len(paper['authors']) > 3 else ''}")
            output.append(f"**链接**: {paper['id']}")
            output.append("")
            output.append("**中文摘要**:")
            summary_short = paper['summary'][:400]
            output.append(f"> {summary_short}...")
            output.append("")
            output.append("**解决的问题**:")
            output.append(f"- {analysis['problem']}")
            output.append("")
            output.append("**核心创新**:")
            output.append(f"- {analysis['innovation']}")
            output.append("")
            output.append("**为什么重要**:")
            output.append(f"- {analysis['importance']}")
            output.append("")
            output.append("**局限性**:")
            output.append(f"- {analysis['limitation']}")
            output.append("")
            output.append("---")
            output.append("")
    
    return '\n'.join(output)

def main():
    print("🔍 开始搜集 arXiv 最新论文...\n")
    
    all_papers = []
    seen_ids = set()
    
    for config in SEARCH_CONFIGS:
        print(f"搜索 [{config['label']}]: {config['query'][:50]}...")
        xml = fetch_papers(config['query'], config['max'])
        
        if xml:
            papers = parse_arxiv_xml(xml)
            for paper in papers:
                if paper['arxiv_id'] not in seen_ids:
                    seen_ids.add(paper['arxiv_id'])
                    all_papers.append(paper)
    
    print(f"\n✅ 共获取 {len(all_papers)} 篇论文（去重后）")
    
    recent_papers = filter_recent_papers(all_papers, days=3)
    print(f"📅 最近 3 天内：{len(recent_papers)} 篇")
    
    # 加载机构数据库
    db = load_affiliations_db()
    print(f"📚 机构数据库：{len(db)} 条记录")
    
    if recent_papers:
        print("\n" + "="*60)
        print(format_output(recent_papers, detailed=True, db=db))
    else:
        print("\n⚠️  最近 3 天内没有找到相关论文")
        print(format_output(all_papers[:5], detailed=True, db=db))

if __name__ == "__main__":
    main()
