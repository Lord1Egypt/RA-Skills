#!/usr/bin/env python3
"""
arXiv 论文搜索与 GitHub 代码验证脚本
支持从 arXiv 页面提取 GitHub 链接
"""

import urllib.request
import urllib.parse
import json
import re
import os
import html
from datetime import datetime, timedelta
from xml.etree import ElementTree as ET

# arXiv API namespace
ARXIV_NS = {'atom': 'http://www.w3.org/2005/Atom'}

# 主题关键词映射
TOPIC_QUERIES = {
    "agent-eval": "(agent OR LLM) AND (evaluation OR benchmark OR assessment)",
    "rag-eval": "(RAG OR \"retrieval augmented generation\") AND (evaluation OR benchmark)",
    "agent-arch": "(agent OR LLM) AND (architecture OR framework OR design) AND NOT evaluation",
    "rag-arch": "(RAG OR \"retrieval augmented generation\") AND (architecture OR framework OR system) AND NOT evaluation"
}

def search_arxiv(topic: str, max_results: int = 15) -> list:
    """搜索 arXiv 论文"""
    query = TOPIC_QUERIES.get(topic, topic)
    encoded_query = urllib.parse.quote(query)
    
    url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
    
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            xml_data = response.read()
    except Exception as e:
        print(f"Error fetching from arXiv: {e}")
        return []
    
    return parse_arxiv_response(xml_data)

def parse_arxiv_response(xml_data: bytes) -> list:
    """解析 arXiv API 响应"""
    root = ET.fromstring(xml_data)
    papers = []
    
    for entry in root.findall('atom:entry', ARXIV_NS):
        paper = {
            'id': entry.find('atom:id', ARXIV_NS).text.split('/')[-1],
            'title': entry.find('atom:title', ARXIV_NS).text.strip().replace('\n', ' '),
            'summary': entry.find('atom:summary', ARXIV_NS).text.strip().replace('\n', ' '),
            'published': entry.find('atom:published', ARXIV_NS).text[:10],
            'updated': entry.find('atom:updated', ARXIV_NS).text[:10],
            'authors': [a.find('atom:name', ARXIV_NS).text for a in entry.findall('atom:author', ARXIV_NS)],
            'link': entry.find('atom:id', ARXIV_NS).text,
            'pdf_link': None
        }
        
        # 找 PDF 链接
        for link in entry.findall('atom:link', ARXIV_NS):
            if link.get('title') == 'pdf':
                paper['pdf_link'] = link.get('href')
        
        papers.append(paper)
    
    return papers

def filter_recent_papers(papers: list, months: int = 6) -> list:
    """过滤最近 N 个月的论文"""
    cutoff = datetime.now() - timedelta(days=months * 30)
    return [p for p in papers if datetime.strptime(p['published'], '%Y-%m-%d') > cutoff]

def extract_github_url(text: str) -> str:
    """从文本中提取 GitHub URL"""
    patterns = [
        r'https?://github\.com/[\w\-]+/[\w\-\.]+',
        r'github\.com/[\w\-]+/[\w\-\.]+'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            url = match.group(0)
            if not url.startswith('http'):
                url = 'https://' + url
            # 清理 URL 尾部的标点
            url = re.sub(r'[.,;:)\]\s]+$', '', url)
            return url
    
    return None

def fetch_arxiv_page(arxiv_id: str) -> str:
    """获取 arXiv 论文页面 HTML"""
    url = f"https://arxiv.org/abs/{arxiv_id}"
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; arxiv-paper-recommender/1.0)'
        })
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching arXiv page: {e}")
        return ""

