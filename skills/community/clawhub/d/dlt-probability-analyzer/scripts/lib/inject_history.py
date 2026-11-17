# -*- coding: utf-8 -*-
"""一次性补录 26114 / 26115 真实开奖结果到 dlt_history.json。
数据来源：联网核实（上海体彩网 / 中国体彩网 / 天齐网 / 广东体彩网 多源一致）。
仅追加缺失期，不修改任何已有条目。
"""
import os, json

W = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(W, 'dlt_history.json')
hist = json.load(open(p, encoding='utf-8'))
existing = {d['period'] for d in hist}

new_entries = [
    {'period': '26114', 'date': '2026-10-07', 'open_time': '2026-10-07 21:25:00',
     'front': [8, 12, 15, 29, 30], 'back': [9, 12]},
    {'period': '26115', 'date': '2026-10-10', 'open_time': '2026-10-10 21:25:00',
     'front': [12, 20, 32, 33, 35], 'back': [6, 7]},
]

added = []
for e in new_entries:
    if e['period'] in existing:
        print('SKIP 已存在:', e['period'])
        continue
    # 格式校验
    assert len(e['front']) == 5 and len(set(e['front'])) == 5 and all(1 <= n <= 35 for n in e['front'])
    assert len(e['back']) == 2 and len(set(e['back'])) == 2 and all(1 <= n <= 12 for n in e['back'])
    hist.append(e)
    existing.add(e['period'])
    added.append(e['period'])

hist.sort(key=lambda x: x['period'])
json.dump(hist, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('已追加:', added)
print('历史库总期数:', len(hist))
print('最新期:', hist[-1]['period'], hist[-1]['date'], hist[-1]['front'], hist[-1]['back'])
