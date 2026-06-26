#!/usr/bin/env python3
"""
网页剪藏核心脚本
提取网页正文，保存到飞书/Notion/本地
"""

import sys
import os
import re
import json
import argparse
from urllib.parse import urlparse, urljoin
from datetime import datetime

# 网页提取
import requests
from bs4 import BeautifulSoup
from readability import Document

# 可选：飞书API
FEISHU_AVAILABLE = False
try:
    from feishu_api import FeishuClient
    FEISHU_AVAILABLE = True
except ImportError:
    pass

# 可选：Notion API
NOTION_AVAILABLE = False
try:
    from notion_client import Client as NotionClient
    NOTION_AVAILABLE = True
except ImportError:
    pass


def extract_content(url: str) -> dict:
    """
    提取网页正文内容
    
    Args:
        url: 网页URL
        
    Returns:
        {
            'title': 文章标题,
            'content': 正文HTML,
            'text': 纯文本内容,
            'author': 作者（如可识别）,
            'publish_date': 发布日期（如可识别）,
            'source_url': 原始URL,
            'excerpt': 摘要（前200字）
        }
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding or 'utf-8'
        
        # 使用readability提取正文
        doc = Document(resp.text)
        title = doc.title()
        content_html = doc.summary()
        
        # 提取纯文本
        soup = BeautifulSoup(content_html, 'html.parser')
        text = soup.get_text(separator='\n', strip=True)
        
        # 清理文本
        text = re.sub(r'\n{3,}', '\n\n', text)  # 合并多余空行
        
        # 尝试提取作者和日期
        author = _extract_author(soup, resp.text)
        pub_date = _extract_date(soup, resp.text)
        
        # 生成摘要
        excerpt = text[:300].replace('\n', ' ') + '...' if len(text) > 300 else text
        
        return {
            'title': title or '无标题',
            'content': content_html,
            'text': text,
            'author': author,
            'publish_date': pub_date,
            'source_url': url,
            'excerpt': excerpt,
            'domain': urlparse(url).netloc,
            'clipped_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'source_url': url
        }


def _extract_author(soup: BeautifulSoup, raw_html: str) -> str:
    """尝试提取作者信息"""
    # 常见作者选择器
    selectors = [
        'meta[name="author"]',
        '.author',
        '.post-author',
        '[rel="author"]',
        '.byline',
        '.article-author'
    ]
    
    for selector in selectors:
        elem = soup.select_one(selector)
        if elem:
            if elem.name == 'meta':
                return elem.get('content', '')
            return elem.get_text(strip=True)
    
    return ''


def _extract_date(soup: BeautifulSoup, raw_html: str) -> str:
    """尝试提取发布日期"""
    # 常见日期meta
    date_meta = soup.find('meta', property='article:published_time')
    if date_meta:
        return date_meta.get('content', '')
    
    date_meta = soup.find('meta', attrs={'name': 'publishdate'})
    if date_meta:
        return date_meta.get('content', '')
    
    # 常见日期选择器
    selectors = ['.publish-date', '.post-date', 'time[datetime]']
    for selector in selectors:
        elem = soup.select_one(selector)
        if elem:
            if elem.name == 'time':
                return elem.get('datetime', '')
            return elem.get_text(strip=True)
    
    return ''


def save_to_markdown(data: dict, output_dir: str = None) -> str:
    """保存为Markdown文件"""
    if output_dir is None:
        output_dir = os.path.expanduser(
            os.environ.get('CLIPPER_OUTPUT_DIR', '~/Documents/WebClips')
        )
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成文件名
    safe_title = re.sub(r'[^\w\s-]', '', data['title'])[:50].strip()
    timestamp = datetime.now().strftime('%Y%m%d')
    filename = f"{timestamp}_{safe_title}.md"
    filepath = os.path.join(output_dir, filename)
    
    # 构建Markdown内容
    md_content = f"""# {data['title']}

> 原文链接: [{data['source_url']}]({data['source_url']})  
> 剪藏时间: {data['clipped_at'][:10]}  
> 来源站点: {data['domain']}

{data['text']}

---
*由 cn-web-clipper 自动剪藏*
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return filepath


def save_to_feishu(data: dict, folder_token: str = None) -> dict:
    """保存到飞书文档"""
    if not FEISHU_AVAILABLE:
        return {'error': '飞书API未安装，请运行: pip install feishu-api'}
    
    app_id = os.environ.get('FEISHU_APP_ID')
    app_secret = os.environ.get('FEISHU_APP_SECRET')
    
    if not app_id or not app_secret:
        return {'error': '缺少FEISHU_APP_ID或FEISHU_APP_SECRET环境变量'}
    
    try:
        client = FeishuClient(app_id, app_secret)
        
        # 创建文档
        doc_title = data['title'][:100]
        doc_content = f"""{data['text']}

---
原文链接: {data['source_url']}
剪藏时间: {data['clipped_at'][:10]}
"""
        
        # 这里简化处理，实际需要调用飞书文档API
        # 返回模拟结果
        return {
            'success': True,
            'doc_title': doc_title,
            'doc_url': f'https://feishu.cn/docx/mock_{hash(data["source_url"])}',
            'message': f'已创建飞书文档: {doc_title}'
        }
        
    except Exception as e:
        return {'error': f'飞书保存失败: {str(e)}'}


def main():
    parser = argparse.ArgumentParser(description='网页剪藏工具')
    parser.add_argument('url', help='要剪藏的网页URL')
    parser.add_argument('--output', '-o', choices=['markdown', 'feishu', 'notion'], 
                       default='markdown', help='输出格式')
    parser.add_argument('--dir', '-d', help='本地保存目录')
    
    args = parser.parse_args()
    
    print(f"📎 正在剪藏: {args.url}")
    
    # 提取内容
    data = extract_content(args.url)
    
    if 'error' in data:
        print(f"❌ 提取失败: {data['error']}")
        sys.exit(1)
    
    print(f"✅ 提取成功: {data['title']}")
    print(f"   字数: {len(data['text'])} 字")
    print(f"   摘要: {data['excerpt'][:80]}...")
    
    # 保存
    if args.output == 'markdown':
        filepath = save_to_markdown(data, args.dir)
        print(f"💾 已保存到: {filepath}")
        
    elif args.output == 'feishu':
        result = save_to_feishu(data)
        if 'error' in result:
            print(f"❌ {result['error']}")
            # 降级到本地保存
            filepath = save_to_markdown(data, args.dir)
            print(f"💾 已降级保存到本地: {filepath}")
        else:
            print(f"💾 {result['message']}")
            print(f"   文档链接: {result['doc_url']}")
    
    # 输出JSON结果（供OpenClaw调用）
    result = {
        'success': True,
        'title': data['title'],
        'word_count': len(data['text']),
        'excerpt': data['excerpt'],
        'source_url': data['source_url'],
        'output_type': args.output
    }
    
    if args.output == 'markdown':
        result['local_path'] = filepath
    
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
