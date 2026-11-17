#!/usr/bin/env python3
"""
券商交割单导入（华泰/通达信 GBK 导出，中文列名）

解析成交明细 → FIFO 配对买卖 → 算真实盈亏（用「发生金额」，已含费用）→
写入 trading/journal/trades.json（形态默认「其他」，待人工归类）+ 输出统计。

用法:
  python3 .../broker_csv.py <csv路径> [--dry]
"""
import argparse
import csv
import datetime as dt
import io
import os
import re
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from radar_common import load_journal, save_journal, ws_root  # noqa: E402

BUY = ("证券买入", "买入")
SELL = ("证券卖出", "卖出")


def _clean(v):
    v = (v or "").strip()
    v = re.sub(r'^=\s*"?', "", v)
    v = v.replace('"', "").strip()
    return v


def _num(v):
    try:
        return float(_clean(v))
    except Exception:
        return 0.0


def parse(path):
    raw = open(path, "rb").read()
    for enc in ("gbk", "gb18030", "utf-8-sig"):
        try:
            txt = raw.decode(enc)
            break
        except Exception:
            continue
    rows = list(csv.reader(io.StringIO(txt)))
    hdr = [c.strip() for c in rows[0]]
    idx = {name: i for i, name in enumerate(hdr)}

    def col(r, *names):
        for n in names:
            if n in idx and idx[n] < len(r):
                return r[idx[n]]
        return ""

    out = []
    for r in rows[1:]:
        if not r or not any(x.strip() for x in r):
            continue
        kind = col(r, "交易类别", "业务名称", "摘要").strip()
        if not (any(k in kind for k in BUY) or any(k in kind for k in SELL)):
            continue
        code = _clean(col(r, "证券代码", "股票代码"))
        out.append({
            "date": _clean(col(r, "发生日期", "交收日期", "成交日期"))[:10],
            "time": _clean(col(r, "发生时间")),
            "code": code,
            "name": col(r, "证券名称", "股票名称").strip(),
            "side": "B" if any(k in kind for k in BUY) else "S",
            "price": _num(col(r, "成交均价", "成交价格", "成交价")),
            "qty": _num(col(r, "成交数量")),
            "cash": _num(col(r, "发生金额")),   # 买入为负、卖出为正，已含费用
        })
    out.sort(key=lambda x: (x["date"], x["time"]))
    return out


def fifo(trades):
    """按代码 FIFO 配对，返回已平仓记录（含 pnl 元 与 pnl%）。"""
    books = {}
    closed = []
    for t in trades:
        b = books.setdefault(t["code"], [])
        if t["side"] == "B":
            if t["qty"] > 0:
                b.append({"date": t["date"], "time": t["time"], "price": t["price"], "qty": t["qty"],
                          "qty0": t["qty"], "cash": t["cash"]})  # cash 为负
        else:
            remain = t["qty"]
            proceeds_per_share = (t["cash"] / t["qty"]) if t["qty"] else 0.0
            while remain > 1e-6 and b:
                leg = b[0]
                use = min(remain, leg["qty"])
                cost = leg["cash"] * (use / leg["qty0"]) if leg["qty0"] else 0.0  # 负
                proceeds = proceeds_per_share * use
                pnl = proceeds + cost
                cost_abs = abs(cost)
                days = 0
                try:
                    days = (dt.date.fromisoformat(t["date"]) - dt.date.fromisoformat(leg["date"])).days
                except Exception:
                    pass
                closed.append({
                    "code": t["code"], "name": t["name"],
                    "date_in": leg["date"], "buy_time": leg.get("time", ""), "date_out": t["date"],
                    "entry": round(leg["price"], 3), "exit": round(t["price"], 3),
                    "qty": round(use, 0), "days": days,
                    "pnl_yuan": round(pnl, 2),
                    "pnl_pct": round(pnl / cost_abs * 100, 2) if cost_abs else 0.0,
                })
                leg["qty"] -= use
                remain -= use
                if leg["qty"] <= 1e-6:
                    b.pop(0)
    return closed


