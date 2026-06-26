import requests
import json

symbol = 'JD'  # 京东美股
token = 'd6nucg1r01qse5qn5e90d6nucg1r01qse5qn5e9g'

# 1. Get quote
url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={token}'
r = requests.get(url).json()

print('='*50)
print('  股票全面分析: 京东快递 (9628.HK)')
print('='*50)
print()
print('【实时行情】')
print(f"  当前价格: HK${r.get('c', 'N/A')}")
print(f"  涨跌额: HK${r.get('d', 'N/A')}")
print(f"  涨跌幅: {r.get('dp', 'N/A')}%")
print(f"  52周高低: HK${r.get('l', 'N/A')} - HK${r.get('h', 'N/A')}")
print(f"  开盘/高/低/收: {r.get('o', 'N/A')} / {r.get('h', 'N/A')} / {r.get('l', 'N/A')} / {r.get('c', 'N/A')}")
print()

# 2. Get news
news_url = 'https://ai.6551.io/open/free_hot?category=macro'
n = requests.get(news_url).json()

print('【今日财经热点】')
if n.get('success'):
    for i, item in enumerate(n['news']['items'][:5], 1):
        print(f"  {i}. [{item['source']}] {item['title'][:60]}...")
print()
print('='*50)
