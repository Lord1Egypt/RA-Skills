#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
港股分析工具 - 使用富途数据源
"""

import sys
import re

def get_futu_url(code):
    """生成富途股票URL"""
    code = code.strip().upper()
    # 移除HK后缀
    for suffix in ['.HK', 'HK', '-HK']:
        code = code.replace(suffix, '')
    
    # 港股代码处理
    if len(code) == 4:
        code = '0' + code
    elif len(code) != 5:
        return None
    
    return f"https://www.futunn.com/stock/{code}-HK"

def analyze_hk_stock(code):
    """
    分析港股 - 返回富途URL供用户访问
    """
    url = get_futu_url(code)
    
    if not url:
        print(f"错误: 无效的股票代码 {code}")
        print("港股代码应为5位数，例如: 03998, 01833, 06060")
        return
    
    print("="*60)
    print(f"  港股分析工具 v2.1 - 富途数据源")
    print("="*60)
    print(f"\n股票代码: {code}")
    print(f"\n请访问富途获取实时数据:")
    print(f"\n  {url}")
    print(f"\n或直接告诉我股票代码，我帮您查询富途实时数据")
    print("="*60)

def get_stock_info_from_text(text):
    """
    从富途页面文本中解析股票信息
    需要配合浏览器工具使用
    """
    info = {}
    
    # 解析价格
    price_match = re.search(r'(\d+\.\d+)', text)
    if price_match:
        info['price'] = price_match.group(1)
    
    # 解析涨跌幅
    change_match = re.search(r'([+-]?\d+\.\d+)%', text)
    if change_match:
        info['change_pct'] = change_match.group(1)
    
    return info

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python futu_hk.py <港股代码>")
        print("示例: python futu_hk.py 03998")
        print("      python futu_hk.py 01833")
        sys.exit(1)
    
    analyze_hk_stock(sys.argv[1])
