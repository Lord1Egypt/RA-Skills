#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业技能生命周期追踪器（Lifecycle Ops Tracker）

读入技能注册表（JSON 数组），输出：
  - 各阶段分布
  - 待复审（评估到期）技能
  - 弃用候选（低频 + 长期未评估的 Operate 阶段技能）
  - 整体健康度提示

注册表每条（字段缺省安全）：
  {
    "name": "skill-a", "domain": "hr", "owner": "alice",
    "version": "v0.3", "stage": "Operate",
    "deps": "", "eval_status": "通过",
    "review_cycle": "季度", "usage": 12, "last_eval": "2026-02-01"
  }

阶段：Plan/Create/Evaluate/Deploy/Operate/Deprecate/Archived
复审周期→月数：月度=1, 季度=3, 半年度=6, 年度=12（未知默认 3）
弃用候选：stage==Operate 且 usage < 1 且 距 last_eval > 2*周期月

纯标准库，无外部依赖；支持 --json / --md。

用法：
  python lifecycle_track.py --registry registry.json
  python lifecycle_track.py --registry registry.json --json
"""
import argparse
import datetime as dt
import json
import sys

STAGES = ["Plan", "Create", "Evaluate", "Deploy", "Operate", "Deprecate", "Archived"]
CYCLE_MONTHS = {"月度": 1, "季度": 3, "半年度": 6, "年度": 12}


def parse_date(s):
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y-%m", "%Y"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def months_since(d):
    if not d:
        return 999
    today = dt.date.today()
    return (today.year - d.year) * 12 + (today.month - d.month)


def track(registry):
    rows = []
    stage_counts = {s: 0 for s in STAGES}
    due = []
    dep_candidates = []
    for item in registry:
        name = item.get("name", "?")
        stage = item.get("stage", "Plan")
        if stage not in stage_counts:
            stage = "Plan"
        stage_counts[stage] += 1
        cycle = CYCLE_MONTHS.get(item.get("review_cycle", "季度"), 3)
        last = parse_date(item.get("last_eval", ""))
        ms = months_since(last)
        if stage in ("Operate", "Deploy") and ms > cycle:
            due.append((name, stage, item.get("last_eval", "从未"), cycle))
        usage = item.get("usage", 0) or 0
        if stage == "Operate" and usage < 1 and ms > 2 * cycle:
            dep_candidates.append((name, usage, item.get("last_eval", "从未")))
        rows.append((name, stage, item.get("version", ""), item.get("owner", ""), usage, ms))
    return stage_counts, due, dep_candidates, rows


def render_text(stage_counts, due, dep, rows):
    L = []
    L.append("企业技能生命周期追踪")
    L.append("=" * 50)
    L.append("阶段分布:")
    for s in STAGES:
        if stage_counts[s]:
            L.append(f"  {s:10s}: {stage_counts[s]}")
    L.append("-" * 50)
    L.append(f"待复审（评估到期）: {len(due)} 项")
    for n, st, le, cy in due:
        L.append(f"  - {n} [{st}] 末次评估 {le}（周期 {cy}月）")
    L.append(f"弃用候选: {len(dep)} 项")
    for n, u, le in dep:
        L.append(f"  - {n} 周用法度 {u}，末次评估 {le}")
    L.append("=" * 50)
    return "\n".join(L)


def render_md(stage_counts, due, dep, rows):
    out = ["# 企业技能生命周期追踪", ""]
    out.append("**阶段分布**")
    out.append("")
    out.append("| 阶段 | 数量 |")
    out.append("|------|------|")
    for s in STAGES:
        if stage_counts[s]:
            out.append(f"| {s} | {stage_counts[s]} |")
    out.append("")
    out.append(f"**待复审（评估到期）**: {len(due)} 项")
    for n, st, le, cy in due:
        out.append(f"- {n} [{st}] 末次评估 {le}（周期 {cy}月）")
    out.append("")
    out.append(f"**弃用候选**: {len(dep)} 项")
    for n, u, le in dep:
        out.append(f"- {n} 周用法度 {u}，末次评估 {le}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="企业技能生命周期追踪器")
    ap.add_argument("--registry", required=True, help="注册表 JSON 文件路径")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--md", action="store_true")
    args = ap.parse_args()

    try:
        with open(args.registry, "r", encoding="utf-8") as f:
            registry = json.load(f)
        if not isinstance(registry, list):
            registry = [registry]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"错误: {e}", file=sys.stderr)
        return 2

    stage_counts, due, dep, rows = track(registry)
    if args.json:
        print(json.dumps({
            "stage_counts": stage_counts,
            "due_review": [{"name": n, "stage": st, "last_eval": le} for n, st, le, _ in due],
            "deprecation_candidates": [{"name": n, "usage": u} for n, u, _ in dep],
        }, ensure_ascii=False, indent=2))
    elif args.md:
        print(render_md(stage_counts, due, dep, rows))
    else:
        print(render_text(stage_counts, due, dep, rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
