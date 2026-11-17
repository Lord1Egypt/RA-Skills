#!/usr/bin/env python3
"""
实时资金流（盘中，非 T-1）

解决「龙虎榜/资金流 T-1 滞后」：
- 大盘/全市场 + 板块 + 个股榜 实时主力资金 → 牛股王公开接口（免 key，分钟级）
- 个股实时「大单/超大单」净额 → 东财逐笔成交（近 1000 笔滚动 ≈ 30–60 分钟）

用法:
  python3 realtime_flow.py                 # 全市场实时（牛股王）
  python3 realtime_flow.py --codes 002487 300285   # 个股实时大单（东财逐笔）
资金分类（money-flow 技能口径）：超大单≥100万、大单20–100万、中单4–20万、小单<4万。
"""
import argparse
import json
import sys
import urllib.request

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from radar_common import http_json  # noqa: E402

NGW = ("https://stq.niuguwang.com/taoquant/CapitalFlows/Index"
       "?s=_test&version=6.9.5&packtype=1&night=0")
EM_DETAIL = ("https://push2.eastmoney.com/api/qt/stock/details/get"
             "?secid={secid}&fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55&pos=-1000"
             "&ut=b2884a393a59ad64002292a3e90d46a5")
EM_HOSTS = ["push2.eastmoney.com", "1.push2.eastmoney.com", "7.push2.eastmoney.com", "82.push2.eastmoney.com"]


def _yi(v):
    try:
        return float(v) / 1e8
    except Exception:
        return 0.0


def market():
    d = http_json(NGW)
    data = d.get("data", {}) if isinstance(d, dict) else {}
    tl = data.get("todaylines", {}) or {}
    ds = data.get("dailystatistics", {}) or {}
    lines = tl.get("lines") or []
    print("==== 全市场实时资金流（牛股王）====")
    print("当日主力净流入：{} ｜ 上证 {}（昨收 {}）".format(
        tl.get("netinflow"), tl.get("shprice"), tl.get("precloseprice")))
    if ds:
        print("分类：主力 {} ｜ 超大单 {} ｜ 大单 {} ｜ 中单 {} ｜ 小单 {}".format(
            ds.get("mainnetinflow"), ds.get("superlarge"), ds.get("large"),
            ds.get("middle"), ds.get("small")))
    if lines:
        # lines 为累计序列（元）
        def delta(n):
            if len(lines) <= n:
                n = len(lines) - 1
            return (_yi(lines[-1].get("netinflow", 0)) - _yi(lines[-1 - n].get("netinflow", 0))) if n > 0 else 0.0
        print("最近流向：近5分钟 {:+.2f}亿 ｜ 近30分钟 {:+.2f}亿 ｜ 首笔至尾 {:+.1f}亿".format(
            delta(5), delta(30), _yi(lines[-1].get("netinflow", 0))))
        print("（数据时间 {}）".format(lines[-1].get("time")))
    st = data.get("stocks") or []
    if st:
        print("\n个股主力净流入榜 Top{}：".format(len(st)))
        for x in st:
            print("  {} {} 净{}({}) 现价{} 区间{}".format(
                x.get("stockcode"), x.get("stockname"), x.get("netinflow"),
                x.get("netinrate"), x.get("nowv"), x.get("periodupdownrate")))
    pl = data.get("plates") or []
    if pl:
        print("\n板块主力净流入榜 Top{}：".format(len(pl)))
        for x in pl:
            tp = {1: "行业", 3: "地域", 4: "概念"}.get(x.get("platetype"), "")
            print("  {}[{}] 净{}({}) 区间{}".format(x.get("platename"), tp, x.get("netinflow"),
                                                x.get("netinrate"), x.get("periodupdownrate")))
    return 0


def _secid(code):
    return ("1." if code[0] in "6" else "0.") + code


def ticks(code):
    for h in EM_HOSTS:
        try:
            d = http_json(EM_DETAIL.format(secid=_secid(code)).replace("push2.eastmoney.com", h),
                          referer="https://quote.eastmoney.com/")
            det = d.get("data", {}).get("details")
            if det:
                return det
        except Exception:
            continue
    return []


def stock(code):
    det = ticks(code)
    if not det:
        print("{} 逐笔取数失败（东财限流）".format(code)); return
    rows = []
    for s in det:
        p = s.split(",")
        if len(p) < 5:
            continue
        try:
            t, price, vol, _x, d = p[0], float(p[1]), float(p[2]), p[3], p[4]
        except Exception:
            continue
        amt = price * vol * 100  # 元
        rows.append((t, amt, d))
    if not rows:
        print("{} 无逐笔".format(code)); return

    def cat(a):
        if a >= 1e6:
            return "超大单"
        if a >= 2e5:
            return "大单"
        if a >= 4e4:
            return "中单"
        return "小单"

    net = {"超大单": 0.0, "大单": 0.0, "中单": 0.0, "小单": 0.0}
    buy = sell = 0.0
    for t, amt, d in rows:
        c = cat(amt)
        if d == "1":
            net[c] += amt; buy += amt
        elif d == "2":
            net[c] -= amt; sell += amt
    main = net["超大单"] + net["大单"]
    print("==== 个股实时大单 {}（近{}笔 {}→{}）====".format(
        code, len(rows), rows[0][0], rows[-1][0]))
    print("主力净额（超大+大）：{:+.2f} 万元".format(main / 1e4))
    for c in ["超大单", "大单", "中单", "小单"]:
        print("  {} 净{:+.2f} 万元".format(c, net[c] / 1e4))
    print("主动买 {:.1f}万 ｜ 主动卖 {:.1f}万 ｜ 买卖比 {:.2f}".format(
        buy / 1e4, sell / 1e4, (buy / sell) if sell else 0))


def main():
    ap = argparse.ArgumentParser(description="实时资金流")
    ap.add_argument("--codes", nargs="*", default=[], help="个股代码；省略则看全市场")
    a = ap.parse_args()
    if not a.codes:
        return market()
    for c in a.codes:
        stock(c); print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
