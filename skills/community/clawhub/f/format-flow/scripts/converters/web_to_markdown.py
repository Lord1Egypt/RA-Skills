#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
网页文档转 Markdown 转换器
支持 URL 和本地 HTML 文件
"""

import sys
import re
from pathlib import Path
from typing import Optional, List
from urllib.parse import urljoin, urlparse

# 导入依赖
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    pass

# 导入工具函数
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import print_success, print_error, print_info


def clean_html(html_content: str) -> str:
    """
    清理 HTML 内容，移除不必要的标签
    
    Args:
        html_content: HTML 内容
    
    Returns:
        清理后的 HTML
    """
    # 移除 script 和 style 标签
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    
    # 移除注释
    html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
    
    # 移除导航、侧边栏、页脚等（常见模式）
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 移除常见的不需要的元素
    for tag in soup.find_all(['nav', 'aside', 'footer', 'header']):
        tag.decompose()
    
    # 移除特定 class 的元素
    for tag in soup.find_all(class_=re.compile(r'(nav|sidebar|footer|header|menu|comment|advertisement)', re.I)):
        tag.decompose()
    
    return str(soup)


def extract_metadata(soup: BeautifulSoup, url: str = None) -> dict:
    """
    提取网页元数据
    
    Args:
        soup: BeautifulSoup 对象
        url: 网页 URL
    
    Returns:
        元数据字典
    """
    metadata = {
        'title': '',
        'author': '',
        'date': '',
        'description': '',
        'url': url or ''
    }
    
    # 标题
    if soup.title:
        metadata['title'] = soup.title.string.strip()
    
    # meta 标签
    for meta in soup.find_all('meta'):
        name = meta.get('name', '').lower()
        prop = meta.get('property', '').lower()
        content = meta.get('content', '')
        
        if name == 'author' or prop == 'article:author':
            metadata['author'] = content
        elif name == 'date' or prop == 'article:published_time':
            metadata['date'] = content
        elif name == 'description' or prop == 'og:description':
            metadata['description'] = content
        elif prop == 'og:title' and not metadata['title']:
            metadata['title'] = content
    
    return metadata


def html_to_markdown(html_content: str, base_url: str = None) -> str:
    """
    将 HTML 内容转换为 Markdown
    
    Args:
        html_content: HTML 内容
        base_url: 基础 URL（用于处理相对路径）
    
    Returns:
        Markdown 文本
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    md_lines = []
    
    # 处理标题
    for i in range(1, 7):
        for tag in soup.find_all(f'h{i}'):
            text = tag.get_text().strip()
            if text:
                md_lines.append(f"\n{'#' * i} {text}\n")
    
    # 处理段落
    for tag in soup.find_all('p'):
        text = tag.get_text().strip()
        if text:
            md_lines.append(f"\n{text}\n")
    
    # 处理链接
    for tag in soup.find_all('a'):
        text = tag.get_text().strip()
        href = tag.get('href', '')
        if text and href:
            # 处理相对路径
            if base_url and not urlparse(href).scheme:
                href = urljoin(base_url, href)
            # 替换原有文本为 Markdown 链接
            md_link = f"[{text}]({href})"
            tag.replace_with(md_link)
    
    # 处理图片
    for tag in soup.find_all('img'):
        alt = tag.get('alt', 'Image')
        src = tag.get('src', '')
        if src:
            # 处理相对路径
            if base_url and not urlparse(src).scheme:
                src = urljoin(base_url, src)
            md_img = f"\n![{alt}]({src})\n"
            md_lines.append(md_img)
    
    # 处理列表
    for tag in soup.find_all('ul'):
        for li in tag.find_all('li', recursive=False):
            text = li.get_text().strip()
            if text:
                md_lines.append(f"- {text}")
        md_lines.append("")
    
    for tag in soup.find_all('ol'):
        for i, li in enumerate(tag.find_all('li', recursive=False), 1):
            text = li.get_text().strip()
            if text:
                md_lines.append(f"{i}. {text}")
        md_lines.append("")
    
    # 处理代码块
    for tag in soup.find_all('pre'):
        code = tag.get_text()
        md_lines.append(f"\n```\n{code}\n```\n")
    
    for tag in soup.find_all('code'):
        if tag.parent.name != 'pre':
            code = tag.get_text()
            md_lines.append(f"`{code}`")
    
    # 处理引用
    for tag in soup.find_all('blockquote'):
        text = tag.get_text().strip()
        lines = text.split('\n')
        for line in lines:
            md_lines.append(f"> {line}")
        md_lines.append("")
    
    # 处理表格
    for table in soup.find_all('table'):
        rows = table.find_all('tr')
        if rows:
            # 表头
            header_cells = rows[0].find_all(['th', 'td'])
            if header_cells:
                md_lines.append("| " + " | ".join([cell.get_text().strip() for cell in header_cells]) + " |")
                md_lines.append("| " + " | ".join(["---"] * len(header_cells)) + " |")
            
            # 数据行
            for row in rows[1:]:
                cells = row.find_all(['td', 'th'])
                if cells:
                    md_lines.append("| " + " | ".join([cell.get_text().strip() for cell in cells]) + " |")
            
            md_lines.append("")
    
    # 处理粗体和斜体
    for tag in soup.find_all(['strong', 'b']):
        text = tag.get_text()
        if text:
            tag.replace_with(f"**{text}**")
    
    for tag in soup.find_all(['em', 'i']):
        text = tag.get_text()
        if text:
            tag.replace_with(f"*{text}*")
    
    return '\n'.join(md_lines)


