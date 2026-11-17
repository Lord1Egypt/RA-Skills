#!/usr/bin/env python3
"""
交易日志（复盘闭环第一步）

录入每笔交易 → 平仓时补 exit → 供 review.py 统计「各形态胜率」。

存库：trading/journal/trades.json

用法:
  add   --code 002487 --name 大金重工 --pattern N字爆发 --entry 39.2 --stop 37.4 --target 42.0 [--size 0.15] [--date 2026-09-24] [--note "..."]
  close --code 002487 --exit 41.5 [--date 2026-09-25] [--reason "冲高走弱"]
  list  [--open] [--code 002487]
  stats
"""
import argparse
import datetime as dt
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from radar_common import PATTERNS, load_journal, save_journal  # noqa: E402


def _today():
    return dt.date.today().isoformat()


def _find(rows, key, only_open=False):
    hits = [r for r in rows if r["code"] == key or str(r["id"]) == str(key)]
    if only_open:
        hits = [r for r in hits if r.get("exit") is None]
    return hits


def cmd_add(a):
    rows = load_journal()
    if a.pattern not in PATTERNS:
        print("⚠️ 形态 '{}' 不在标准集 {}，仍记录。".format(a.pattern, PATTERNS))
    tid = max([r["id"] for r in rows], default=0) + 1
    rec = {
        "id": tid,
        "date_in": a.date or _today(),
        "code": a.code,
        "name": a.name or "",
        "pattern": a.pattern,
        "entry": float(a.entry),
        "stop": float(a.stop),
        "target": float(a.target) if a.target else None,
        "size": float(a.size) if a.size else None,
        "date_out": None,
        "exit": None,
        "reason": None,
        "pnl_pct": None,
        "win": None,
        "note": a.note or "",
    }
    rows.append(rec)
    save_journal(rows)
    print("✅ 已记录 #{id} {name}({code}) {pattern} 入场{entry} 止损{stop} 目标{target}".format(**rec))


def cmd_close(a):
    rows = load_journal()
    hits = _find(rows, a.code, only_open=True)
    if not hits:
        print("❌ 没找到未平仓的 {}（用 list --open 看）".format(a.code))
        return 1
    r = hits[-1]
    r["date_out"] = a.date or _today()
    r["exit"] = float(a.exit)
    r["reason"] = a.reason or ""
    r["pnl_pct"] = round((r["exit"] - r["entry"]) / r["entry"] * 100, 2)
    r["win"] = r["pnl_pct"] > 0
    save_journal(rows)
    print("✅ 平仓 #{id} {name}({code}) 出{exit:.2f} → {p:+.2f}% ({w})".format(
        id=r["id"], name=r.get("name", ""), code=r["code"], exit=r["exit"],
        p=r["pnl_pct"], w="盈" if r["win"] else "亏"))
    return 0


def cmd_list(a):
    rows = load_journal()
    if a.code:
        rows = [r for r in rows if r["code"] == a.code]
    if a.open:
        rows = [r for r in rows if r.get("exit") is None]
    if not rows:
        print("(空)")
        return 0
    print("{:>3} {:<10} {:<7} {:<6} {:<10} {:>7} {:>7} {:>7} {:>7}".format(
        "id", "date_in", "code", "pat", "name", "entry", "stop", "exit", "pnl%"))
    for r in rows:
        print("{id:>3} {date_in:<10} {code:<7} {pat:<6} {name:<10} {entry:>7.2f} {stop:>7.2f} "
              "{exit:>7} {pnl:>7}".format(
                  id=r["id"], date_in=r["date_in"], code=r["code"],
                  pat=r.get("pattern", "")[:5], name=(r.get("name") or "")[:9],
                  entry=r["entry"], stop=r["stop"],
                  exit=("{:.2f}".format(r["exit"]) if r.get("exit") is not None else "-"),
                  pnl=("{:+.2f}".format(r["pnl_pct"]) if r.get("pnl_pct") is not None else "-")))
    return 0


def cmd_stats(a):
    rows = load_journal()
    closed = [r for r in rows if r.get("exit") is not None]
    openp = [r for r in rows if r.get("exit") is None]
    print("总记录 {} ｜ 已平仓 {} ｜ 持仓中 {}".format(len(rows), len(closed), len(openp)))
    if closed:
        wins = [r for r in closed if r["win"]]
        print("总体胜率 {}/{} = {:.1f}%".format(len(wins), len(closed), len(wins) / len(closed) * 100))
    return 0


def main():
    p = argparse.ArgumentParser(description="交易日志")
    sub = p.add_subparsers(dest="cmd", required=True)
    pa = sub.add_parser("add")
    pa.add_argument("--code", required=True)
    pa.add_argument("--name", default="")
    pa.add_argument("--pattern", required=True, help="|".join(PATTERNS))
    pa.add_argument("--entry", required=True)
    pa.add_argument("--stop", required=True)
    pa.add_argument("--target", default="")
    pa.add_argument("--size", default="")
    pa.add_argument("--date", default="")
    pa.add_argument("--note", default="")
    pa.set_defaults(func=cmd_add)
    pc = sub.add_parser("close")
    pc.add_argument("--code", required=True)
    pc.add_argument("--exit", required=True)
    pc.add_argument("--date", default="")
    pc.add_argument("--reason", default="")
    pc.set_defaults(func=cmd_close)
    pl = sub.add_parser("list")
    pl.add_argument("--open", action="store_true")
    pl.add_argument("--code", default="")
    pl.set_defaults(func=cmd_list)
    ps = sub.add_parser("stats")
    ps.set_defaults(func=cmd_stats)
    args = p.parse_args()
    sys.exit(args.func(args) or 0)


if __name__ == "__main__":
    main()
