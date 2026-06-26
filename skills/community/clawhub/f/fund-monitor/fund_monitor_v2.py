#!/usr/bin/env python3
"""基金监控 V2 - 获取东方财富基金数据，支持持仓计算和投资建议"""

import requests
import re
import json
import sys
from datetime import datetime

# 22只基金代码
FUND_CODES = [
    "017745", "002834", "018412", "025857", "008888", "011609", 
    "021894", "025209", "021533", "018195", "020357", "010990", 
    "016874", "016858", "020105", "015897", "022328", "004433", 
    "016450", "017994", "019571", "025491"
]

# 持仓数据
# 持仓数据 (2026-02-13)
# amount: 持仓金额（市值）, cost: 成本金额（本金）
HOLDINGS = {
    "017745": {"amount": 27366.18, "cost": 25000.00},
    "002834": {"amount": 15815.61, "cost": 14405.19},
    "018412": {"amount": 13353.88, "cost": 13000.00},
    "025857": {"amount": 3814.24, "cost": 3563.01},
    "008888": {"amount": 14249.14, "cost": 14000.00},
    "011609": {"amount": 17223.77, "cost": 17000.00},
    "021894": {"amount": 11169.87, "cost": 11000.00},
    "025209": {"amount": 20157.11, "cost": 20000.00},
    "021533": {"amount": 8101.91, "cost": 8000.00},
    "018195": {"amount": 4793.39, "cost": 4693.62},
    "020357": {"amount": 13095.07, "cost": 13000.00},
    "010990": {"amount": 6538.28, "cost": 6461.06},
    "016874": {"amount": 1020.06, "cost": 1000.00},
    "016858": {"amount": 510.17, "cost": 500.00},
    "020105": {"amount": 100.32, "cost": 100.00},
    "015897": {"amount": 97.96, "cost": 100.00},
    "022328": {"amount": 985.15, "cost": 1000.00},
    "004433": {"amount": 2636.22, "cost": 2680.10},
    "016450": {"amount": 945.92, "cost": 1000.00},
    "017994": {"amount": 8901.05, "cost": 9000.00},
    "019571": {"amount": 9770.38, "cost": 10000.00},
    "025491": {"amount": 14515.97, "cost": 17000.00},
}

def get_fund_data(fund_code):
    url = f"https://fund.eastmoney.com/pingzhongdata/{fund_code}.js"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Referer': 'https://fund.eastmoney.com/'
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        text = resp.text
        
        name_match = re.search(r'fS_name\s*=\s*"([^"]+)"', text)
        name = name_match.group(1) if name_match else ""
        
        trend_match = re.search(r'Data_netWorthTrend\s*=\s*(\[.*?\]);', text, re.DOTALL)
        if trend_match:
            trend_data = json.loads(trend_match.group(1))
            if trend_data:
                latest = trend_data[-1]
                timestamp = latest['x'] / 1000
                date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                nav = latest['y']
                
                if len(trend_data) >= 2:
                    yesterday = trend_data[-2]
                    yesterday_nav = yesterday['y']
                    daily_change = ((nav - yesterday_nav) / yesterday_nav) * 100
                else:
                    daily_change = 0
        
        def getSyl(key):
            m = re.search(rf'{key}\s*=\s*"([^"]+)"', text)
            return float(m.group(1)) if m else None
        
        return {
            'code': fund_code,
            'name': name,
            'date': date_str,
            'nav': nav,
            'daily_change': daily_change,
            'change_1y': getSyl('syl_1y'),
            'change_3y': getSyl('syl_3y'),
            'change_6y': getSyl('syl_6y'),
            'change_1n': getSyl('syl_1n'),
        }
    except Exception as e:
        return {'code': fund_code, 'error': str(e)}

def main():
    funds_data = []
    
    print("=" * 60)
    print("📊 基金监控 - 22只基金每日涨跌")
    print("=" * 60)
    
    for code in FUND_CODES:
        data = get_fund_data(code)
        funds_data.append(data)
    
    funds = [d for d in funds_data if 'error' not in d]
    funds.sort(key=lambda x: x.get('daily_change', 0), reverse=True)
    
    print("\n" + "=" * 60)
    print("📈 上涨基金 (共{}只)".format(len([f for f in funds if f.get('daily_change', 0) >= 0])))
    print("=" * 60)
    
    for f in funds:
        if f.get('daily_change', 0) >= 0:
            print(f"  ✅ {f['name'][:22]:<24} {f['daily_change']:+.2f}%")
    
    print("\n" + "=" * 60)
    print("📉 下跌基金 (共{}只)".format(len([f for f in funds if f.get('daily_change', 0) < 0])))
    print("=" * 60)
    
    for f in funds:
        if f.get('daily_change', 0) < 0:
            print(f"  ❌ {f['name'][:22]:<24} {f['daily_change']:+.2f}%")
    
    print("\n" + "=" * 60)
    print("💰 账户收益估算")
    print("=" * 60)
    
    total_today = 0
    total_cost = 0  # 总本金
    total_value = 0  # 总市值
    
    for f in funds:
        code = f['code']
        if code in HOLDINGS:
            holding = HOLDINGS[code]
            amount = holding['amount']  # 当前市值
            cost = holding['cost']  # 成本本金
            daily_change = f.get('daily_change', 0)
            today_gain = cost * daily_change / 100
            total_today += today_gain
            total_cost += cost
            total_value += amount
    
    total_return = total_value - total_cost
    total_return_pct = (total_return / total_cost * 100) if total_cost > 0 else 0
    
    # 实际总收益 = 持仓收益 + 今日收益变化
    total_actual_return = total_return + total_today
    total_actual_return_pct = (total_actual_return / total_cost * 100) if total_cost > 0 else 0
    
    print(f"今日收益变化: {total_today:+.2f} 元")
    print(f"持仓总收益: {total_return:+.2f} 元")
    print(f"实际总收益(含今日): {total_actual_return:+.2f} 元")
    print(f"总本金: {total_cost:.2f} 元")
    print(f"总市值: {total_value:.2f} 元")
    print(f"总收益率(含今日): {total_actual_return_pct:+.2f}%")
    
    print("\n" + "=" * 60)
    print("💡 投资建议")
    print("=" * 60)
    
    up_count = len([f for f in funds if f.get('daily_change', 0) >= 0])
    down_count = 22 - up_count
    
    print(f"今日涨跌: 涨 {up_count} 只, 跌 {down_count} 只")
    
    if up_count > down_count:
        print("📈 市场整体偏多，建议继续持有")
    else:
        print("📉 市场整体偏空，可考虑逢低加仓")
    
    best = funds[0]
    worst = funds[-1]
    print(f"\n🔥 今日最佳: {best['name'][:15]} ({best['daily_change']:+.2f}%)")
    print(f"💩 今日最差: {worst['name'][:15]} ({worst['daily_change']:+.2f}%)")

if __name__ == "__main__":
    main()
