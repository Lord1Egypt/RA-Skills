import requests

token = 'd6nucg1r01qse5qn5e90d6nucg1r01qse5qn5e9g'

# 公司信息
company = requests.get(f'https://finnhub.io/api/v1/stock/profile2?symbol=JD&token={token}').json()
print('【公司基本信息】')
print(f"  名称: {company.get('name', 'N/A')}")
print(f"  行业: {company.get('finnhubIndustry', 'N/A')}")
print(f"  市值: {company.get('marketCapitalization', 'N/A')}M {company.get('currency', 'N/A')}")
print(f"  股份数: {company.get('shareOutstanding', 'N/A')}M")
print(f"  CEO: {company.get('ceo', 'N/A')}")
print(f"  官网: {company.get('weburl', 'N/A')}")
print()

# 股价历史
import time
from datetime import datetime, timedelta

# 最近30天
end_ts = int(datetime.now().timestamp())
start_ts = int((datetime.now() - timedelta(days=45)).timestamp())

candles = requests.get(f'https://finnhub.io/api/v1/stock/candle?symbol=JD&resolution=D&from={start_ts}&to={end_ts}&token={token}').json()

if candles.get('s') == 'ok':
    closes = candles.get('c', [])
    highs = candles.get('h', [])
    lows = candles.get('l', [])
    volumes = candles.get('v', [])
    print('【最近30天走势】')
    print(f"  最高: {max(highs) if highs else 'N/A'}")
    print(f"  最低: {min(lows) if lows else 'N/A'}")
    print(f"  当前收盘: {closes[-1] if closes else 'N/A'}")
    print(f"  30日平均成交量: {sum(volumes)/len(volumes) if volumes else 'N/A':.0f}")
    # 简单计算均线
    if len(closes) >= 5:
        ma5 = sum(closes[-5:])/5
        ma20 = sum(closes[-20:])/20 if len(closes) >= 20 else ma5
        print(f"  5日均线: {ma5:.2f}")
        print(f"  20日均线: {ma20:.2f}")
        # 金叉死叉判断
        if ma5 > ma20:
            print("  📈 均线形态: 金叉 (短期看涨)")
        else:
            print("  📉 均线形态: 死叉 (短期看跌)")
print()

# 分析师评级
rating = requests.get(f'https://finnhub.io/api/v1/stock/recommendation?symbol=JD&token={token}').json()
if rating:
    latest = rating[0] if rating else {}
    print('【分析师评级】')
    print(f"  强烈买入: {latest.get('strongBuy', 0)}")
    print(f"  买入: {latest.get('buy', 0)}")
    print(f"  持有: {latest.get('hold', 0)}")
    print(f"  卖出: {latest.get('sell', 0)}")
    print(f"  强烈卖出: {latest.get('strongSell', 0)}")
print()
