#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
次日开盘复核（留/减/走）—— 对「昨天选出的票」，次日开盘用实时价 + 分时主力做裁决

为什么需要：选股理由里的资金流是**昨日滞后信号**；次日必须用「分时主力 + 价格是否达标/破位」复核，
          在 9:25~10:00 就能给出 留 / 减 / 走。

用法：
  python3 nextday_check.py 600707:9.845:9.58  002204:5.361:5.44
      格式=代码[:买价[:止损]]（买价/止损可省，省了只做价格与资金判断）

  python3 nextday_check.py --file trading/records/2026-09-21.md   # 从留档里解析「代码:买价」自动复核(实验)
判定：
  破止损 → 走；最高≥买价×1.03 → 已达标(可走/减)；主力分时净流出且价<买价 → 偏弱(反弹减)；否则观察。
"""
import sys, json, re, time, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"}
EM = ["push2.eastmoney.com", "1.push2.eastmoney.com", "push2delay.eastmoney.com"]
TARGET = 1.03  # 达标线：次日最高 ≥ 买价×1.03


def secid(code):
    return ("1." if code[0] in "69" else "0.") + str(code)


def sina(code):
    sym = ("sh" if code[0] in "69" else "sz") + str(code)
    req = urllib.request.Request("https://hq.sinajs.cn/list=" + sym,
                                 headers={"User-Agent": UA["User-Agent"], "Referer": "https://finance.sina.com.cn/"})
    raw = urllib.request.urlopen(req, timeout=10).read().decode("gbk", "replace")
    p = raw.split('"')[1].split(",")
    if len(p) < 10 or not p[3]:
        return None
    return {"name": p[0], "open": float(p[1]), "prev": float(p[2]), "price": float(p[3]),
            "high": float(p[4]), "low": float(p[5]), "vol": float(p[8]), "amount": float(p[9])}


def flow_min(code):
    u = ("https://{H}/api/qt/stock/fflow/kline/get?lmt=0&klt=1&secid=%s"
         "&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65" % secid(code))
    last = None
    for k in range(3):
        try:
            req = urllib.request.Request(u.replace("{H}", EM[k % len(EM)]),
                                         headers={**UA, "Referer": "https://quote.eastmoney.com/"})
            j = json.loads(urllib.request.urlopen(req, timeout=15).read().decode("utf-8", "replace"))
            kl = (j.get("data") or {}).get("klines") or []
            return float(kl[-1].split(",")[1]) if kl else None
        except Exception as e:
            last = e; time.sleep(0.6 * (k + 1))
    return None


def check(code, buy=None, stop=None):
    q = sina(code)
    print(f"===== {code} =====")
    if not q:
        print("  ⚠️ 无实时行情（停牌/代码错）\n"); return
    chg = (q["price"] - q["prev"]) / q["prev"] * 100
    print(f"  {q['name']} 现价 {q['price']} ({chg:+.2f}%)  开 {q['open']} 高 {q['high']} 低 {q['low']}")
    fm = flow_min(code)
    print(f"  今日分时主力净额: {'%.0f万' % (fm/1e4) if fm is not None else '无数据'} "
          f"→ {'流入' if (fm or 0) > 0 else '流出' if fm is not None else '—'}")
    if buy:
        buy = float(buy)
        hi = q["high"]
        hit = hi >= buy * TARGET
        pnl = (q["price"] - buy) / buy * 100
        print(f"  成本 {buy} | 当前浮动 {pnl:+.2f}% | 今日最高 {hi}（{'✅达标≥+3%' if hit else '未达标'}）")
    if stop:
        stop = float(stop)
        broke = q["low"] <= stop
        print(f"  止损 {stop} | 今日最低 {q['low']}（{'❌已触及止损' if broke else '未破'}）")
    # 裁决
    if stop and q["low"] <= float(stop):
        v = "❌ 已破止损 → 走"
    elif buy and q["high"] >= float(buy) * TARGET:
        v = "✅ 已达标(+3%) → 可走/减半（次日获利即走纪律）"
    elif fm is not None and fm < 0 and buy and q["price"] < float(buy):
        v = "⚠️ 主力流出+浮亏 → 偏弱，反弹减"
    elif chg > 3:
        v = "🟢 强势 → 持有观察，冲高滞涨再走"
    else:
        v = "⚪ 观察，守防线"
    print("  ➡️", v, "\n")


def from_file(path):
    txt = open(path, encoding="utf-8").read()
    pairs = re.findall(r"\|\s*(6\d{5}|0\d{5}|3\d{5})\s*\|[^\n|]*\|[^\n|]*\|", txt)
    return list(dict.fromkeys(pairs))


def main():
    args = [a for a in sys.argv[1:] if a]
    items = []
    if args and args[0] == "--file":
        for c in from_file(args[1]):
            items.append((c, None, None))
    else:
        for a in args:
            p = a.replace("：", ":").split(":")
            items.append((p[0], p[1] if len(p) > 1 and p[1] else None, p[2] if len(p) > 2 and p[2] else None))
    if not items:
        print(__doc__); return
    for i, (c, b, s) in enumerate(items):
        if i:
            time.sleep(1.0)
        try:
            check(c, b, s)
        except Exception as e:
            print(f"⚠️ {c}: {e}\n")


if __name__ == "__main__":
    main()
