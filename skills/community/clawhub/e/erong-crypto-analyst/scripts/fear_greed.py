#!/usr/bin/env python3
"""
Crypto Fear & Greed Index
Fetches the current Fear & Greed index from alternative.me
"""

import sys
import requests
import argparse
import json

def get_fear_greed():
    url = "https://api.alternative.me/fng/"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        return data['data'][0] if data.get('data') else None
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

def value_to_emoji(value: int) -> str:
    if value >= 80: return '🔴 极度贪婪'
    elif value >= 60: return '🟠 贪婪'
    elif value >= 40: return '🟡 中性'
    elif value >= 20: return '🔵 恐惧'
    else: return '🔵 极度恐惧'

def value_to_color(value: int) -> str:
    if value >= 60: return '🟢'
    elif value >= 40: return '🟡'
    else: return '🔴'

def main():
    data = get_fear_greed()

    if not data:
        print('无法获取恐惧贪婪指数', file=sys.stderr)
        sys.exit(1)

    value = int(data['value'])
    classification = data['value_classification']
    timestamp = data['timestamp']
    from datetime import datetime
    date = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M')

    bar_len = 20
    filled = int(value / 100 * bar_len)
    bar = '█' * filled + '░' * (bar_len - filled)

    print(f'''
╔══════════════════════════════════════╗
║      加密市场恐惧 & 贪婪指数           ║
╠══════════════════════════════════════╣
║  {value:>3}/100  [{bar}]     ║
║  {classification}                       ║
║  更新时间: {date}          ║
╠══════════════════════════════════════╣
║  交易建议:                              ''')

    if value >= 75:
        print('║  ⚠️  极度贪婪 — 考虑减仓/观望      ║')
        print('║  历史高位，市场可能过热            ║')
    elif value >= 60:
        print('║  🟡 贪婪 — 谨慎做多               ║')
        print('║  市场乐观，但有回调风险           ║')
    elif value >= 40:
        print('║  ✅ 中性 — 观望为主               ║')
        print('║  无明显方向，等待信号             ║')
    elif value >= 20:
        print('║  🔵 恐惧 — 可考虑定投建仓         ║')
        print('║  市场恐慌可能是买入机会           ║')
    else:
        print('║  🔵 极度恐惧 — 积极定投/长线布局  ║')
        print('║  历史低位，适合逆向布局           ║')

    print('╚══════════════════════════════════════╝')

if __name__ == '__main__':
    main()