def main():
    ap = argparse.ArgumentParser(description="券商交割单导入")
    ap.add_argument("csvpath")
    ap.add_argument("--dry", action="store_true", help="只打印不写库")
    a = ap.parse_args()

    trades = parse(a.csvpath)
    closed = fifo(trades)
    buys = [t for t in trades if t["side"] == "B"]
    sells = [t for t in trades if t["side"] == "S"]

    print("==== 交割单解析 ====")
    print("成交笔数 {}（买 {} / 卖 {}）｜ 配对平仓 {} 笔".format(len(trades), len(buys), len(sells), len(closed)))
    if closed:
        total = sum(c["pnl_yuan"] for c in closed)
        wins = [c for c in closed if c["pnl_yuan"] > 0]
        print("已实现盈亏合计：{:+.2f} 元".format(total))
        print("胜率：{}/{} = {:.1f}%".format(len(wins), len(closed), len(wins) / len(closed) * 100))
        print("{:<7} {:<8} {:>5} {:>5} {:>7} {:>7} {:>10} {:>8}".format(
            "代码", "名称", "买日", "卖日", "入场", "出场", "盈亏(元)", "盈亏%"))
        for c in sorted(closed, key=lambda x: x["date_out"]):
            print("{:<7} {:<8} {:>5} {:>5} {:>7.2f} {:>7.2f} {:>10.2f} {:>8.2f}".format(
                c["code"], c["name"][:6], c["date_in"][5:], c["date_out"][5:],
                c["entry"], c["exit"], c["pnl_yuan"], c["pnl_pct"]))
        # 买入时点分桶 / ETF vs 个股
        def bucket(hhmm):
            try:
                h, m = int(hhmm[:2]), int(hhmm[3:5])
            except Exception:
                return "未知"
            t = h * 60 + m
            if t <= 9 * 60 + 40:
                return "早盘(≤09:40)"
            if t <= 11 * 60 + 30:
                return "上午(09:40-11:30)"
            if t <= 14 * 60:
                return "午后(13:00-14:00)"
            return "尾盘(≥14:00)"

        def agg(keyfn, title):
            g = {}
            for c in closed:
                g.setdefault(keyfn(c), []).append(c)
            print("\n" + title)
            for k in sorted(g):
                rs = g[k]
                w = sum(1 for x in rs if x["pnl_yuan"] > 0)
                print("  {:<16} {}笔　胜率{:>3.0f}%　{:+.0f}元".format(
                    k, len(rs), w / len(rs) * 100, sum(x["pnl_yuan"] for x in rs)))

        agg(lambda c: "{}日".format(c["days"]), "按持股天数：")
        agg(lambda c: bucket(c.get("buy_time", "")), "按买入时点：")
        agg(lambda c: "ETF/LOF" if (c["code"].startswith("51") or c["code"].startswith("15")) else "个股",
            "按标的类型：")

        # 未匹配提示
        unmatched = {}
        openq = {}
        for c in closed:
            pass
        print("\n提示：卖出中若有早于窗口的持仓，成本不完整；未在窗口内卖出的买入为持仓中。")

    if not a.dry:
        rows = load_journal()
        base = max([r["id"] for r in rows], default=0)
        added = []
        for i, c in enumerate(closed, 1):
            added.append({
                "id": base + i, "date_in": c["date_in"], "code": c["code"], "name": c["name"],
                "pattern": "其他", "entry": c["entry"],
                "stop": None, "target": None, "size": None,
                "date_out": c["date_out"], "exit": c["exit"], "reason": "交割单导入",
                "pnl_pct": c["pnl_pct"], "win": c["pnl_yuan"] > 0,
                "note": "交割单导入 · 持{}日 · {:+.0f}元".format(c["days"], c["pnl_yuan"]),
            })
        save_journal(rows + added)
        print("\n→ 已导入 {} 笔到 trading/journal/trades.json（形态默认「其他」，可后续归类）".format(len(added)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
