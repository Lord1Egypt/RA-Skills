#!/usr/bin/env python3
"""
引用格式化工具：将论文元数据转换为各种引用格式
支持格式：BibTeX / GB/T 7714 / APA
"""

import json
import re
import sys
import argparse
from typing import Dict, List, Optional
from datetime import datetime


class CitationFormatter:
    """引用格式化基类"""
    
    def __init__(self, papers: List[Dict]):
        self.papers = papers
        self.citation_key_map = {}  # 用于去重 key
    
    def format_all(self) -> str:
        """格式化所有论文"""
        raise NotImplementedError
    
    def _generate_key(self, paper: Dict) -> str:
        """生成唯一引用 key"""
        # 使用作者姓氏 + 年份
        authors = paper.get('authors', [])
        year = str(paper.get('year', 'unknown'))
        
        if authors:
            # 取第一作者的姓氏
            first_author = authors[0]
            last_name = first_author.split()[-1] if isinstance(first_author, str) else first_author.get('name', '').split()[-1]
            last_name = re.sub(r'[^a-zA-Z]', '', last_name).lower()
            
            key = f"{last_name}{year}"
            
            # 处理重复 key
            base_key = key
            counter = 1
            while key in self.citation_key_map.values():
                key = f"{base_key}{counter}"
                counter += 1
            
            self.citation_key_map[paper.get('doi') or paper.get('arxiv_id')] = key
            return key
        
        return f"paper{year}"
    
    def _format_authors(self, authors: List, style: str = 'full') -> str:
        """格式化作者列表"""
        if not authors:
            return "Unknown"
        
        if style == 'bibtex':
            # BibTeX: Author1 and Author2 and Author3
            formatted = []
            for author in authors:
                if isinstance(author, dict):
                    name = author.get('name', '')
                else:
                    name = str(author)
                formatted.append(name)
            return ' and '.join(formatted)
        
        elif style == 'gb7714':
            # GB/T 7714: Author A, Author B, Author C
            formatted = []
            for author in authors[:3]:  # 最多显示3个作者
                if isinstance(author, dict):
                    name = author.get('name', '')
                else:
                    name = str(author)
                # 简化为 A. Author 格式
                parts = name.split()
                if len(parts) >= 2:
                    last = parts[-1]
                    initials = ''.join([p[0] for p in parts[:-1]])
                    formatted.append(f"{initials}. {last}")
                else:
                    formatted.append(name)
            
            if len(authors) > 3:
                formatted.append("et al.")
            
            return ', '.join(formatted)
        
        elif style == 'apa':
            # APA: Author, A. A., Author, B. B., & Author, C. C.
            formatted = []
            for i, author in enumerate(authors[:20]):  # APA最多20个作者
                if isinstance(author, dict):
                    name = author.get('name', '')
                else:
                    name = str(author)
                
                parts = name.split()
                if len(parts) >= 2:
                    last = parts[-1]
                    initials = ' '.join([f"{p[0]}." for p in parts[:-1]])
                    formatted.append(f"{last}, {initials}")
                else:
                    formatted.append(name)
            
            if len(authors) == 1:
                return formatted[0]
            elif len(authors) <= 20:
                return ', '.join(formatted[:-1]) + ', & ' + formatted[-1]
            else:
                return ', '.join(formatted) + ', et al.'
        
        return ', '.join([str(a) for a in authors])


