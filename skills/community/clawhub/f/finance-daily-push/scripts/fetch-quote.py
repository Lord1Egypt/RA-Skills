#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯财经 API 行情数据获取脚本
用于获取 A 股实时行情数据
"""

import requests
import sys
from datetime import datetime

def fetch_quotes(symbols):
    """
    获取腾讯财经 API 行情数据
    
    Args:
        symbols: 股票代码列表，如 ['sh000001', 'sz399006']
    
    Returns:
        dict: 行情数据字典
    """
    url = f'http://qt.gtimg.cn/q={",".join(symbols)}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://finance.qq.com'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f'数据获取失败，状态码：{response.status_code}', file=sys.stderr)
            return None
        
        content = response.content.decode('gbk')
        quotes = {}
        
        for line in content.strip().split('\n'):
            if '=' in line:
                # 解析：v_sh000001="51~上证指数~000001~4086.30~4049.91~..."
                data_part = line.split('"')[1] if '"' in line else line
                parts = data_part.split('~')
                
                if len(parts) > 10:
                    symbol = line.split('=')[0].replace('v_', '')
                    name = parts[1]
                    current = float(parts[3])
                    yesterday = float(parts[4])
                    change = current - yesterday
                    percent = (change / yesterday) * 100
                    
                    quotes[symbol] = {
                        'name': name,
                        'current': current,
                        'change': change,
                        'percent': percent,
                        'time': datetime.now().strftime('%H:%M')
                    }
        
        return quotes
        
    except Exception as e:
        print(f'获取行情数据异常：{e}', file=sys.stderr)
        return None


def main():
    """主函数"""
    # 默认获取主要指数
    default_symbols = [
        'sh000001',  # 上证指数
        'sz399006',  # 创业板指
        'sz399001',  # 深证成指
        'sh000016',  # 上证 50
        'sh000688',  # 科创 50
    ]
    
    # 从命令行参数获取股票代码
    if len(sys.argv) > 1:
        symbols = sys.argv[1].split(',')
    else:
        symbols = default_symbols
    
    quotes = fetch_quotes(symbols)
    
    if quotes:
        print(f'【来源：腾讯财经，{datetime.now().strftime("%H:%M")} 实时】')
        print('=' * 70)
        print('A 股主要指数')
        print('=' * 70)
        
        for symbol, data in quotes.items():
            print(f'{data["name"]:<10} {data["current"]:>10.2f}  '
                  f'涨跌：{data["change"]:+>8.2f} ({data["percent"]:+>7.2f}%)')
    else:
        print('数据获取失败', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
