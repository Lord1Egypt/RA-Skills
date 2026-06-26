#!/usr/bin/env bash
# Market Quotes — A股 + 美股指数实时行情 via 东方财富
set -euo pipefail

python3 << 'PYEOF'
import urllib.request, json
from datetime import datetime

# secids: 1.=沪市 0.=深市 100.=美股
symbols = "1.000001,0.399001,1.000300,1.000688,0.399006,100.NDX,100.DJI,100.SPX"
fields = "f2,f3,f4,f12,f14,f15,f16"

url = f"https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&secids={symbols}&fields={fields}&ut=fa5fd1943c7b386f172d6893dbfba10b"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

try:
    data = json.loads(urllib.request.urlopen(req, timeout=10).read())
    items = data.get("data", {}).get("diff", [])
except Exception as e:
    print(f"行情获取失败: {e}")
    items = []

market_map = {"000001":"沪","399001":"深","000300":"沪","000688":"沪","399006":"深","NDX":"美","DJI":"美","SPX":"美"}

print("\n===== 指数行情 =====")
print()

for item in items:
    code = item.get("f12", "?")
    name = item.get("f14", "?")
    price = item.get("f2", 0)
    chg_pct = item.get("f3", 0)
    chg_val = item.get("f4", 0)

    arrow = "🔺" if chg_pct > 0 else ("🔻" if chg_pct < 0 else "➖")
    sign = "+" if chg_pct > 0 else ""
    mkt = market_map.get(code, "?")

    if isinstance(price, (int, float)):
        ps = f"{price:,.2f}" if price > 1000 else f"{price:.2f}"
    else:
        ps = str(price)

    print(f"{mkt} {name}  {arrow}  {ps}  {sign}{chg_pct:.2f}%")

print()
print("数据来源: 东方财富")
print(f"⏰ {datetime.now().strftime('%m/%d %H:%M')}")
PYEOF