class BibTeXFormatter(CitationFormatter):
    """BibTeX 格式生成器"""
    
    def format_all(self) -> str:
        """生成 BibTeX 格式的引用列表"""
        entries = []
        
        for paper in self.papers:
            entry = self._format_single(paper)
            entries.append(entry)
        
        return '\n\n'.join(entries)
    
    def _format_single(self, paper: Dict) -> str:
        """格式化单篇论文为 BibTeX 条目"""
        key = self._generate_key(paper)
        
        # 确定条目类型
        venue = paper.get('venue', '')
        if paper.get('arxiv_id'):
            entry_type = 'misc'
        elif any(conf in venue.lower() for conf in ['conference', 'proceedings', 'cvpr', 'icml', 'neurips', 'iclr', 'acl', 'emnlp', 'aaai', 'ijcai', 'kdd']):
            entry_type = 'inproceedings'
        elif any(journal in venue.lower() for journal in ['journal', 'transactions', 'review', 'letters', 'arxiv']):
            entry_type = 'article'
        else:
            entry_type = 'misc'
        
        # 构建字段
        fields = []
        
        # title
        title = paper.get('title', '').replace('{', '').replace('}', '')
        fields.append(f'  title = {{{title}}}')
        
        # author
        authors = self._format_authors(paper.get('authors', []), 'bibtex')
        if authors and authors != "Unknown":
            fields.append(f'  author = {{{authors}}}')
        
        # year
        year = paper.get('year', '')
        if year:
            fields.append(f'  year = {{{year}}}')
        
        # venue/booktitle/journal
        if entry_type == 'inproceedings':
            fields.append(f'  booktitle = {{{venue}}}')
        elif entry_type == 'article':
            fields.append(f'  journal = {{{venue}}}')
        
        # pages
        pages = paper.get('pages', '')
        if pages:
            fields.append(f'  pages = {{{pages}}}')
        
        # doi
        doi = paper.get('doi', '')
        if doi:
            fields.append(f'  doi = {{{doi}}}')
        
        # arXiv
        arxiv_id = paper.get('arxiv_id', '')
        if arxiv_id:
            fields.append(f'  eprint = {{{arxiv_id}}}')
            fields.append(f'  eprinttype = {{arXiv}}')
        
        # url
        pdf_url = paper.get('pdf_url', '')
        if pdf_url:
            fields.append(f'  url = {{{pdf_url}}}')
        
        # abstract (可选)
        abstract = paper.get('abstract', '')
        if abstract:
            fields.append(f'  abstract = {{{abstract[:200]}...}}')
        
        # 组装条目
        entry_lines = [f'@{entry_type}{{{key},'] + [f + ',' for f in fields] + ['}']
        return '\n'.join(entry_lines)


class GB7714Formatter(CitationFormatter):
    """GB/T 7714 格式生成器（中文论文标准）"""
    
    def format_all(self) -> str:
        """生成 GB/T 7714 格式的引用列表"""
        entries = []
        
        for i, paper in enumerate(self.papers, 1):
            entry = self._format_single(paper, i)
            entries.append(entry)
        
        return '\n'.join(entries)
    
    def _format_single(self, paper: Dict, index: int) -> str:
        """格式化单篇论文为 GB/T 7714 格式"""
        authors = self._format_authors_gb7714(paper.get('authors', []))
        title = paper.get('title', '')
        venue = paper.get('venue', '')
        year = paper.get('year', '')
        doi = paper.get('doi', '')
        arxiv_id = paper.get('arxiv_id', '')
        
        # 判断文献类型
        if arxiv_id and not venue:
            # 预印本
            entry = f"[{index}] {authors}. {title}[EB/OL]. arXiv preprint arXiv:{arxiv_id}, {year}."
            if doi:
                entry += f" https://doi.org/{doi}"
        
        elif any(conf in venue.lower() for conf in ['conference', 'proceedings', 'cvpr', 'icml', 'neurips', 'iclr']):
            # 会议论文
            entry = f"[{index}] {authors}. {title}[C]. {venue}, {year}."
            if doi:
                entry += f" https://doi.org/{doi}"
            entry += "."
        
        elif venue:
            # 期刊论文
            volume = paper.get('volume', '')
            issue = paper.get('issue', '')
            pages = paper.get('pages', '')
            
            entry = f"[{index}] {authors}. {title}[J]. {venue}"
            if year:
                entry += f", {year}"
            if volume:
                entry += f", {volume}"
            if issue:
                entry += f"({issue})"
            if pages:
                entry += f": {pages}"
            entry += "."
            if doi:
                entry += f" https://doi.org/{doi}."
        
        else:
            # 其他类型
            entry = f"[{index}] {authors}. {title}[M]. {year}."
        
        return entry
    
    def _format_authors_gb7714(self, authors: List) -> str:
        """GB/T 7714 作者格式：姓前名后，逗号分隔，最多3人"""
        if not authors:
            return "佚名"
        
        formatted = []
        for author in authors[:3]:
            if isinstance(author, dict):
                name = author.get('name', '')
            else:
                name = str(author)
            
            # 简化为 姓,名首字母 格式
            parts = name.split()
            if len(parts) >= 2:
                # 假设最后一个是姓
                last = parts[-1]
                initials = ''.join([p[0] for p in parts[:-1]])
                formatted.append(f"{last} {initials}")
            else:
                formatted.append(name)
        
        if len(authors) > 3:
            formatted.append("等")
        
        return ', '.join(formatted)


