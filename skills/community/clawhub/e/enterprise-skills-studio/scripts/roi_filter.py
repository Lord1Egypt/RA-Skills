#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业技能 ROI 筛选器（ROI Gate）

判断一个候选流程"值不值得做成技能"。四要件须同时满足：
  1. 频次 weekly_freq >= 10 次/周
  2. 时长 avg_minutes > 30 分钟/次
  3. 年化成本 annual_cost > 5000（本币，默认英镑 £）
  4. 一致性 consistent == True（步骤基本一致）

任一不满足 → HOLD，并列出未达标项与建议。

纯标准库，无外部依赖；支持 --answers JSON / 直接参数 / --json / --md。

用法：
  python roi_filter.py --freq 15 --minutes 45 --cost 8000 --consistent
  python roi_filter.py --answers roi.json
  python roi_filter.py --freq 3 --minutes 50 --cost 9000 --consistent --json
"""
import argparse
import json
import sys

THRESH = {
    "weekly_freq": 10,      # 次/周
    "avg_minutes": 30,      # 分钟/次
    "annual_cost": 5000,    # 年成本（本币）
}

ITEMS = [
    ("weekly_freq", "频次(次/周)", "每周 ≥ 10 次"),
    ("avg_minutes", "单次时长(分钟)", "单次 > 30 分钟"),
    ("annual_cost", "年化成本", "年 > 5000"),
    ("consistent", "步骤一致性", "步骤基本一致"),
]


def evaluate(d):
    reasons = []
    passed = True
    detail = {}
    # 数值门槛
    freq = d.get("weekly_freq", 0)
    mins = d.get("avg_minutes", 0)
    cost = d.get("annual_cost", 0)
    cons = bool(d.get("consistent", False))

    ok_freq = freq >= THRESH["weekly_freq"]
    ok_mins = mins > THRESH["avg_minutes"]
    ok_cost = cost > THRESH["annual_cost"]
    ok_cons = cons is True

    detail["weekly_freq"] = {"value": freq, "need": ">= %d" % THRESH["weekly_freq"], "pass": ok_freq}
    detail["avg_minutes"] = {"value": mins, "need": "> %d" % THRESH["avg_minutes"], "pass": ok_mins}
    detail["annual_cost"] = {"value": cost, "need": "> %d" % THRESH["annual_cost"], "pass": ok_cost}
    detail["consistent"] = {"value": cons, "need": "True", "pass": ok_cons}

    if not ok_freq:
        passed = False
        reasons.append(f"频次 {freq} < {THRESH['weekly_freq']}/周")
    if not ok_mins:
        passed = False
        reasons.append(f"单次 {mins} 分钟 ≤ {THRESH['avg_minutes']}")
    if not ok_cost:
        passed = False
        reasons.append(f"年成本 {cost} ≤ {THRESH['annual_cost']}")
    if not ok_cons:
        passed = False
        reasons.append("步骤不一致，需先标准化")

    return ("BUILD" if passed else "HOLD"), reasons, detail


def render_text(verdict, reasons, detail):
    L = []
    L.append("企业技能 ROI 筛选")
    L.append("=" * 50)
    L.append(f"判定: {verdict}")
    L.append("-" * 50)
    for key, label, need in ITEMS:
        dd = detail[key]
        mark = "✅" if dd["pass"] else "❌"
        L.append(f"  {mark} {label}: {dd['value']}（需 {need}）")
    L.append("-" * 50)
    if verdict == "BUILD":
        L.append("建议：值得做成技能，进入 Plan 阶段（lifecycle-ops.md）。")
    else:
        L.append("建议：HOLD，暂不建正式技能。" + (" 原因：" + "；".join(reasons) if reasons else ""))
    return "\n".join(L)


def render_md(verdict, reasons, detail):
    out = ["# 企业技能 ROI 筛选", ""]
    out.append(f"**判定**: {verdict}")
    out.append("")
    out.append("| 要件 | 实测 | 门槛 | 结果 |")
    out.append("|------|------|------|------|")
    for key, label, need in ITEMS:
        dd = detail[key]
        out.append(f"| {label} | {dd['value']} | {need} | {'PASS' if dd['pass'] else 'FAIL'} |")
    out.append("")
    if verdict == "BUILD":
        out.append("建议：值得做成技能，进入 Plan 阶段。")
    else:
        out.append("建议：HOLD。" + (" 原因：" + "；".join(reasons) if reasons else ""))
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="企业技能 ROI 筛选器")
    ap.add_argument("--freq", type=float, help="每周频次")
    ap.add_argument("--minutes", type=float, help="单次时长(分钟)")
    ap.add_argument("--cost", type=float, help="年化成本")
    ap.add_argument("--consistent", action="store_true", help="步骤一致")
    ap.add_argument("--answers", help="JSON 文件：{weekly_freq,avg_minutes,annual_cost,consistent}")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--md", action="store_true")
    args = ap.parse_args()

    if args.answers:
        try:
            with open(args.answers, "r", encoding="utf-8") as f:
                d = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"错误: {e}", file=sys.stderr)
            return 2
    else:
        d = {
            "weekly_freq": args.freq if args.freq is not None else 0,
            "avg_minutes": args.minutes if args.minutes is not None else 0,
            "annual_cost": args.cost if args.cost is not None else 0,
            "consistent": args.consistent,
        }

    verdict, reasons, detail = evaluate(d)
    if args.json:
        print(json.dumps({"verdict": verdict, "reasons": reasons, "detail": detail},
                         ensure_ascii=False, indent=2))
    elif args.md:
        print(render_md(verdict, reasons, detail))
    else:
        print(render_text(verdict, reasons, detail))
    return 0


if __name__ == "__main__":
    sys.exit(main())
