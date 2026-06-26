import requests

symbol = '2618.HK'  # 京东物流港股代码
token = 'd6nucg1r01qse5qn5e90d6nucg1r01qse5qn5e9g'

# 1. 实时行情
q = requests.get(f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={token}').json()
print('【实时行情】')
print(f'  当前价格: HK${q.get("c", "N/A")}')
print(f'  涨跌额: HK${q.get("d", "N/A")}')
print(f'  涨跌幅: {q.get("dp", "N/A")}%')
print(f'  52周高低: HK${q.get("l", "N/A")} - HK${q.get("h", "N/A")}')
print(f'  开盘/高/低/收: {q.get("o", "N/A")} / {q.get("h", "N/A")} / {q.get("l", "N/A")} / {q.get("c", "N/A")}')
print()

# 2. 公司信息
c = requests.get(f'https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={token}').json()
print('【公司概况】')
print(f'  名称: {c.get("name", "N/A")}')
print(f'  行业: {c.get("finnhubIndustry", "N/A")}')
print(f'  市值: {c.get("marketCapitalization", "N/A")}M {c.get("currency", "N/A")}')
print(f'  官网: {c.get("weburl", "N/A")}')
print()

# 3. 分析师评级
r = requests.get(f'https://finnhub.io/api/v1/stock/recommendation?symbol={symbol}&token={token}').json()
if r:
    latest = r[0]
    print('【分析师评级】')
    print(f'  强烈买入: {latest.get("strongBuy", 0)}')
    print(f'  买入: {latest.get("buy", 0)}')
    print(f'  持有: {latest.get("hold", 0)}')
    print(f'  卖出: {latest.get("sell", 0)}')
    print(f'  强烈卖出: {latest.get("strongSell", 0)}')
print()
