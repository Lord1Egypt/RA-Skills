#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
overview.py / ct-safety 第一段：概览

[DEPRECATED since v0.1.18]
  The "write a standalone .md/.json overview file" responsibility of this script
  has been merged into `fetch_reports.py` DEFAULT behavior (the `present` mode):
  retrieval now prints the count-facet summary directly to the context (terminal/
  dialog) AND stashes a JSON cache (`faers_summary_cache.json`) for a later
  `--out-xlsx` to reuse without re-hitting the network. This script is retained
  for backward reference only and is NO LONGER invoked by the ct-safety workflow.
  Use `fetch_reports.py --drug X` for the default retrieval summary.

Workflow (overview-first, confirm-before-detail):
  Step 1 (this script) — only fetch the drug's TOTAL report count + Top-N adverse
  events, present a brief summary, and STOP. No disproportionality, no detailed
  retrieval, no China-PV. The agent MUST show this to the user and obtain explicit
  confirmation before running any Step-2 detailed analysis.
  Step 2 (ct_safety.py with --event / detail dimensions) — only after the user
  confirms which detailed dimension(s) they want.

Reads only public FAERS data; zero confidential data or information input.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_faers


def render(drug, res, top=None):
    drug_total = res.get("drug_total")
    grand_total = res.get("grand_total")
    top_ev = res.get("top_events", []) or []
    date_from = res.get("date_from")
    date_to = res.get("date_to")
    win = ""
    if date_from or date_to:
        win = "（时间窗 %s ~ %s）" % (date_from or "…", date_to or "…")

    lines = []
    lines.append("# FAERS 安全性概览 / FAERS Safety Overview\n")
    lines.append("- 药物 Drug: **%s**" % drug)
    lines.append("- 数据源 Source: FDA FAERS (openFDA public API)")
    if win:
        lines.append("- 时间窗 Date window: **%s**" % win)
    lines.append("- 该药报告总数 Drug total reports: **%s**%s" % (
        (drug_total if drug_total is not None else "?"), win))
    if grand_total is not None:
        share = (100.0 * drug_total / grand_total) if drug_total else None
        lines.append("- 占同期 FAERS 总报告比例 Share of all FAERS: **%.3f%%** "
                     "（分母 N = %s）" % (share, grand_total))
    lines.append("")
    lines.append("## 高频不良事件 Top adverse events (MedDRA PT, 前 %d)\n" % (top or len(top_ev)))
    if top_ev:
        lines.append("| 排名 | 不良事件 Reaction (MedDRA PT) | 报告数 Count |")
        lines.append("|---|---|---|")
        for i, e in enumerate(top_ev, 1):
            lines.append("| %d | %s | %s |" % (i, e.get("term"), e.get("count")))
    else:
        lines.append("_（无数据）_")
    lines.append("")
    lines.append("> ⚠️ 以上仅为高频事件排行，未做信号检测，也非因果结论。")
    lines.append("> 如需进一步分析，请确认要检索的维度（详见下方选项），确认后本技能才会执行详细检索。")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="ct-safety Step 1: overview only (total + top events).")
    ap.add_argument("--drug", required=True)
    ap.add_argument("--field", default="patient.drug.medicinalproduct")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--date-from", help="filter receivedate >= YYYYMMDD")
    ap.add_argument("--date-to", help="filter receivedate <= YYYYMMDD")
    ap.add_argument("--api-key")
    ap.add_argument("--run", action="store_true", help="execute network request")
    ap.add_argument("--out-dir", default="./out")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    out_json = os.path.join(args.out_dir, "faers_overview.json")
    out_md = os.path.join(args.out_dir, "faers_overview.md")

    res = fetch_faers.fetch_counts(args.drug, None, args.field, args.top,
                                   args.api_key, args.run, out_json,
                                   args.date_from, args.date_to)
    if res is None:
        # preview mode: fetch_counts already printed the preview notice
        return
    md = render(args.drug, res, top=args.top)
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(md)
    print("[OK] overview ->", out_md)
    print("[NEXT] 将概览呈现给用户，等待其确认详细检索维度后再执行 Step 2。")


if __name__ == "__main__":
    main()
