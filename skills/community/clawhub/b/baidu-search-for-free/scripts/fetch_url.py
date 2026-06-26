#!/usr/bin/env python3
"""
网页内容抓取和解析脚本

用法:
    python3 fetch_url.py "http://example.com"
    python3 fetch_url.py "http://example.com" --max-chars 2000
    python3 fetch_url.py "http://example.com" --json
"""

import sys
import json
import argparse
import re

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("错误: 缺少必要的依赖库")
    print("请运行: pip3 install --user requests beautifulsoup4 lxml")
    sys.exit(1)


def clean_text(text):
    """清理文本内容"""
    # 移除多余空白
    text = re.sub(r'\s+', ' ', text)
    # 移除特殊字符
    text = re.sub(r'[\n\r\t]+', '\n', text)
    # 移除多余空行
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()


def fetch_url(url, max_chars=None, timeout=30):
    """
    抓取并解析网页内容
    
    Args:
        url: 网页URL
        max_chars: 最大返回字符数
        timeout: 请求超时时间
    
    Returns:
        dict: 包含标题、正文、URL等信息的字典
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # 禁用 SSL 验证（某些环境可能需要）
        response = requests.get(url, headers=headers, timeout=timeout, verify=False)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 获取标题
        title = ''
        if soup.title:
            title = soup.title.string.strip() if soup.title.string else ''
        
        # 获取正文内容
        # 移除 script 和 style 标签
        for script in soup(['script', 'style', 'nav', 'footer', 'header']):
            script.decompose()
        
        # 尝试找到主要内容区域
        text = ''
        
        # 优先查找 article 或 main 标签
        main_content = soup.find(['article', 'main'])
        if main_content:
            text = main_content.get_text(separator='\n', strip=True)
        
        # 如果没有找到，尝试查找 content 相关的 class/id
        if not text:
            for elem in soup.find_all(['div', 'section']):
                elem_class = ' '.join(elem.get('class', []))
                elem_id = elem.get('id', '')
                if any(keyword in elem_class.lower() or elem_id.lower() for keyword in 
                       ['content', 'article', 'post', 'main', 'body']):
                    text = elem.get_text(separator='\n', strip=True)
                    break
        
        # 如果还是没找到，获取 body 的全部文本
        if not text:
            body = soup.find('body')
            if body:
                text = body.get_text(separator='\n', strip=True)
        
        # 清理文本
        text = clean_text(text)
        
        # 截断文本
        if max_chars and len(text) > max_chars:
            text = text[:max_chars] + '...'
        
        return {
            'title': title,
            'text': text,
            'url': url,
            'status_code': response.status_code
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'title': '',
            'text': f'请求错误: {e}',
            'url': url,
            'status_code': None,
            'error': str(e)
        }
    except Exception as e:
        return {
            'title': '',
            'text': f'解析错误: {e}',
            'url': url,
            'status_code': None,
            'error': str(e)
        }


def main():
    parser = argparse.ArgumentParser(description='网页内容抓取工具')
    parser.add_argument('url', help='要抓取的网页URL')
    parser.add_argument('--max-chars', '-m', type=int, default=None, help='最大返回字符数')
    parser.add_argument('--json', '-j', action='store_true', help='以JSON格式输出')
    parser.add_argument('--silent', '-s', action='store_true', help='静默模式')
    
    args = parser.parse_args()
    
    if not args.silent:
        print(f"正在抓取: {args.url}")
        print("-" * 50)
    
    result = fetch_url(args.url, max_chars=args.max_chars)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result.get('error'):
            print(f"错误: {result['error']}")
            sys.exit(1)
        
        print(f"标题: {result['title']}")
        print(f"状态: {result['status_code']}")
        print(f"URL: {result['url']}")
        print("-" * 50)
        print("正文内容:")
        print(result['text'])


if __name__ == '__main__':
    main()
