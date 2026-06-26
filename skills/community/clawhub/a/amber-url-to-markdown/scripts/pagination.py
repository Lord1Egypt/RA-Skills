#!/usr/bin/env python3
"""
Amber Url to Markdown - 分页自动拼接模块
识别分页链接，自动抓取并拼接完整内容

作者：小文
时间：2026-03-24
版本：V3.1
"""

import re
from typing import List, Optional, Set
from urllib.parse import urljoin, urlparse, parse_qs
from bs4 import BeautifulSoup

# 导入配置
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
from fetcher import fetch_url_content


# ============================================================================
# 分页链接识别
# ============================================================================

def extract_pagination(html: str, base_url: str) -> List[str]:
    """
    识别分页链接（下一页/next/page=2）
    
    Args:
        html: HTML 内容
        base_url: 基础 URL（用于拼接相对路径）
    
    Returns:
        List[str]: 下一页链接列表
    """
    soup = BeautifulSoup(html, "html.parser")
    next_page_links = []
    
    # 1. 匹配"下一页"文本的链接
    next_btn = soup.find("a", text=re.compile(r"下一页 |Next|下页|更多", re.IGNORECASE))
    if next_btn and next_btn.get("href"):
        next_url = next_btn["href"]
        next_url = _normalize_url(next_url, base_url)
        if next_url:
            next_page_links.append(next_url)
    
    # 2. 匹配包含"next"类的链接
    next_class = soup.find("a", class_=re.compile(r"next|more|load-more", re.IGNORECASE))
    if next_class and next_class.get("href"):
        next_url = next_class["href"]
        next_url = _normalize_url(next_url, base_url)
        if next_url and next_url not in next_page_links:
            next_page_links.append(next_url)
    
    # 3. 匹配 page=数字的分页（如?page=2）
    page_pattern = re.compile(r"page=(\d+)", re.IGNORECASE)
    for a in soup.find_all("a", href=True):
        href = a["href"]
        match = page_pattern.search(href)
        if match:
            page_num = int(match.group(1))
            if page_num > 1:  # 跳过第一页
                full_url = _normalize_url(href, base_url)
                if full_url and full_url not in next_page_links:
                    next_page_links.append(full_url)
    
    # 4. 匹配数字分页（1, 2, 3...）- 取最大的数字
    page_numbers = []
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        if text.isdigit() and len(text) <= 3:  # 避免匹配大数字
            page_num = int(text)
            if page_num > 1:
                href = a["href"]
                full_url = _normalize_url(href, base_url)
                if full_url:
                    page_numbers.append((page_num, full_url))
    
    # 取最大页码
    if page_numbers:
        max_page = max(page_numbers, key=lambda x: x[0])
        if max_page[1] not in next_page_links:
            next_page_links.append(max_page[1])
    
    return next_page_links


def _normalize_url(url: str, base_url: str) -> Optional[str]:
    """
    标准化 URL（处理相对路径）
    
    Args:
        url: 原始 URL（可能是相对路径）
        base_url: 基础 URL
    
    Returns:
        str: 完整的 URL 或 None
    """
    if not url:
        return None
    
    # 使用 urljoin 处理相对路径
    full_url = urljoin(base_url, url)
    
    # 验证 URL 有效性
    parsed = urlparse(full_url)
    if parsed.scheme and parsed.netloc:
        return full_url
    
    return None


# ============================================================================
# 分页内容抓取
# ============================================================================

