#!/usr/bin/env python3
"""
ETF 波动监控脚本 v5
使用 腾讯财经 API 获取实时行情（免费、无需 Token、实时）
"""
import requests
import json
import sys

# 监控列表 (腾讯财经格式)
ETF_LIST = [
    ("sz159985", "159985", "豆粕 ETF"),
    ("sz159792", "159792", "港股通互联网 ETF"),
    ("sh515220", "515220", "煤炭 ETF"),
    ("sh513310", "513310", "中韩半导体 ETF"),
    ("sh510050", "510050", "上证 50ETF"),
    ("sz159922", "159922", "中证 500ETF"),
    ("sz159919", "159919", "沪深 300ETF"),
]

THRESHOLD = 1.0  # 波动阈值 1%

def get_realtime_quotes():
    """从腾讯财经获取实时行情"""
    try:
        symbols = ",".join([item[0] for item in ETF_LIST])
        url = f"http://qt.gtimg.cn/q={symbols}"
        
        resp = requests.get(url, timeout=10)
        resp.encoding = 'gbk'
        content = resp.text
        
        quotes = {}
        for line in content.split('\n'):
            if line.strip():
                parts = line.split('=')
                if len(parts) > 1 and parts[1].strip():
                    data = parts[1].strip('"').split('~')
                    if len(data) > 30:
                        # 提取代码
                        code_part = parts[0].replace('v_', '')
                        code = code_part.replace('sz', '').replace('sh', '')
                        
                        current = float(data[3]) if data[3] else 0
                        last_close = float(data[4]) if data[4] else 0
                        
                        pct_chg = ((current - last_close) / last_close * 100) if last_close > 0 else 0
                        
                        quotes[code] = {
                            'price': current,
                            'pct_chg': pct_chg
                        }
        
        return quotes
    except Exception as e:
        print(f"获取行情失败：{e}", file=sys.stderr)
        return {}

def check_volatility():
    """检查 ETF 波动"""
    alerts = []
    quotes = get_realtime_quotes()
    
    for symbol, code, name in ETF_LIST:
        try:
            if code in quotes:
                data = quotes[code]
                pct_chg = data['pct_chg']
                
                if abs(pct_chg) >= THRESHOLD:
                    direction = "📈" if pct_chg > 0 else "📉"
                    alerts.append({
                        'code': code,
                        'name': name,
                        'current': data['price'],
                        'percent': pct_chg,
                        'direction': direction
                    })
        except Exception as e:
            print(f"查询 {name} 失败：{e}", file=sys.stderr)
    
    return alerts

if __name__ == '__main__':
    alerts = check_volatility()
    
    if alerts:
        print(json.dumps({'alerts': alerts}, ensure_ascii=False))
    else:
        print(json.dumps({'alerts': []}, ensure_ascii=False))
