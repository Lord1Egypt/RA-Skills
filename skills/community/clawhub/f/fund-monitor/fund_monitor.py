#!/usr/bin/env python3
"""基金监控 - 获取东方财富基金数据"""

import requests
import re
import json
import sys
from datetime import datetime

def get_fund_data(fund_code):
    """获取基金数据 - 方法1：东方财富API"""
    url = f"https://fund.eastmoney.com/pingzhongdata/{fund_code}.js"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Referer': 'https://fund.eastmoney.com/'
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        text = resp.text
        
        # 提取基金名称
        name_match = re.search(r'fS_name\s*=\s*"([^"]+)"', text)
        name = name_match.group(1) if name_match else ""
        
        # 提取最新净值和日期 - 从Data_netWorthTrend最后一条
        trend_match = re.search(r'Data_netWorthTrend\s*=\s*(\[.*?\]);', text)
        if trend_match:
            trend_data = json.loads(trend_match.group(1))
            if trend_data:
                latest = trend_data[-1]
                # 转换时间戳
                timestamp = latest['x'] / 1000
                date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                nav = latest['y']
        
        # 提取日涨幅 - 从第一个数据点获取
        if trend_match and len(trend_data) >= 2:
            yesterday = trend_data[-2]
            yesterday_nav = yesterday['y']
            daily_change = ((nav - yesterday_nav) / yesterday_nav) * 100
        
        # 提取阶段涨幅
        syl_1n = re.search(r'syl_1n\s*=\s*"([^"]+)"', text)  # 近1年
        syl_6y = re.search(r'syl_6y\s*=\s*"([^"]+)"', text)  # 近6月
        syl_3y = re.search(r'syl_3y\s*=\s*"([^"]+)"', text)  # 近3月
        syl_1y = re.search(r'syl_1y\s*=\s*"([^"]+)"', text)  # 近1月
        
        return {
            'code': fund_code,
            'name': name,
            'date': date_str,
            'nav': nav,
            'daily_change': daily_change,
            'change_1y': float(syl_1y.group(1)) if syl_1y else None,
            'change_3y': float(syl_3y.group(1)) if syl_3y else None,
            'change_6y': float(syl_6y.group(1)) if syl_6y else None,
            'change_1n': float(syl_1n.group(1)) if syl_1n else None,
        }
        
    except Exception as e:
        return {'error': str(e)}

def search_fund_by_web(fund_code):
    """获取基金数据 - 方法2：Web Search备选"""
    # 使用天天基金搜索页面
    url = f"https://fund.eastmoney.com/{fund_code}.html"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Referer': 'https://fund.eastmoney.com/'
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        text = resp.text
        
        # 从页面提取净值数据
        # 格式: (2026-02-25) 1.6885-0.65%
        match = re.search(r'\((\d{4}-\d{2}-\d{2})\)\s*([0-9.]+)([+-]?[\d.]+)%', text)
        if match:
            date_str, nav, daily_change = match.groups()
            return {
                'code': fund_code,
                'date': date_str,
                'nav': float(nav),
                'daily_change': float(daily_change),
                'method': 'web'
            }
        
        return {'error': 'No data found'}
        
    except Exception as e:
        return {'error': str(e)}

def main():
    if len(sys.argv) < 2:
        print("Usage: fund_monitor.py <fund_code>")
        sys.exit(1)
    
    fund_codes = sys.argv[1:]  # 支持多个基金代码
    
    if not fund_codes:
        print("Usage: fund_monitor.py <fund_code1> <fund_code2> ...")
        sys.exit(1)
    
    for fund_code in fund_codes:
        print(f"\n{'='*40}")
        # 方法1：直接API
        data = get_fund_data(fund_code)
        
        # 如果方法1失败，尝试方法2
        if 'error' in data:
            print(f"{fund_code} 方法1失败，尝试方法2...")
            data = search_fund_by_web(fund_code)
        
        if 'error' in data:
            print(f"Error: {data['error']}")
            continue
        
        print(f"基金代码: {data['code']}")
        print(f"基金名称: {data['name']}")
        print(f"日期: {data['date']}")
        print(f"净值: {data['nav']:.4f}")
        print(f"日涨跌: {data['daily_change']:+.2f}%")
        print(f"近1月: {data['change_1y']:+.2f}%" if data['change_1y'] else "近1月: N/A")
        print(f"近3月: {data['change_3y']:+.2f}%" if data['change_3y'] else "近3月: N/A")
        print(f"近6月: {data['change_6y']:+.2f}%" if data['change_6y'] else "近6月: N/A")
        print(f"近1年: {data['change_1n']:+.2f}%" if data['change_1n'] else "近1年: N/A")

if __name__ == "__main__":
    main()
