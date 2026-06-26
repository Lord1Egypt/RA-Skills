#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度搜索工具 - 安全修复版
使用百度站内搜索API进行网页搜索

修复:
- [SECURITY] 移除 SSL 验证禁用代码
- [SECURITY] 添加输入验证
- [SECURITY] 添加请求超时和重试限制
- [IMPROVE] 改进错误处理
"""

import os
import sys
import json
import urllib.parse
import urllib.request
import re
import ssl
import socket

# ============== 安全配置 ==============

# 使用系统默认 SSL 上下文（不禁用证书验证）
# 如果需要自定义 CA 证书，可以使用:
# import certifi
# ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl_context = ssl.create_default_context()

# 请求超时设置（秒）
REQUEST_TIMEOUT = 10

# 最大重试次数
MAX_RETRIES = 2

# 最大结果数量限制
MAX_RESULTS = 50


def validate_input(query, num=10, page=1):
    """
    验证输入参数
    
    Returns:
        (is_valid, error_message)
    """
    # 验证查询词
    if not query or not isinstance(query, str):
        return False, "搜索词不能为空"
    
    # 限制查询长度
    if len(query) > 200:
        return False, "搜索词过长（最大200字符）"
    
    # 清理查询词（移除危险字符）
    query = query.strip()
    if not query:
        return False, "搜索词不能为空"
    
    # 验证数量
    if not isinstance(num, int) or num < 1:
        return False, "结果数量必须为正整数"
    
    if num > MAX_RESULTS:
        return False, f"结果数量超过最大限制（{MAX_RESULTS}）"
    
    # 验证页码
    if not isinstance(page, int) or page < 1:
        return False, "页码必须为正整数"
    
    return True, None


def sanitize_html(text):
    """
    清理 HTML 内容，移除潜在危险标签
    """
    if not text:
        return ""
    
    # 移除 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)
    
    # 解码 HTML 实体
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    text = text.replace('&nbsp;', ' ')
    
    # 清理多余空白
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def baidu_search(query, num=10, page=1):
    """
    执行百度搜索
    
    Args:
        query: 搜索关键词（最大200字符）
        num: 返回结果数量 (1-50)
        page: 页码
    
    Returns:
        dict: 搜索结果，格式:
        {
            'query': '搜索词',
            'total': 结果数量,
            'results': [
                {'title': '标题', 'link': '链接', 'abstract': '摘要'},
                ...
            ]
        }
        None: 搜索失败
    """
    # 输入验证
    is_valid, error = validate_input(query, num, page)
    if not is_valid:
        print(f"参数错误: {error}")
        return None
    
    # 清理查询词
    query = query.strip()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'identity',  # 不压缩，简化处理
        'Referer': 'https://www.baidu.com/',
        'Connection': 'keep-alive'
    }
    
    params = {
        'wd': query,
        'pn': (page - 1) * 10,
        'rn': min(num, MAX_RESULTS),
        'tn': 'baidu',
        'ie': 'utf-8'
    }
    
    url = 'https://www.baidu.com/s?' + urllib.parse.urlencode(params)
    
    # 请求重试
    html = None
    last_error = None
    
    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers=headers)
            
            # 使用安全的 SSL 上下文
            with urllib.request.urlopen(
                req, 
                timeout=REQUEST_TIMEOUT,
                context=ssl_context
            ) as response:
                html = response.read().decode('utf-8', errors='ignore')
            break  # 成功，退出重试
            
        except urllib.error.HTTPError as e:
            last_error = f"HTTP错误: {e.code} {e.reason}"
            if e.code == 429:  # 限流
                break
        except urllib.error.URLError as e:
            last_error = f"URL错误: {e.reason}"
        except socket.timeout:
            last_error = "请求超时"
        except Exception as e:
            last_error = f"未知错误: {str(e)}"
    
    if html is None:
        print(f"搜索失败: {last_error}")
        return None
    
    try:
        results = []
        
        # 查找所有结果容器
        result_pattern = r'<div[^>]*class="[^"]*result[^"]*"[^>]*>(.*?)</div>\s*</div>'
        result_blocks = re.findall(result_pattern, html, re.DOTALL)
        
        if not result_blocks:
            # 尝试另一种模式
            result_pattern = r'<div[^>]*class="c-container"[^>]*>(.*?)</div>\s*</div>'
            result_blocks = re.findall(result_pattern, html, re.DOTALL)
        
        for block in result_blocks[:num]:
            try:
                # 提取标题和链接
                title_match = re.search(
                    r'<h3[^>]*>.*?<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>.*?</h3>',
                    block,
                    re.DOTALL
                )
                if not title_match:
                    continue
                
                link = title_match.group(1)
                title = sanitize_html(title_match.group(2))
                
                # 验证链接格式（只允许 http/https）
                if not link.startswith(('http://', 'https://')):
                    continue
                
                # 提取摘要
                abstract = ""
                abstract_patterns = [
                    r'<span class="content-right[^"]*">(.*?)</span>',
                    r'<div class="content-right[^"]*">(.*?)</div>',
                    r'<span class="c-abstract">(.*?)</span>',
                    r'<div class="c-abstract">(.*?)</div>',
                ]
                
                for pattern in abstract_patterns:
                    abs_match = re.search(pattern, block, re.DOTALL)
                    if abs_match:
                        abstract = sanitize_html(abs_match.group(1))
                        # 限制摘要长度
                        if len(abstract) > 200:
                            abstract = abstract[:200] + '...'
                        break
                
                if title:
                    results.append({
                        'title': title,
                        'link': link,
                        'abstract': abstract
                    })
            except Exception:
                continue
        
        # 备用方案：直接匹配所有标题和链接
        if not results:
            h3_pattern = r'<h3[^>]*>.*?<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>.*?</h3>'
            matches = re.findall(h3_pattern, html, re.DOTALL)
            
            for link, title_html in matches[:num]:
                title = sanitize_html(title_html)
                # 验证链接
                if title and link and link.startswith(('http://', 'https://')):
                    results.append({
                        'title': title,
                        'link': link,
                        'abstract': ''
                    })
        
        return {
            'query': query,
            'total': len(results),
            'results': results
        }
        
    except Exception as e:
        print(f"解析结果出错: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("使用方法: python baidu_search.py <搜索词> [结果数量]")
        print("示例: python baidu_search.py 'Python教程' 10")
        sys.exit(1)
    
    query = sys.argv[1]
    
    # 验证数量参数
    try:
        num = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    except ValueError:
        print("错误: 结果数量必须为整数")
        sys.exit(1)
    
    print(f"🔍 百度搜索: {query}\n")
    
    result = baidu_search(query, num)
    
    if result and result['results']:
        for i, item in enumerate(result['results'], 1):
            print(f"{i}. {item['title']}")
            print(f"   链接: {item['link']}")
            if item['abstract']:
                print(f"   摘要: {item['abstract']}")
            print()
    else:
        print("未找到搜索结果")


if __name__ == '__main__':
    main()
