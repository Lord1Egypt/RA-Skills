#!/usr/bin/env python3
"""propose_dws.py — 建模段：宽表设计草案生成（ai-data-delivery v0.0.4）

按"问答主题域"把源表盘点聚成宽表草案。AI 提案、人审拍板——
草案里的粒度/主题域必须人工确认后才准进入 gen_metadata。

用法：
  python propose_dws.py --inventory inventory/ --metrics-raw inventory/metrics_raw.yaml \
      --out proposals/dws_draft.yaml [--max-tables 15]

聚类依据（优先级）：同构表族（必须先合并）→ 命名前缀 → 指标来源表共现。
输出草案含：建议宽表名、主题域、来源表、指标覆盖、粒度占位（必填待声明）。
"""
import argparse
import os
import re
import sys
from collections import defaultdict

import yaml
from _contract import load

MEASURE_HINT = re.compile(r"_cnt$|_count$|_days$|_rate$|_sec$|_hours?$|_minutes$|"
                          r"_amount$|_total$|_num$|_sum$|里程|金额|学时", re.I)


def main():
    ap = argparse.ArgumentParser(description="宽表设计草案生成")
    ap.add_argument("--inventory", required=True, help="盘点目录（tables/columns/isomorphic.yaml）")
    ap.add_argument("--metrics-raw", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-tables", type=int, default=15)
    args = ap.parse_args()

    tables = load(os.path.join(args.inventory, "tables.yaml"))
    metrics = load(args.metrics_raw)
    iso_path = os.path.join(args.inventory, "isomorphic.yaml")
    iso = load(iso_path) if os.path.exists(iso_path) else {}

    metric_by_table = defaultdict(list)
    for m in metrics.get("metrics", []):
        if m.get("source_table"):
            metric_by_table[m["source_table"]].append(m["id"])

    drafts, claimed = [], set()

    # 1. 同构族 → 一族一宽表
    for fam in (iso or {}).get("families", []):
        members = fam["members"]
        covered = [mid for t in members for mid in metric_by_table.get(t, [])]
        drafts.append({"proposed_table": f"dws_{fam.get('stem', 'merged').replace('#', 'x')}",
                       "theme": "同构合并（待命名主题域）",
                       "grain": "【必填，待声明】一行代表什么",
                       "sources": members, "merge": True,
                       "covered_metrics": sorted(set(covered)),
                       "note": f"{fam['count']} 张同构表合并，新增编码维度列"})
        claimed.update(members)

    # 2. 前缀聚类 → 其余表按前缀成组
    by_prefix = defaultdict(list)
    for t in tables["tables"]:
        if t["name"] not in claimed:
            by_prefix[t.get("prefix", "(无前缀)")].append(t["name"])
    for prefix, members in sorted(by_prefix.items(), key=lambda kv: -len(kv[1])):
        covered = [mid for t in members for mid in metric_by_table.get(t, [])]
        drafts.append({"proposed_table": f"dws_{prefix.rstrip('_')}",
                       "theme": f"{prefix} 域（待确认主题域归属）",
                       "grain": "【必填，待声明】一行代表什么",
                       "sources": sorted(members), "merge": False,
                       "covered_metrics": sorted(set(covered)),
                       "note": "dm_ 集市层优先复用，不重复建设" if prefix == "dm_" else ""})

    over = "" if len(drafts) <= args.max_tables else f" ⚠ 超上限，需再聚合"
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        yaml.safe_dump({"draft_count": len(drafts), "max_tables": args.max_tables,
                        "discipline": "宽表按问答主题域建，先粒度后字段；人审后才准进入 gen_metadata",
                        "drafts": drafts}, f, allow_unicode=True, sort_keys=False)
    print(f"宽表草案 {len(drafts)} 张（上限 {args.max_tables}）{over} → {args.out}")
    for d in drafts:
        print(f"  {d['proposed_table']:36s} 源表 {len(d['sources']):3d} 覆盖指标 {len(d['covered_metrics'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
