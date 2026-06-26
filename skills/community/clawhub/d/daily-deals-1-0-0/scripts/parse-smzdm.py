#!/usr/bin/env python3
"""
什么值得买 HTML 解析器 v2
支持多种页面格式（搜索页/汇总页/分类页）
"""
import re
import json
import sys

def parse_smzdm_html(html_path):
    with open(html_path, 'r') as f:
        html = f.read()
    
    deals = []
    
    # 模式 1: 商品链接 + 标题（搜索页）
    link_pattern1 = r'<a[^>]*href="[^"]*p/(\d+)[^"]*"[^>]*>([^<]+)'
    # 模式 2: 价格
    price_pattern = r'>([^<]*\d+\.?\d*元[^<]*)<'
    
    links = re.findall(link_pattern1, html)
    prices = re.findall(price_pattern, html)
    
    for i, (pid, title) in enumerate(links[:30]):
        title = title.strip()
        # 过滤无效标题
        if len(title) < 8 or len(title) > 120:
            continue
        if any(x in title for x in ['京东', '天猫', '拼多多', '优惠券', '红包', '外卖', '推荐', '券', '促销']):
            continue
        # 过滤特殊字符过多的
        if title.count('&') > 2 or title.count(';') > 2:
            continue
        
        # 获取价格
        price = prices[i] if i < len(prices) else '价格面议'
        price = price.strip()
        if len(price) > 60:  # 价格信息过长，截断
            price = price[:60] + '...'
        
        # 判断平台
        platform = '什么值得买'
        title_lower = title.lower()
        if '京东' in title:
            platform = '京东'
        elif '天猫' in title:
            platform = '天猫'
        elif '拼多多' in title or '百亿补贴' in title:
            platform = '拼多多'
        elif '淘宝' in title:
            platform = '淘宝'
        
        deals.append({
            'title': title,
            'price': price,
            'platform': platform,
            'url': f'https://www.smzdm.com/p/{pid}/'
        })
        
        if len(deals) >= 10:
            break
    
    return deals

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps([]))
        sys.exit(0)
    
    html_path = sys.argv[1]
    deals = parse_smzdm_html(html_path)
    print(json.dumps(deals, ensure_ascii=False))
