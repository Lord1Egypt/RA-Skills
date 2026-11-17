#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""usage_tracker.py - 技能成本/计量追踪（半自动）

为什么是"半自动"：纯静态技能库拿不到 runtime 真实调用，因此本工具
约定一个 usage JSONL 日志格式，由调用方（Agent/CI/手动）在每次技能
运行后追加一条记录；本工具负责聚合与导出，把数据喂给 ROI 筛选。

日志格式（每行一条 JSON）：
  {"ts":"2026-08-26T16:00:00", "skill":"invoice-bot",
   "calls":1, "tokens_in":1200, "tokens_out":300,
   "cost_usd":0.0021, "duration_s":4.5}

子命令：
  log     追加一条记录到日志（--log 指定文件，默认 ./usage.jsonl）
  report  汇总：按技能统计调用次数/token/成本/时长，并给 ROI 输入建议
  export  导出为脚本可读的 CSV/JSON，便于接 roi_filter 或门户

接 ROI（见 references/roi.md）：
  report 会按"已有记录覆盖的天数"外推月调用量，换算成 roi_filter 所需的
  --freq（次/周）与节省成本，直接给出建议命令。

纯标准库，无外部依赖。
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime, timedelta

DEFAULT_LOG = "usage.jsonl"


def _now_iso():
    return datetime.now().replace(microsecond=0).isoformat()


def cmd_log(args):
    rec = {
        "ts": args.ts or _now_iso(),
        "skill": args.skill,
        "calls": max(0, int(args.calls)),
        "tokens_in": max(0, int(args.tin)),
        "tokens_out": max(0, int(args.tout)),
        "cost_usd": max(0.0, float(args.cost)),
        "duration_s": max(0.0, float(args.dur)),
    }
    path = args.log
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"已记录: {rec['skill']} -> {path}")
    return 0


def _load(path):
    rows = []
    if not os.path.isfile(path):
        return rows
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def cmd_report(args):
    rows = _load(args.log)
    if not rows:
        print(f"日志为空或无数据: {args.log}")
        return 0

    # 聚合
    agg = {}
    for r in rows:
        s = r.get("skill", "?")
        a = agg.setdefault(s, {"calls": 0, "tin": 0, "tout": 0, "cost": 0.0,
                               "dur": 0.0, "first": None, "last": None})
        a["calls"] += int(r.get("calls", 0))
        a["tin"] += int(r.get("tokens_in", 0))
        a["tout"] += int(r.get("tokens_out", 0))
        a["cost"] += float(r.get("cost_usd", 0.0))
        a["dur"] += float(r.get("duration_s", 0.0))
        ts = r.get("ts")
        if ts:
            if a["first"] is None or ts < a["first"]:
                a["first"] = ts
            if a["last"] is None or ts > a["last"]:
                a["last"] = ts

    # 覆盖天数（用于外推月调用）
    span_days = 1
    try:
        fa = datetime.fromisoformat(agg and min(
            a["first"] for a in agg.values() if a["first"]))
        la = datetime.fromisoformat(agg and max(
            a["last"] for a in agg.values() if a["last"]))
        span_days = max(1, (la - fa).days + 1)
    except Exception:
        span_days = 1

    factor = 30.0 / span_days  # 外推到月

    print("=" * 64)
    print("技能成本/计量汇总")
    print("=" * 64)
    print(f"{'技能':20s} {'调用':>6s} {'tok_in':>9s} {'tok_out':>9s} "
          f"{'成本$':>9s} {'月调*':>7s}")
    print("-" * 64)
    roi_lines = []
    for s, a in sorted(agg.items(), key=lambda kv: -kv[1]["cost"]):
        monthly_calls = a["calls"] * factor
        print(f"{s:20s} {a['calls']:6d} {a['tin']:9d} {a['tout']:9d} "
              f"{a['cost']:9.4f} {monthly_calls:7.0f}")
        # ROI 输入建议：周频次 = 月调用/4.33
        freq_week = monthly_calls / 4.33
        roi_lines.append((s, freq_week, a["cost"] * factor))

    print("-" * 64)
    print(f"* 月调用 = 记录覆盖 {span_days} 天外推至 30 天")
    print("")
    print("ROI 输入建议（接 roi_filter.py，--consistent 由你判断）：")
    for s, fw, mc in roi_lines:
        print(f"  studio roi --freq {fw:.1f} --minutes <单次分钟> "
              f"--cost {mc*52:.1f}   # {s}")
    return 0


def cmd_export(args):
    rows = _load(args.log)
    if args.format == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        w = csv.writer(sys.stdout)
        w.writerow(["ts", "skill", "calls", "tokens_in", "tokens_out",
                    "cost_usd", "duration_s"])
        for r in rows:
            w.writerow([r.get("ts", ""), r.get("skill", ""),
                        r.get("calls", 0), r.get("tokens_in", 0),
                        r.get("tokens_out", 0), r.get("cost_usd", 0.0),
                        r.get("duration_s", 0.0)])
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="usage_tracker",
        description="技能成本/计量追踪（半自动 usage 日志）")
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("log", help="追加一条 usage 记录")
    pl.add_argument("--log", default=DEFAULT_LOG)
    pl.add_argument("--skill", required=True)
    pl.add_argument("--calls", default=1)
    pl.add_argument("--tin", default=0, help="输入 token 数")
    pl.add_argument("--tout", default=0, help="输出 token 数")
    pl.add_argument("--cost", default=0.0, help="本次成本 USD")
    pl.add_argument("--dur", default=0.0, help="耗时秒")
    pl.add_argument("--ts", default=None, help="ISO 时间，默认现在")
    pl.set_defaults(func=cmd_log)

    pr = sub.add_parser("report", help="汇总并给 ROI 建议")
    pr.add_argument("--log", default=DEFAULT_LOG)
    pr.set_defaults(func=cmd_report)

    pe = sub.add_parser("export", help="导出 json/csv")
    pe.add_argument("--log", default=DEFAULT_LOG)
    pe.add_argument("--format", choices=["csv", "json"], default="csv")
    pe.set_defaults(func=cmd_export)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
