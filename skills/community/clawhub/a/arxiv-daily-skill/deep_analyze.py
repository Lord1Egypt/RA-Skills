#!/usr/bin/env python3
"""
arXiv 论文深度分析工具
支持对单篇论文进行详细解读（调用 ljg-paper skill 的逻辑）
"""

import sys
import urllib.request
import re

def fetch_paper_full_info(arxiv_id):
    """获取论文完整信息"""
    try:
        # 获取 arXiv 页面
        url = f"https://arxiv.org/abs/{arxiv_id}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        # 提取标题
        title_match = re.search(r'<h1 class="title[^>]*>([^<]+)</h1>', html)
        title = title_match.group(1).strip() if title_match else "Unknown"
        
        # 提取作者
        authors_match = re.search(r'Authors:(.+?)(?:<br|$)', html, re.DOTALL)
        authors = authors_match.group(1).strip() if authors_match else "Unknown"
        authors = re.sub(r'<[^>]+>', ' ', authors)
        authors = re.sub(r'\s+', ' ', authors).strip()
        
        # 提取摘要
        abstract_match = re.search(r'<blockquote class="abstract[^>]*>(.+?)</blockquote>', html, re.DOTALL)
        abstract = abstract_match.group(1) if abstract_match else ""
        abstract = re.sub(r'<[^>]+>', ' ', abstract)
        abstract = re.sub(r'\s+', ' ', abstract).strip()
        
        # 提取机构（从 HTML 中查找）
        institutions = []
        inst_keywords = ['University', 'Institute', 'Laboratory', 'Google', 'Microsoft', 'Meta', 'OpenAI', 'Huawei', 'Tencent', 'Alibaba']
        for kw in inst_keywords:
            if kw.lower() in html.lower():
                institutions.append(kw)
        
        return {
            'arxiv_id': arxiv_id,
            'title': title,
            'authors': authors,
            'abstract': abstract,
            'institutions': institutions[:3],
            'url': url
        }
    except Exception as e:
        return {'error': str(e)}

def generate_deep_analysis(paper):
    """生成深度分析报告"""
    if 'error' in paper:
        return f"❌ 获取论文信息失败：{paper['error']}"
    
    report = []
    report.append(f"# 📖 论文深度分析")
    report.append("")
    report.append(f"## {paper['title']}")
    report.append("")
    report.append(f"**arXiv**: [{paper['arxiv_id']}](https://arxiv.org/abs/{paper['arxiv_id']})")
    if paper['institutions']:
        report.append(f"**机构**: {' + '.join(paper['institutions'])}")
    report.append(f"**作者**: {paper['authors']}")
    report.append("")
    report.append("---")
    report.append("")
    
    report.append("## 📝 摘要")
    report.append("")
    report.append(paper['abstract'][:1000] + ("..." if len(paper['abstract']) > 1000 else ""))
    report.append("")
    
    report.append("## 💡 核心思想（大白话版）")
    report.append("")
    report.append("> 这部分需要调用 ljg-paper skill 进行深度解读...")
    report.append("")
    
    report.append("## 🔧 技术细节")
    report.append("")
    report.append("### 解决的问题")
    report.append("- （待分析）")
    report.append("")
    report.append("### 核心方法")
    report.append("- （待分析）")
    report.append("")
    report.append("### 创新点")
    report.append("- （待分析）")
    report.append("")
    
    report.append("## 📊 实验结果")
    report.append("")
    report.append("- （待分析）")
    report.append("")
    
    report.append("## 🤔 局限性与未来方向")
    report.append("")
    report.append("- （待分析）")
    report.append("")
    
    report.append("---")
    report.append("")
    report.append("💡 **提示**: 如需更详细的中文解读，请说：`用 ljg-paper 分析这篇论文`")
    
    return '\n'.join(report)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 deep_analyze.py <arxiv_id>")
        print("示例：python3 deep_analyze.py 2604.13016")
        sys.exit(1)
    
    arxiv_id = sys.argv[1].replace('arxiv:', '').replace('https://arxiv.org/abs/', '').split('/')[-1]
    
    print(f"🔍 获取论文信息：{arxiv_id}...\n")
    paper = fetch_paper_full_info(arxiv_id)
    
    if 'error' in paper:
        print(f"❌ 失败：{paper['error']}")
    else:
        print(generate_deep_analysis(paper))
