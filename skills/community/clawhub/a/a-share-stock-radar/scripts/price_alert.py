#!/usr/bin/env python3
"""
持仓到价/止损监控（盘中兜底：人忙也能收到提醒）

持仓存 trading/alerts/positions.json
用法:
  add    --code 002487 --name 大金重工 --entry 39.2 --stop 37.4 --target 42.0 [--size 0.15]
  remove --code 002487
  list
  check                       # 拉实时价，命中止损/目标就打印 TRIGGER，退出码 2
  check --quiet               # 无触发时完全静默（给 cron 用）
数据源：新浪实时 → 腾讯兜底。
"""
import argparse
import datetime as dt
import json
import os
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from radar_common import http_get, sina_symbol, tencent_quote_symbol, ws_root  # noqa: E402

PF = os.path.join(ws_root(), "trading", "alerts", "positions.json")


def load():
    if os.path.exists(PF):
        with open(PF, encoding="utf-8") as f:
            return json.load(f)
    return []


def save(rows):
    os.makedirs(os.path.dirname(PF), exist_ok=True)
    with open(PF, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


def quotes(codes):
    ids = ",".join(sina_symbol(c) for c in codes)
    out = {}
    try:
        txt = http_get("https://hq.sinajs.cn/list=" + ids, referer="https://finance.sina.com.cn/",
                       encoding="gbk")
        for line in txt.strip().split("\n"):
            if '="' not in line:
                continue
            code = line.split("=")[0].split("_")[-1][2:]
            p = line.split('"')[1].split(",")
            if len(p) >= 4:
                out[code] = {"name": p[0], "price": float(p[3]), "prev": float(p[2]),
                             "high": float(p[33]) if len(p) > 33 and p[33] else float(p[3])}
    except Exception:
        pass
    missing = [c for c in codes if c not in out]
    if missing:
        try:
            ids2 = ",".join(tencent_quote_symbol(c) for c in missing)
            txt = http_get("https://qt.gtimg.cn/q=" + ids2, referer="https://gu.qq.com/", encoding="gbk")
            for line in txt.strip().split(";"):
                if '"' not in line:
                    continue
                p = line.split('"')[1].split("~")
                if len(p) > 5:
                    out[p[2]] = {"name": p[1], "price": float(p[3]), "prev": float(p[4]),
                                 "high": float(p[33]) if len(p) > 33 and p[33] else float(p[3])}
        except Exception:
            pass
    return out


def cmd_add(a):
    rows = load()
    rows = [r for r in rows if r["code"] != a.code]
    rows.append({"code": a.code, "name": a.name, "entry": float(a.entry), "stop": float(a.stop),
                 "target": float(a.target) if a.target else None,
                 "size": float(a.size) if a.size else None, "date": a.date or dt.date.today().isoformat()})
    save(rows)
    print("✅ 已挂监控 {} {}（止损{} 目标{}）".format(a.code, a.name, a.stop, a.target or "-"))
    return 0


def cmd_remove(a):
    rows = [r for r in load() if r["code"] != a.code]
    save(rows)
    print("✅ 已移除 {}".format(a.code))
    return 0


def cmd_list(a):
    rows = load()
    if not rows:
        print("(无持仓监控)"); return 0
    for r in rows:
        print("{} {} 入场{} 止损{} 目标{}".format(
            r["code"], r["name"], r["entry"], r["stop"], r.get("target") or "-"))
    return 0


def cmd_check(a):
    rows = load()
    if not rows:
        if not a.quiet:
            print("(无持仓监控)")
        return 0
    q = quotes([r["code"] for r in rows])
    triggers = []
    lines = []
    for r in rows:
        it = q.get(r["code"])
        if not it:
            lines.append("{} {} 取价失败".format(r["code"], r["name"])); continue
        price = it["price"]
        hi = it.get("high") or price
        fade = (hi / price - 1) * 100 if price else 0.0   # 现价距今日最高回落幅度
        pnl = (price / r["entry"] - 1) * 100 if r["entry"] else 0
        status = "持有"
        if price <= r["stop"]:
            status = "🛑 破止损 → 走"; triggers.append((r, price, "STOP"))
        elif r.get("target") and price >= r["target"]:
            status = "🎯 达目标 → 止盈"; triggers.append((r, price, "TARGET"))
        elif pnl > 0 and fade >= a.fade:
            status = "⚠️ 冲高走弱（距今高-{:.1f}%）→ 减仓/走".format(fade)
            triggers.append((r, price, "FADE"))
        lines.append("{} {} 现{:.2f}（{:+.2f}%） 止损{} 目标{} → {}".format(
            r["code"], r["name"], price, pnl, r["stop"], r.get("target") or "-", status))
    if triggers or not a.quiet:
        print("==== 持仓监控 {} ====".format(dt.datetime.now().strftime("%m-%d %H:%M")))
        for ln in lines:
            print(ln)
    if triggers:
        print("\n⚠️ 触发提醒：")
        for r, price, kind in triggers:
            print("  TRIGGER {} {} {} 现{:.2f}".format(kind, r["code"], r["name"], price))
        return 2
    return 0


def main():
    ap = argparse.ArgumentParser(description="持仓到价监控")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pa = sub.add_parser("add")
    pa.add_argument("--code", required=True); pa.add_argument("--name", required=True)
    pa.add_argument("--entry", required=True); pa.add_argument("--stop", required=True)
    pa.add_argument("--target", default=""); pa.add_argument("--size", default=""); pa.add_argument("--date", default="")
    pa.set_defaults(func=cmd_add)
    pr = sub.add_parser("remove"); pr.add_argument("--code", required=True); pr.set_defaults(func=cmd_remove)
    pl = sub.add_parser("list"); pl.set_defaults(func=cmd_list)
    pc = sub.add_parser("check"); pc.add_argument("--quiet", action="store_true")
    pc.add_argument("--fade", type=float, default=3.0, help="冲高回落阈值%%，默认3；现价距今日最高回落≥此值 → 提醒")
    pc.set_defaults(func=cmd_check)
    args = ap.parse_args()
    sys.exit(args.func(args) or 0)


if __name__ == "__main__":
    main()
