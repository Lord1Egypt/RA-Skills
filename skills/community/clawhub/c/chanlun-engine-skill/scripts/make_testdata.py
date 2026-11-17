#!/usr/bin/env python3
"""生成合成日K testdata.csv (600根, 趋势+回调+噪声, 可形成完整缠论结构) — 无真实数据时自测用"""
import math, random, datetime, sys
random.seed(42)
rows = ["date,open,high,low,close,volume"]
price, d, n = 10.0, datetime.date(2024, 1, 2), 0
while n < 600:
    if d.weekday() < 5:
        drift = 0.004 * math.sin(n / 40.0) + (0.002 if (n // 120) % 2 == 0 else -0.0015)
        ret = drift + random.gauss(0, 0.018)
        o = price; c = max(0.5, price * (1 + ret))
        h = max(o, c) * (1 + abs(random.gauss(0, 0.006)))
        l = min(o, c) * (1 - abs(random.gauss(0, 0.006)))
        rows.append(f"{d.isoformat()},{o:.2f},{h:.2f},{l:.2f},{c:.2f},{random.randint(100000,900000)}")
        price = c; n += 1
    d += datetime.timedelta(days=1)
open("testdata.csv", "w").write("\n".join(rows))
print(f"testdata.csv written ({n} bars)")
