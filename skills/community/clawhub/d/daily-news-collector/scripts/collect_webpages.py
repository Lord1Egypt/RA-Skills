#!/usr/bin/env python3
"""
网页内容抓取脚本
从指定URL抓取网页内容，提取正文文本
"""

import json
import argparse
from datetime import datetime
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional
import re

def fetch_webpage(url: str) -> Optional[str]:
    """抓取网页HTML内容"""
    try:
        import requests
        response = requests.get(url, timeout=30, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"错误: 抓取网页失败 {url}: {str(e)}")
        return None


def extract_content(html: str, url: str) -> Dict[str, Any]:
    """
    从HTML中提取关键信息

    参数:
        html: HTML内容
        url: 网页URL

    返回:
        提取的内容字典
    """
    soup = BeautifulSoup(html, 'lxml')

    # 提取标题
    title = ''
    if soup.find('h1'):
        title = soup.find('h1').get_text().strip()
    elif soup.find('title'):
        title = soup.find('title').get_text().strip()

    # 尝试找到正文内容（常见的选择器）
    content_selectors = [
        'article',
        '[class*="content"]',
        '[class*="article"]',
        '[id*="content"]',
        '[id*="article"]',
        'main',
    ]

    content_text = ''
    for selector in content_selectors:
        element = soup.select_one(selector)
        if element:
            # 移除脚本和样式标签
            for script in element(['script', 'style', 'nav', 'footer']):
                script.decompose()
            content_text = element.get_text(separator='\n', strip=True)
            if len(content_text) > 200:  # 找到足够长的内容
                break

    # 如果没有找到内容，提取所有段落
    if not content_text:
        paragraphs = soup.find_all('p')
        content_text = '\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])

    # 清理文本
    content_text = re.sub(r'\n+', '\n', content_text)
    content_text = content_text[:2000]  # 限制长度

    # 提取发布时间
    published = ''
    time_elements = soup.find_all(['time', 'span'], attrs={'class': re.compile(r'time|date|publish', re.I)})
    for elem in time_elements:
        text = elem.get_text().strip()
        if text:
            published = text
            break

    return {
        'url': url,
        'title': title,
        'content': content_text,
        'published': published,
        'collected_at': datetime.now().isoformat()
    }


def collect_webpages(urls: list) -> list:
    """
    收集多个网页的内容

    参数:
        urls: URL列表

    返回:
        网页内容列表
    """
    results = []

    for url in urls:
        if not url.startswith(('http://', 'https://')):
            print(f"警告: 跳过无效URL: {url}")
            continue

        print(f"正在抓取: {url}")
        html = fetch_webpage(url)

        if html:
            content = extract_content(html, url)
            results.append(content)
            print(f"成功: {content['title'][:50]}")
        else:
            print(f"失败: {url}")

    return results


def main():
    parser = argparse.ArgumentParser(description='抓取网页内容')
    parser.add_argument('--url', help='单个网页URL')
    parser.add_argument('--url-list', help='包含URL列表的文本文件（每行一个URL）')
    parser.add_argument('--output', required=True, help='输出文件路径（JSON格式）')
    args = parser.parse_args()

    # 收集URL列表
    urls = []

    if args.url:
        urls.append(args.url)

    if args.url_list:
        try:
            with open(args.url_list, 'r', encoding='utf-8') as f:
                for line in f:
                    url = line.strip()
                    if url and not url.startswith('#'):
                        urls.append(url)
        except FileNotFoundError:
            raise ValueError(f"URL列表文件不存在: {args.url_list}")

    if not urls:
        raise ValueError("未指定有效的URL")

    # 收集网页内容
    results = collect_webpages(urls)

    # 输出结果
    output_data = {
        'collected_at': datetime.now().isoformat(),
        'total_pages': len(results),
        'webpages': results
    }

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n抓取完成: 共 {len(results)} 个网页")
    print(f"结果已保存到: {args.output}")


if __name__ == '__main__':
    main()