def convert_url_to_markdown(url: str, output_path: Optional[Path] = None,
                             include_metadata: bool = True,
                             clean_content: bool = True,
                             verbose: bool = True) -> bool:
    """
    将网页 URL 转换为 Markdown
    
    Args:
        url: 网页 URL
        output_path: 输出 Markdown 路径（可选）
        include_metadata: 是否包含元数据
        clean_content: 是否清理不必要的内容
        verbose: 是否显示详细信息
    
    Returns:
        是否转换成功
    """
    try:
        if verbose:
            print_info(f"Fetching: {url}")
        
        # 获取网页内容
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取元数据
        metadata = extract_metadata(soup, url)
        
        # 清理内容
        if clean_content:
            html_content = clean_html(response.text)
            soup = BeautifulSoup(html_content, 'html.parser')
        
        # 转换为 Markdown
        md_content = html_to_markdown(str(soup), url)
        
        # 确定输出路径
        if output_path is None:
            # 从 URL 生成文件名
            parsed_url = urlparse(url)
            filename = parsed_url.path.strip('/').replace('/', '_') or 'webpage'
            output_path = Path(f"{filename}.md")
        
        # 添加元数据
        final_content = []
        if include_metadata:
            final_content.append(f"# {metadata['title']}\n")
            if metadata['author']:
                final_content.append(f"**Author:** {metadata['author']}\n")
            if metadata['date']:
                final_content.append(f"**Date:** {metadata['date']}\n")
            if metadata['url']:
                final_content.append(f"**Source:** {metadata['url']}\n")
            final_content.append("\n---\n")
        
        final_content.append(md_content)
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(''.join(final_content))
        
        if verbose:
            print_success(f"Created: {output_path}")
        
        return True
    
    except Exception as e:
        if verbose:
            print_error(f"Conversion failed: {e}")
        return False




def convert_html_file_to_markdown(html_path: Path, output_path: Optional[Path] = None,
                                    verbose: bool = True) -> bool:
    """
    将本地 HTML 文件转换为 Markdown
    
    Args:
        html_path: HTML 文件路径
        output_path: 输出 Markdown 路径（可选）
        verbose: 是否显示详细信息
    
    Returns:
        是否转换成功
    """
    if not html_path.exists():
        if verbose:
            print_error(f"File not found: {html_path}")
        return False
    
    try:
        if verbose:
            print_info(f"Reading: {html_path.name}")
        
        # 读取 HTML 文件
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 清理和转换
        html_content = clean_html(html_content)
        md_content = html_to_markdown(html_content)
        
        # 确定输出路径
        if output_path is None:
            output_path = html_path.with_suffix('.md')
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        if verbose:
            print_success(f"Created: {output_path}")
        
        return True
    
    except Exception as e:
        if verbose:
            print_error(f"Conversion failed: {e}")
        return False


def batch_convert_urls_to_markdown(urls: List[str], output_dir: Optional[Path] = None,
                                     verbose: bool = True) -> dict:
    """
    批量转换多个 URL 为 Markdown
    
    Args:
        urls: URL 列表
        output_dir: 输出目录
        verbose: 是否显示详细信息
    
    Returns:
        转换结果统计
    """
    results = {'success': 0, 'failed': 0}
    
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    for i, url in enumerate(urls, 1):
        if verbose:
            print(f"\n[{i}/{len(urls)}] {url}")
        
        # 生成输出路径
        if output_dir:
            parsed_url = urlparse(url)
            filename = parsed_url.path.strip('/').replace('/', '_') or f'webpage_{i}'
            output_path = output_dir / f"{filename}.md"
        else:
            output_path = None
        
        success = convert_url_to_markdown(url, output_path, verbose=verbose)
        
        if success:
            results['success'] += 1
        else:
            results['failed'] += 1
    
    if verbose:
        print(f"\n{'='*50}")
        print(f"Conversion completed: {results['success']} success, {results['failed']} failed")
    
    return results