def fetch_paginated_content(
    base_url: str,
    max_pages: int = 10,
    timeout: int = None
) -> Optional[str]:
    """
    抓取分页页面，拼接完整内容
    
    Args:
        base_url: 起始 URL（第一页）
        max_pages: 最大抓取页数（防止无限循环）
        timeout: 请求超时时间
    
    Returns:
        str: 拼接后的完整 HTML 内容
    """
    all_content = []
    visited_urls: Set[str] = set()
    urls_to_fetch = [base_url]
    
    print(f"\n{'='*60}")
    print(f"分页抓取 - 起始 URL：{base_url}")
    print(f"最大页数：{max_pages}")
    print(f"{'='*60}\n")
    
    page_count = 0
    
    while urls_to_fetch and page_count < max_pages:
        url = urls_to_fetch.pop(0)
        
        # 防止重复抓取
        if url in visited_urls:
            print(f"[INFO] 跳过已抓取页面：{url}")
            continue
        
        visited_urls.add(url)
        page_count += 1
        
        print(f"[INFO] 抓取第 {page_count} 页：{url}")
        
        # 抓取当前页
        content = fetch_url_content(url, timeout)
        if not content:
            print(f"[WARN] 第 {page_count} 页抓取失败，停止")
            break
        
        all_content.append(content)
        
        # 识别下一页
        next_links = extract_pagination(content, url)
        
        if next_links:
            print(f"[INFO] 发现 {len(next_links)} 个下一页链接")
            # 添加到队列（去重）
            for link in next_links:
                if link not in visited_urls and link not in urls_to_fetch:
                    urls_to_fetch.append(link)
        else:
            print(f"[INFO] 未找到更多分页，已是最后一页")
            break
    
    if not all_content:
        return None
    
    # 拼接所有页的正文
    print(f"\n{'='*60}")
    print(f"✅ 分页抓取完成，共 {page_count} 页")
    print(f"{'='*60}\n")
    
    full_html = _merge_pages(all_content)
    return full_html


def _merge_pages(html_pages: List[str]) -> str:
    """
    拼接多个页面的 HTML
    
    Args:
        html_pages: HTML 内容列表
    
    Returns:
        str: 拼接后的 HTML
    """
    # 提取每页的 body 内容并拼接
    bodies = []
    
    for html in html_pages:
        soup = BeautifulSoup(html, "html.parser")
        body = soup.find("body")
        if body:
            # 移除脚本和样式
            for tag in body.find_all(["script", "style", "iframe"]):
                tag.decompose()
            bodies.append(str(body))
        else:
            # 没有 body 则使用整个 HTML
            bodies.append(html)
    
    # 用换行符拼接
    return "\n\n".join(bodies)


# ============================================================================
# 智能分页检测
# ============================================================================

def is_paginated(html: str, url: str) -> bool:
    """
    智能检测页面是否有分页
    
    Args:
        html: HTML 内容
        url: 当前 URL
    
    Returns:
        bool: 是否有分页
    """
    next_links = extract_pagination(html, url)
    return len(next_links) > 0


def get_pagination_info(html: str, url: str) -> dict:
    """
    获取分页详细信息
    
    Args:
        html: HTML 内容
        url: 当前 URL
    
    Returns:
        dict: 分页信息
    """
    next_links = extract_pagination(html, url)
    
    # 尝试提取当前页码
    soup = BeautifulSoup(html, "html.parser")
    current_page = 1
    
    # 查找当前页码指示器
    page_indicator = soup.find(class_=re.compile(r"current|active|selected", re.IGNORECASE))
    if page_indicator:
        text = page_indicator.get_text(strip=True)
        if text.isdigit():
            current_page = int(text)
    
    # 查找总页数
    total_pages = None
    total_match = re.search(r"共\s*(\d+)\s*页", html)
    if total_match:
        total_pages = int(total_match.group(1))
    
    return {
        "has_pagination": len(next_links) > 0,
        "next_urls": next_links,
        "current_page": current_page,
        "total_pages": total_pages,
        "is_first_page": current_page == 1,
    }


# ============================================================================
# 测试入口
# ============================================================================

if __name__ == "__main__":
    # 简单测试
    test_html = """
    <html>
        <body>
            <div class="content">第 1 页内容</div>
            <nav class="pagination">
                <a href="?page=1" class="active">1</a>
                <a href="?page=2">2</a>
                <a href="?page=3">3</a>
                <a href="?page=2" class="next">下一页</a>
            </nav>
        </body>
    </html>
    """
    
    base_url = "https://example.com/article"
    
    # 测试分页识别
    print("测试分页识别...")
    next_links = extract_pagination(test_html, base_url)
    print(f"下一页链接：{next_links}")
    
    # 测试分页检测
    print(f"\n是否有分页：{is_paginated(test_html, base_url)}")
    
    # 测试分页信息
    info = get_pagination_info(test_html, base_url)
    print(f"\n分页信息：{info}")
