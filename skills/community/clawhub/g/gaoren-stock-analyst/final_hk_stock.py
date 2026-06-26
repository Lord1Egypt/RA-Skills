import requests
import re

# 京东物流正确代码: hk02618
symbol = 'hk02618'
name = '京东物流'

url = f'https://qt.gtimg.cn/q={symbol}'
r = requests.get(url, timeout=10)
text = r.text

print("="*60)
print(f"  {name} (02618.HK) 实时行情")
print("="*60)

# 解析
match = re.search(r'"([^"]+)"', text)
if match:
    parts = match.group(1).split('~')
    
    current = float(parts[3])    # 当前价
    high = float(parts[4])       # 最高
    low = float(parts[5])        # 最低
    open_p = float(parts[9])     # 开盘
    volume = float(parts[6])     # 成交量
    
    change = current - open_p
    change_pct = (change / open_p) * 100
    
    print(f"\n  当前价格: HK${current:.2f}")
    print(f"  涨跌额: {change:+.2f} ({change_pct:+.2f}%)")
    print(f"  开盘: {open_p:.2f} | 最高: {high:.2f} | 最低: {low:.2f}")
    print(f"  成交量: {volume:,.0f}")
    print(f"  总成交额: HK${current * volume / 1000000:.2f}M")
    print()

# 获取其他京东系股票
stocks = {
    'hk09618': '京东集团',
    'hk00700': '腾讯',
    'hk09988': '阿里巴巴',
    'hk03690': '美团',
}

print("="*60)
print("  科技/电商热门股")
print("="*60)

for code, nm in stocks.items():
    url = f'https://qt.gtimg.cn/q={code}'
    try:
        r = requests.get(url, timeout=5)
        m = re.search(r'"([^"]+)"', r.text)
        if m:
            p = m.group(1).split('~')
            price = float(p[3])
            open_p = float(p[9])
            vol = float(p[6])
            chg = price - open_p
            chg_pct = (chg / open_p) * 100
            print(f"\n  [{nm}]")
            print(f"    {price:.2f} ({chg_pct:+.2f}%)  Vol: {vol/1000000:.1f}M")
    except:
        pass

print("\n" + "="*60)
