#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析前程无忧页面结构
"""

import requests
from bs4 import BeautifulSoup
import json

print('测试前程无忧页面结构...')

url = 'https://search.51job.com/list/010000,000000,0000,00,9,99,Python,2,1.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

try:
    response = requests.get(url, headers=headers, timeout=15)
    print(f'状态码: {response.status_code}')
    print(f'页面大小: {len(response.text)} 字符')
    
    # 保存页面供分析
    with open('51job_analysis.html', 'w', encoding='utf-8') as f:
        f.write(response.text[:10000])  # 保存前10000字符
    
    # 分析结构
    soup = BeautifulSoup(response.text, 'html.parser')
    
    print('\n分析页面结构:')
    
    # 查找所有包含'job'的class
    job_elements = []
    for tag in soup.find_all(True):
        if tag.get('class'):
            classes = ' '.join(tag.get('class'))
            if 'job' in classes.lower() or '职位' in classes or '工作' in classes:
                job_elements.append((tag.name, classes, len(str(tag))))
    
    print(f'找到 {len(job_elements)} 个可能包含职位的元素')
    
    if job_elements:
        # 按大小排序，取前5个
        job_elements.sort(key=lambda x: x[2], reverse=True)
        print('\n最大的5个可能职位容器:')
        for i, (tag, classes, size) in enumerate(job_elements[:5], 1):
            print(f'  {i}. <{tag}> class="{classes}" (大小: {size} 字符)')
    
    # 查找所有链接
    links = soup.find_all('a')
    job_links = []
    for link in links:
        href = link.get('href', '')
        text = link.get_text().strip()
        if ('job' in href or '职位' in text or '招聘' in text) and len(text) > 5:
            job_links.append((text[:30], href))
    
    print(f'\n找到 {len(job_links)} 个可能职位链接')
    if job_links:
        print('前5个链接:')
        for i, (text, href) in enumerate(job_links[:5], 1):
            print(f'  {i}. {text}... -> {href[:50]}...')
    
    # 查找特定的class模式
    print('\n查找常见的选择器模式:')
    common_selectors = [
        '.j_joblist',
        '.dw_table',
        '.joblist',
        '.job_item',
        '.el',
        '.e',
        '.jname',
        '.cname',
        '.sal',
        '.d.at',
        '.jtag',
        '.t1',
        '.t2'
    ]
    
    for selector in common_selectors:
        elements = soup.select(selector)
        if elements:
            print(f'  {selector}: 找到 {len(elements)} 个元素')
            if len(elements) > 0:
                # 显示第一个元素的部分内容
                elem = elements[0]
                text = elem.get_text().strip()[:50]
                if text:
                    print(f'    示例: {text}...')
    
    print('\n分析完成，已保存到: 51job_analysis.html')
    
except Exception as e:
    print(f'错误: {e}')
    import traceback
    traceback.print_exc()