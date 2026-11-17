#!/usr/bin/env python3
"""
30 分钟结构 + 量价背离（比日线更早看到拐点）

用法:
  python3 .../intraday_structure.py <code...>
数据源：新浪 30 分钟K（scale=30），近 ~6 个交易日。
判定：
  - 结构：站上/跌破 30min MA20；近 8 根 HH/HL=上升，LH/LL=下降
  - 量价背离：价创近 16 根新高但量低于前高 → ⚠顶背离；价创新低但量缩 → ⚠底背离(可能止跌)
"""
import argparse
import json
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from radar_common import http_get, sina_symbol  # noqa: E402

URL = ("https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData"
       "?symbol={sym}&scale=30&ma=no&datalen=48")


def analyze(code):
    txt = http_get(URL.format(sym=sina_symbol(code)), referer="https://finance.sina.com.cn/")
    data = json.loads(txt)
    if not isinstance(data, list):
        return None
    bars = [b for b in data if isinstance(b, dict) and "close" in b and "volume" in b]
    if len(bars) < 24:
        return None
    closes = [float(b["close"]) for b in bars]
    vols = [float(b["volume"]) for b in bars]
    last = closes[-1]
    ma20 = sum(closes[-20:]) / 20
    hi8, lo8 = max(closes[-8:]), min(closes[-8:])
    # 结构
    struct = "多头" if last > ma20 and closes[-1] > closes[-8] else ("空头" if last < ma20 else "震荡")
    # 量价背离
    w = 16
    hi_idx = max(range(len(closes) - w, len(closes)), key=lambda i: closes[i])
    div = "-"
    if closes[-1] >= max(closes[-w:]) * 0.999 and vols[-1] < vols[hi_idx] * 0.8:
        div = "⚠️ 顶背离(价新高量不跟)"
    lo_idx = min(range(len(closes) - w, len(closes)), key=lambda i: closes[i])
    if closes[-1] <= min(closes[-w:]) * 1.001 and vols[-1] < vols[lo_idx]:
        div = "🟡 底背离(缩量新低，可能止跌)"
    return {"code": code, "last": last, "ma20": round(ma20, 2), "struct": struct,
            "hi8": hi8, "lo8": lo8, "div": div,
            "range8_pct": round((hi8 - lo8) / lo8 * 100, 2) if lo8 else 0}


def main():
    ap = argparse.ArgumentParser(description="30分钟结构+量价背离")
    ap.add_argument("codes", nargs="+")
    a = ap.parse_args()
    for c in a.codes:
        try:
            r = analyze(c)
            if not r:
                print("{}: 30min 数据不足".format(c)); continue
            print("{code} 30min 现{last} MA20={ma20} 结构={struct} 8根区间{range8_pct}% 背离={div}".format(**r))
        except Exception as e:
            print("{}: ❌ {}".format(c, type(e).__name__))
    return 0


if __name__ == "__main__":
    sys.exit(main())
