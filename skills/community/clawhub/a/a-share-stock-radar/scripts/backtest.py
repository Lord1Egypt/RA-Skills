#!/usr/bin/env python3
"""
4 形态历史回测（把「感觉」变成「数据」）

对给定股票池的日K，逐日检测 playbook 的 4 形态，统计：
  - 次日最高 ≥ 入场价×1.03 的达标率（老板的短线口径）
  - 次日/未来5日最大涨幅、平均

用法:
  python3 .../backtest.py                       # 默认池 + 近 180 日
  python3 .../backtest.py --days 120 --codes 002487,603667,300285
  python3 .../backtest.py --pool-file trading/watchlist.txt --days 250
数据源：新浪日K(scale=240) → 失败落腾讯 ifzq 日K。
"""
import argparse
import json
import statistics
import sys
import urllib.parse

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from radar_common import http_get, http_json, sina_symbol, tencent_quote_symbol  # noqa: E402

SINA_K = ("https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData"
          "?symbol={sym}&scale=240&ma=no&datalen={n}")
TX_K = "https://ifzq.gtimg.cn/appstock/app/fqkline/get?param={sym},day,,,{n},qfq"

DEFAULT_POOL = [
    "002487", "603667", "300285", "601218", "002553", "002164", "300207", "600699",
    "002594", "300750", "300124", "601012", "600438", "002459", "300274", "688981",
    "002415", "300496", "002230", "300308", "300502", "002281", "600036", "601398",
    "601288", "600030", "300059", "601688", "600519", "000858", "000568", "600276",
    "300760", "300347", "603259", "688180", "002049", "603501", "600584", "002156",
    "601633", "600104", "000625", "600066", "002048", "601127", "600699", "603197",
]


def fetch_daily(code, n=250):
    sym = sina_symbol(code)
    try:
        txt = http_get(SINA_K.format(sym=sym, n=n), referer="https://finance.sina.com.cn/")
        arr = json.loads(txt)
        return [{"date": x["day"][:10], "open": float(x["open"]), "high": float(x["high"]),
                 "low": float(x["low"]), "close": float(x["close"]), "vol": float(x["volume"])}
                for x in arr]
    except Exception:
        pass
    tsym = tencent_quote_symbol(code)
    obj = http_json(TX_K.format(sym=tsym, n=n), referer="https://gu.qq.com/")
    data = obj.get("data", {}).get(tsym, {})
    rows = data.get("qfqday") or data.get("day") or []
    return [{"date": r[0], "open": float(r[1]), "close": float(r[2]), "high": float(r[3]),
             "low": float(r[4]), "vol": float(r[5])} for r in rows]


def _ma(vals, n, i):
    if i + 1 < n:
        return None
    return sum(vals[i + 1 - n:i + 1]) / n


def detect(bars, i):
    """返回该日命中的形态列表（i 为当前日）。"""
    if i < 25:
        return []
    b = bars[i]
    prev = bars[:i]
    o, c, h, l, v = b["open"], b["close"], b["high"], b["low"], b["vol"]
    if o <= 0 or c <= 0:
        return []
    pct = (c / prev[-1]["close"] - 1) * 100
    vols = [x["vol"] for x in prev]
    vma5 = sum(vols[-5:]) / 5 if len(vols) >= 5 else v
    hits = []

    # 1) 一阳穿三阴：前3根阴线，今日阳线实体吞没其区间
    if len(prev) >= 3:
        last3 = prev[-3:]
        if all(x["close"] < x["open"] for x in last3) and c > o:
            top3 = max(x["open"] for x in last3)
            if o < min(x["close"] for x in last3) and c > top3 and pct >= 2:
                hits.append("一阳穿三阴")

    # 2) 平台突破VCP：近10日振幅收窄(<=8%)，今日放量突破10日高
    win = prev[-10:]
    if len(win) == 10:
        hi10 = max(x["high"] for x in win[:-1]) if len(win) > 1 else win[0]["high"]
        lo10 = min(x["low"] for x in win)
        if lo10 > 0 and (hi10 - lo10) / lo10 <= 0.10 and c > hi10 and v > vma5 * 1.3 and pct >= 2:
            hits.append("平台突破VCP")

    # 3) N字爆发：近15日内先冲高 → 回调不破前低 → 今日放量再上攻破前高
    if len(prev) >= 15:
        w = prev[-15:]
        seg_hi = max(x["high"] for x in w)
        hi_idx = max(range(len(w)), key=lambda k: w[k]["high"])
        if 3 <= hi_idx <= len(w) - 3:
            after = w[hi_idx + 1:]
            pull_lo = min(x["low"] for x in after) if after else seg_hi
            if seg_hi > 0 and (seg_hi - pull_lo) / seg_hi >= 0.05 and c > seg_hi and v > vma5 * 1.2 and pct >= 3:
                hits.append("N字爆发")

    # 4) 竞价异动(日线近似)：高开>2% 且 收阳走强(收>开) 且 放量
    if len(prev) >= 1:
        pc = prev[-1]["close"]
        if pc > 0 and (o / pc - 1) * 100 >= 2 and c > o and v > vma5 * 1.2:
            hits.append("竞价异动")

    return hits