class APAFormatter(CitationFormatter):
    """APA 格式生成器（第 7 版）"""
    
    def format_all(self) -> str:
        """生成 APA 格式的引用列表"""
        entries = []
        
        for paper in self.papers:
            entry = self._format_single(paper)
            entries.append(entry)
        
        return '\n\n'.join(entries)
    
    def _format_single(self, paper: Dict) -> str:
        """格式化单篇论文为 APA 格式"""
        authors = self._format_authors(paper.get('authors', []), 'apa')
        year = paper.get('year', 'n.d.')
        title = paper.get('title', '')
        venue = paper.get('venue', '')
        doi = paper.get('doi', '')
        arxiv_id = paper.get('arxiv_id', '')
        
        # 判断文献类型
        if arxiv_id and not venue:
            # 预印本
            entry = f"{authors} ({year}). {title}. *arXiv preprint arXiv:{arxiv_id}*."
            if doi:
                entry += f" https://doi.org/{doi}"
        
        elif any(conf in venue.lower() for conf in ['conference', 'proceedings', 'cvpr', 'icml', 'neurips', 'iclr']):
            # 会议论文
            entry = f"{authors} ({year}). {title}. In *{venue}* (pp. XX-XX)."
            if doi:
                entry += f" https://doi.org/{doi}"
            entry += "."
        
        elif venue:
            # 期刊论文
            volume = paper.get('volume', '')
            issue = paper.get('issue', '')
            pages = paper.get('pages', '')
            
            entry = f"{authors} ({year}). {title}. *{venue}*"
            if volume:
                entry += f", *{volume}*"
            if issue:
                entry += f"({issue})"
            if pages:
                entry += f", {pages}"
            entry += "."
            if doi:
                entry += f" https://doi.org/{doi}"
        
        else:
            # 其他类型
            entry = f"{authors} ({year}). {title}."
        
        return entry
    
    def format_citations_inline(self) -> List[str]:
        """生成文中引用标记 (Author, Year)"""
        markers = []
        for paper in self.papers:
            authors = paper.get('authors', [])
            year = paper.get('year', 'n.d.')
            
            if authors:
                if isinstance(authors[0], dict):
                    first_author = authors[0].get('name', '')
                else:
                    first_author = str(authors[0])
                
                last_name = first_author.split()[-1]
                
                if len(authors) == 1:
                    marker = f"({last_name}, {year})"
                elif len(authors) == 2:
                    second = str(authors[1]).split()[-1] if not isinstance(authors[1], dict) else authors[1].get('name', '').split()[-1]
                    marker = f"({last_name} & {second}, {year})"
                else:
                    marker = f"({last_name} et al., {year})"
            else:
                marker = f"(Anonymous, {year})"
            
            markers.append(marker)
        
        return markers


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Format citations in various styles')
    parser.add_argument('--style', choices=['bibtex', 'gb7714', 'apa'], required=True,
                       help='Citation style to use')
    parser.add_argument('--papers', type=str, required=True,
                       help='JSON file containing paper metadata or JSON string')
    parser.add_argument('--output', type=str, help='Output file path (default: stdout)')
    parser.add_argument('--with-markers', action='store_true',
                       help='Also generate inline citation markers (APA only)')
    
    args = parser.parse_args()
    
    # 读取论文数据
    papers_data = args.papers
    if papers_data.endswith('.json') and os.path.exists(papers_data):
        with open(papers_data, 'r', encoding='utf-8') as f:
            papers = json.load(f)
    else:
        # 尝试解析为 JSON 字符串
        try:
            papers = json.loads(papers_data)
        except json.JSONDecodeError:
            print(f"Error: Cannot parse papers data: {papers_data[:100]}...", file=sys.stderr)
            sys.exit(1)
    
    # 确保是列表
    if not isinstance(papers, list):
        papers = [papers]
    
    # 选择格式化器
    formatter_map = {
        'bibtex': BibTeXFormatter,
        'gb7714': GB7714Formatter,
        'apa': APAFormatter,
    }
    
    formatter_class = formatter_map.get(args.style)
    if not formatter_class:
        print(f"Error: Unknown style {args.style}", file=sys.stderr)
        sys.exit(1)
    
    formatter = formatter_class(papers)
    output = formatter.format_all()
    
    # 如果需要文中引用标记（APA 格式）
    if args.with_markers and args.style == 'apa':
        markers = formatter.format_citations_inline()
        output += "\n\n---\n\nInline citation markers:\n"
        for i, marker in enumerate(markers, 1):
            output += f"[{i}] {marker}\n"
    
    # 输出结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Formatted citations written to: {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    import os
    main()
