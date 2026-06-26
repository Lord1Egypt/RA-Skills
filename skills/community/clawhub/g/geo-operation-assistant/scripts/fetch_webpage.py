#!/usr/bin/env python3
"""
网页内容抓取脚本

功能：抓取指定 URL 的网页内容，提取标题、正文、外链、图片等结构化信息

参数：
  --url: 目标网页 URL（必需）
  --timeout: 请求超时时间（可选，默认 30 秒）

输出：JSON 格式的结构化数据
"""

import argparse
import json
import re
import sys
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


def fetch_webpage(url: str, timeout: int = 30) -> dict:
    """
    抓取网页内容并提取结构化信息
    
    Args:
        url: 目标网页 URL
        timeout: 请求超时时间（秒）
    
    Returns:
        包含网页结构化信息的字典
    """
    try:
        # 发送 HTTP 请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        # 解析 HTML
        soup = BeautifulSoup(response.content, 'lxml')
        
        # 提取标题
        title = ''
        if soup.title:
            title = soup.title.string.strip() if soup.title.string else ''
        
        # 提取 meta 描述
        meta_desc = ''
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag and meta_tag.get('content'):
            meta_desc = meta_tag['content'].strip()
        
        # 提取正文内容
        # 移除 script、style、nav、footer 等非正文元素
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            tag.decompose()
        
        # 提取主要内容区域
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|article|post|entry'))
        
        if main_content:
            content_text = main_content.get_text(separator='\n', strip=True)
        else:
            content_text = soup.get_text(separator='\n', strip=True)
        
        # 清理文本：移除多余空行
        content_lines = [line.strip() for line in content_text.split('\n') if line.strip()]
        content_text = '\n'.join(content_lines)
        
        # 提取标题层级
        headings = []
        for i in range(1, 7):
            for h in soup.find_all(f'h{i}'):
                heading_text = h.get_text(strip=True)
                if heading_text:
                    headings.append({
                        'level': i,
                        'text': heading_text
                    })
        
        # 提取外链
        external_links = []
        parsed_url = urlparse(url)
        base_domain = parsed_url.netloc
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            link_text = a.get_text(strip=True)
            
            # 解析完整 URL
            full_url = urljoin(url, href)
            parsed_href = urlparse(full_url)
            
            # 判断是否为外链
            if parsed_href.netloc and parsed_href.netloc != base_domain:
                external_links.append({
                    'url': full_url,
                    'text': link_text,
                    'domain': parsed_href.netloc
                })
        
        # 提取图片信息
        images = []
        for img in soup.find_all('img', src=True):
            img_url = urljoin(url, img['src'])
            alt_text = img.get('alt', '')
            images.append({
                'url': img_url,
                'alt': alt_text
            })
        
        # 统计信息
        word_count = len(content_text.split())
        paragraph_count = len(content_lines)
        
        # 构建结果
        result = {
            'url': url,
            'domain': base_domain,
            'title': title,
            'meta_description': meta_desc,
            'content': content_text,
            'word_count': word_count,
            'paragraph_count': paragraph_count,
            'headings': headings,
            'heading_count': len(headings),
            'external_links': external_links,
            'external_link_count': len(external_links),
            'images': images,
            'image_count': len(images),
            'status_code': response.status_code,
            'content_type': response.headers.get('Content-Type', ''),
            'fetch_success': True,
            'error_message': ''
        }
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            'url': url,
            'fetch_success': False,
            'error_message': f'HTTP 请求失败: {str(e)}'
        }
    except Exception as e:
        return {
            'url': url,
            'fetch_success': False,
            'error_message': f'解析失败: {str(e)}'
        }


def main():
    parser = argparse.ArgumentParser(description='抓取网页内容并提取结构化信息')
    parser.add_argument('--url', required=True, help='目标网页 URL')
    parser.add_argument('--timeout', type=int, default=30, help='请求超时时间（秒）')
    parser.add_argument('--output', choices=['json', 'text'], default='json', help='输出格式')
    
    args = parser.parse_args()
    
    # 执行抓取
    result = fetch_webpage(args.url, args.timeout)
    
    # 输出结果
    if args.output == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result['fetch_success']:
            print(f"标题: {result['title']}")
            print(f"域名: {result['domain']}")
            print(f"字数: {result['word_count']}")
            print(f"段落数: {result['paragraph_count']}")
            print(f"标题层级数: {result['heading_count']}")
            print(f"外链数: {result['external_link_count']}")
            print(f"图片数: {result['image_count']}")
            print(f"\n正文内容:\n{result['content'][:500]}...")
        else:
            print(f"抓取失败: {result['error_message']}")


if __name__ == '__main__':
    main()