def backtest_one(code, days=180):
    bars = fetch_daily(code, n=days + 40)
    if len(bars) < 30:
        return []
    recs = []
    start = max(25, len(bars) - days)
    for i in range(start, len(bars) - 1):
        for pat in detect(bars, i):
            entry = bars[i]["close"]
            nxt = bars[i + 1]
            fwd = bars[i + 1:i + 6]
            max1 = (nxt["high"] / entry - 1) * 100
            max5 = (max(x["high"] for x in fwd) / entry - 1) * 100 if fwd else max1
            recs.append({"code": code, "date": bars[i]["date"], "pattern": pat,
                         "next_max": round(max1, 2), "fwd5_max": round(max5, 2),
                         "hit": max1 >= 3.0})
    return recs


def main():
    ap = argparse.ArgumentParser(description="4形态回测")
    ap.add_argument("--days", type=int, default=180)
    ap.add_argument("--codes", default="")
    ap.add_argument("--pool-file", default="")
    a = ap.parse_args()

    if a.codes:
        pool = [c.strip() for c in a.codes.split(",") if c.strip()]
    elif a.pool_file:
        with open(a.pool_file, encoding="utf-8") as f:
            pool = [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]
    else:
        pool = DEFAULT_POOL

    print("回测标的 {} 只 ｜ 近 {} 日".format(len(pool), a.days))
    allrecs = []
    for k, c in enumerate(pool, 1):
        try:
            rs = backtest_one(c, a.days)
            allrecs += rs
            print("  [{}/{}] {} 命中 {} 次".format(k, len(pool), c, len(rs)), flush=True)
        except Exception as e:
            print("  [{}/{}] {} ❌ {}".format(k, len(pool), c, type(e).__name__), flush=True)

    if not allrecs:
        print("无样本"); return 1
    print("\n" + "=" * 56)
    print("分形态胜率（达标 = 次日最高 ≥ 入场价×1.03）")
    print("=" * 56)
    by = {}
    for r in allrecs:
        by.setdefault(r["pattern"], []).append(r)
    print("{:<12} {:>5} {:>8} {:>10} {:>10}".format("形态", "样本", "达标率", "均次日高%", "均5日高%"))
    for pat, rs in sorted(by.items(), key=lambda kv: -sum(x["hit"] for x in kv[1]) / len(kv[1])):
        n = len(rs)
        wr = sum(x["hit"] for x in rs) / n * 100
        print("{:<12} {:>5} {:>7.1f}% {:>10.2f} {:>10.2f}".format(
            pat, n, wr, statistics.mean(x["next_max"] for x in rs), statistics.mean(x["fwd5_max"] for x in rs)))
    n = len(allrecs)
    wr = sum(x["hit"] for x in allrecs) / n * 100
    print("-" * 56)
    print("合计：{} 个信号，达标率 {:.1f}%".format(n, wr))
    return 0


if __name__ == "__main__":
    sys.exit(main())
