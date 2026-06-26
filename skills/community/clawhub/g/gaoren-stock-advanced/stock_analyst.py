#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stock Analyst - 智能股票分析
支持港股/美股实时行情 + 新闻 + 智能分析
"""

import sys
import requests
import re
import os

# 股票代码映射
HK_STOCKS = {
    '2618': '京东物流', '01826': '京东物流', '02618': '京东物流',
    '9618': '京东集团', '09618': '京东集团',
    '700': '腾讯', '00700': '腾讯',
    '9988': '阿里巴巴', '09988': '阿里巴巴',
    '3690': '美团', '03690': '美团',
    '1810': '小米', '01810': '小米',
    '2318': '平安保险', '02318': '平安保险',
    '1299': '友邦保险', '01299': '友邦保险',
    '0005': '汇丰控股', '00005': '汇丰控股',
}

US_STOCKS = {
    'JD': '京东',
    'BABA': '阿里巴巴',
    'TCEHY': '腾讯',
    'TSLA': '特斯拉',
    'AAPL': '苹果',
    'MSFT': '微软',
    'GOOGL': '谷歌',
    'AMZN': '亚马逊',
    'META': 'Meta',
    'NVDA': '英伟达',
}

FINNHUB_KEY = os.environ.get('FINNHUB_API_KEY', 'd6nucg1r01qse5qn5e90d6nucg1r01qse5qn5e9g')

def get_hk_stock(code):
    """获取港股行情"""
    # 标准化代码
    code = code.strip().upper()
    
    # 去除常见后缀
    for suffix in ['.HK', 'HK', '.HK']:
        code = code.replace(suffix, '')
    
    # 补齐到5位
    if len(code) == 4:
        code = '0' + code
    elif len(code) == 3:
        code = '00' + code
    
    # 尝试多个代码变体
    for hk_code in [f'hk{code}', f'hk0{code}', f'hk00{code}']:
        try:
            url = f'https://qt.gtimg.cn/q={hk_code}'
            r = requests.get(url, timeout=8)
            text = r.text.strip()
            
            if 'none_match' in text:
                continue
            
            # 解析数据
            match = re.search(r'"([^"]+)"', text)
            if not match:
                continue
                
            parts = match.group(1).split('~')
            if len(parts) < 10:
                continue
            
            name = parts[1]  # 股票名称
            current = float(parts[3])
            high = float(parts[4])
            low = float(parts[5])
            volume = float(parts[6])
            open_p = float(parts[9])
            
            # 如果名称是乱码，尝试从映射获取
            if name.encode('utf-8') == name.encode('gbk', errors='ignore'):
                name = HK_STOCKS.get(code.replace('0', '').replace('hk', ''), name)
            
            return {
                'market': '港股',
                'code': code,
                'name': name,
                'current': current,
                'high': high,
                'low': low,
                'open': open_p,
                'volume': volume,
                'change': current - open_p,
                'change_pct': ((current - open_p) / open_p) * 100 if open_p else 0
            }
        except Exception as e:
            continue
    
    return None

def get_us_stock(code):
    """获取美股行情"""
    code = code.strip().upper()
    code = US_STOCKS.get(code, code)
    
    try:
        url = f'https://finnhub.io/api/v1/quote?symbol={code}&token={FINNHUB_KEY}'
        r = requests.get(url, timeout=10).json()
        
        if r.get('c'):  # current price
            return {
                'market': '美股',
                'code': code,
                'name': US_STOCKS.get(code, code),
                'current': r['c'],
                'high': r['h'],
                'low': r['l'],
                'open': r['o'],
                'volume': r['v'] if 'v' in r else 0,
                'change': r['d'],
                'change_pct': r['dp']
            }
    except Exception as e:
        print(f"Error: {e}")
    
    return None

def get_news():
    """获取财经新闻"""
    try:
        url = 'https://ai.6551.io/open/free_hot?category=macro'
        r = requests.get(url, timeout=15)
        data = r.json()
        
        if data.get('success'):
            return data['news']['items'][:5]
    except:
        pass
    return []

def format_number(n):
    """格式化数字"""
    if abs(n) >= 1_000_000_000:
        return f"{n/1_000_000_000:.2f}B"
    elif abs(n) >= 1_000_000:
        return f"{n/1_000_000:.2f}M"
    elif abs(n) >= 1_000:
        return f"{n/1_000:.2f}K"
    return f"{n:.2f}"

def analyze_stock(code):
    """分析股票"""
    print("="*65)
    print(" "*15 + "股票全面分析")
    print("="*65)
    
    # 尝试港股
    hk_data = get_hk_stock(code)
    
    # 尝试美股
    us_data = get_us_stock(code)
    
    data = hk_data or us_data
    
    if not data:
        print(f"\n无法获取 {code} 的行情数据")
        print("\n提示: 港股代码如 02618, 00700, 09988")
        print("      美股代码如 JD, BABA, TSLA, AAPL")
        return
    
    # 打印行情
    print(f"\n【{data['name']}】{data['code']} ({data['market']})")
    print("-"*65)
    print(f"  当前价格:  {data['current']:.2f} {'HKD' if data['market']=='港股' else 'USD'}")
    print(f"  涨跌额:    {data['change']:+.2f} ({data['change_pct']:+.2f}%)")
    print(f"  开盘:      {data['open']:.2f}")
    print(f"  最高:      {data['high']:.2f}")
    print(f"  最低:      {data['low']:.2f}")
    print(f"  成交量:    {format_number(data['volume'])}")
    
    # 计算技术指标
    if data['open'] > 0:
        today_range = data['high'] - data['low']
        distance_from_high = ((data['high'] - data['current']) / data['high']) * 100
        distance_from_low = ((data['current'] - data['low']) / data['low']) * 100
        
        print(f"\n【技术指标】")
        print(f"  今日振幅:  {today_range:.2f} ({today_range/data['open']*100:.1f}%)")
        print(f"  距高点:    {distance_from_high:.1f}%")
        print(f"  距低点:    {distance_from_low:.1f}%")
        
        # 简单判断
        if data['change_pct'] > 2:
            print(f"  状态:      强势上涨")
        elif data['change_pct'] > 0:
            print(f"  状态:      小幅上涨")
        elif data['change_pct'] < -2:
            print(f"  状态:      明显下跌")
        elif data['change_pct'] < 0:
            print(f"  状态:      小幅回调")
        else:
            print(f"  状态:      横盘整理")
    
    # 新闻
    print(f"\n【财经热点】")
    news = get_news()
    if news:
        for i, item in enumerate(news, 1):
            title = item.get('title', '')[:50]
            source = item.get('source', '')
            signal = item.get('signal', 'neutral')
            print(f"  {i}. [{source}] {title}...")
    else:
        print("  暂无新闻")
    
    print("\n" + "="*65)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: stock_analyst.py <股票代码>")
        print("示例: stock_analyst.py 02618")
        print("      stock_analyst.py JD")
        sys.exit(1)
    
    analyze_stock(sys.argv[1])
