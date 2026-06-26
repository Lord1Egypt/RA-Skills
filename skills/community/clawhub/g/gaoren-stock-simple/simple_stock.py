#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票简单查询工具 v1
A股/港股/美股实时行情
"""

import sys
import requests
import re

def get_a_stock(code):
    """获取A股行情"""
    if len(code) != 6 or not code.isdigit():
        return None
    
    market = 'sh' + code if code.startswith('6') else 'sz' + code
    url = f'https://qt.gtimg.cn/q={market}'
    
    try:
        r = requests.get(url, timeout=5)
        text = r.text.strip()
        if 'none_match' in text:
            return None
        
        match = re.search(r'"([^"]+)"', text)
        if not match:
            return None
        
        parts = match.group(1).split('~')
        if len(parts) < 10:
            return None
        
        return {
            'name': parts[1],
            'price': float(parts[3]),
            'change': float(parts[31]),
            'currency': 'CNY'
        }
    except:
        return None

def get_hk_stock(code):
    """获取港股行情"""
    code = code.upper().replace('.HK', '').replace('HK', '')
    if len(code) == 4:
        code = '0' + code
    
    url = f'https://qt.gtimg.cn/q=hk{code}'
    
    try:
        r = requests.get(url, timeout=5)
        text = r.text.strip()
        if 'none_match' in text:
            return None
        
        match = re.search(r'"([^"]+)"', text)
        if not match:
            return None
        
        parts = match.group(1).split('~')
        if len(parts) < 10:
            return None
        
        open_price = float(parts[9])
        change = ((float(parts[3]) - open_price) / open_price) * 100 if open_price else 0
        
        return {
            'name': parts[1],
            'price': float(parts[3]),
            'change': change,
            'currency': 'HKD'
        }
    except:
        return None

def get_us_stock(code):
    """获取美股行情"""
    FINNHUB_KEY = 'd6nucg1r01qse5qn5e90d6nucg1r01qse5qn5e9g'
    url = f'https://finnhub.io/api/v1/quote?symbol={code.upper()}&token={FINNHUB_KEY}'
    
    try:
        r = requests.get(url, timeout=5).json()
        if r.get('c'):
            return {
                'name': code.upper(),
                'price': r['c'],
                'change': r.get('dp', 0),
                'currency': 'USD'
            }
    except:
        pass
    return None

def query_stock(code):
    """查询股票"""
    # 尝试获取
    data = get_a_stock(code) or get_hk_stock(code) or get_us_stock(code)
    
    if not data:
        print(f"未找到股票: {code}")
        return
    
    # 输出
    print("="*50)
    print(f"【{data['name']}】{code}")
    print("-"*50)
    print(f"价格: {data['price']:.2f} {data['currency']}")
    print(f"涨跌: {data['change']:+.2f}%")
    print("="*50)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python simple_stock.py <股票代码>")
        sys.exit(1)
    
    query_stock(sys.argv[1])