def extract_github_from_page(html_content: str) -> str:
    """从 arXiv 页面 HTML 中提取 GitHub 链接"""
    if not html_content:
        return None
    
    # 解码 HTML 实体
    html_content = html.unescape(html_content)
    
    # 常见模式
    patterns = [
        # 标准链接
        r'https?://github\.com/[\w\-]+/[\w\-\.]+',
        # 在 href 中
        r'href=["\']?(https?://github\.com/[\w\-]+/[\w\-\.]+)["\']?',
        # markdown 格式
        r'\[.*?\]\((https?://github\.com/[\w\-]+/[\w\-\.]+)\)',
    ]
    
    found_urls = set()
    
    for pattern in patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        for match in matches:
            # 如果是 tuple，取第一个
            url = match if isinstance(match, str) else match[0]
            # 清理
            url = re.sub(r'[.,;:)\]\s]+$', '', url)
            # 过滤无效的
            if '/issues/' in url or '/pull/' in url or '/wiki' in url:
                continue
            found_urls.add(url)
    
    # 优先返回最可能是主仓库的 URL（最短的）
    if found_urls:
        return min(found_urls, key=len)
    
    return None

def verify_github_repo(github_url: str) -> dict:
    """验证 GitHub 仓库信息"""
    # 提取 owner/repo
    match = re.search(r'github\.com/([\w\-]+)/([\w\-\.]+)', github_url)
    if not match:
        return None
    
    owner, repo = match.groups()
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    
    try:
        req = urllib.request.Request(api_url, headers={
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'arxiv-paper-recommender/1.0'
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
        
        return {
            'exists': True,
            'stars': data.get('stargazers_count', 0),
            'updated_at': data.get('updated_at', '')[:10],
            'language': data.get('language', 'Unknown'),
            'description': data.get('description', ''),
            'open_issues': data.get('open_issues_count', 0),
            'url': github_url,
            'owner': owner,
            'repo': repo
        }
    except Exception as e:
        return {'exists': False, 'error': str(e), 'url': github_url}

def find_github_for_paper(paper: dict) -> str:
    """为论文查找 GitHub 链接"""
    # 1. 先检查摘要
    github_url = extract_github_url(paper['summary'])
    
    if github_url:
        return github_url
    
    # 2. 访问 arXiv 页面
    print(f"  访问 arXiv 页面查找 GitHub...")
    html_content = fetch_arxiv_page(paper['id'])
    github_url = extract_github_from_page(html_content)
    
    return github_url

def find_papers_with_code(topic: str, max_results: int = 15) -> list:
    """查找有代码的论文"""
    print(f"正在搜索主题: {topic}")
    papers = search_arxiv(topic, max_results)
    print(f"找到 {len(papers)} 篇论文")
    
    # 过滤最近6个月
    recent_papers = filter_recent_papers(papers, months=6)
    print(f"最近6个月: {len(recent_papers)} 篇")
    
    results = []
    for i, paper in enumerate(recent_papers):
        print(f"\n[{i+1}/{len(recent_papers)}] {paper['title'][:50]}...")
        
        # 查找 GitHub 链接
        github_url = find_github_for_paper(paper)
        
        if github_url:
            print(f"  验证 GitHub: {github_url}")
            repo_info = verify_github_repo(github_url)
            
            if repo_info and repo_info.get('exists'):
                paper['github'] = repo_info
                results.append(paper)
                print(f"  ✅ 有效 (⭐ {repo_info['stars']})")
            else:
                print(f"  ❌ 仓库无效")
        else:
            print(f"  ⏭️ 未找到 GitHub 链接")
    
    # 按星数排序
    results.sort(key=lambda x: x['github']['stars'], reverse=True)
    
    return results

def main():
    import sys
    
    topic = sys.argv[1] if len(sys.argv) > 1 else "agent-eval"
    
    papers = find_papers_with_code(topic)
    
    print(f"\n{'='*60}")
    print(f"找到 {len(papers)} 篇有代码的论文:")
    print('='*60)
    
    for i, p in enumerate(papers[:5], 1):
        print(f"\n{i}. {p['title']}")
        print(f"   arXiv: {p['id']} | {p['published']}")
        print(f"   GitHub: {p['github']['url']} (⭐ {p['github']['stars']})")

if __name__ == '__main__':
    main()
