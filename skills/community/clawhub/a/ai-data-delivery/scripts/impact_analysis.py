#!/usr/bin/env python3
"""impact_analysis.py — 运营段：变更影响面分析（ai-data-delivery v0.0.4）

RULE-CHANGE-01：改一个字段/数据集/指标前，先回答"谁会受影响"——概念展开、指标口径、
关系与多跳路径、gold 用例。先评估再动手，改完跑 release_gate.py 收口。

用法：
  python impact_analysis.py --model semantic.yaml --target ent_id [--cases cases.json]
target 可以是：字段名 / 数据集名 / 物理表名 / 指标 id 或名称 / 概念 term。
退出码：0 找到影响面；2 未找到 target。
"""
import argparse
import json
import re
import sys

import yaml
from _contract import load


def mentions(text, name):
    return bool(text) and bool(re.search(rf"\b{re.escape(name)}\b", str(text)))


def metric_text(mt):
    parts = [mt.get("expr"), mt.get("extra_where"), mt.get("time_field")]
    for k in ("numerator", "denominator"):
        if isinstance(mt.get(k), dict):
            parts.append(mt[k].get("expr"))
    return " ".join(p for p in parts if p)


def main():
    ap = argparse.ArgumentParser(description="变更影响面分析")
    ap.add_argument("--model", required=True)
    ap.add_argument("--target", required=True)
    ap.add_argument("--cases", default=None, help="gold 用例集（可选，评估回归面）")
    args = ap.parse_args()

    m = load(args.model)
    t = args.target
    ds_list = m.get("datasets", [])
    ds_by_name = {d["name"]: d for d in ds_list}
    ds_by_source = {d.get("source"): d for d in ds_list}

    # ---- 定位 target ----
    hit_datasets, hit_fields = [], {}   # hit_fields: {dataset_name: [field,...]}
    hit_metrics, hit_concepts = [], []
    if t in ds_by_name:
        hit_datasets.append(ds_by_name[t])
    elif t in ds_by_source:
        hit_datasets.append(ds_by_source[t])
    for d in ds_list:
        for f in d.get("fields", []):
            if f["name"] == t and d not in hit_datasets:
                hit_fields.setdefault(d["name"], []).append(f["name"])
    for mt in m.get("metrics", []):
        if t in (mt.get("id"), mt.get("name")):
            hit_metrics.append(mt)
    for c in m.get("concepts", []):
        if t == c.get("term") or t in (c.get("aliases") or []):
            hit_concepts.append(c)

    if not (hit_datasets or hit_fields or hit_metrics or hit_concepts):
        ds_names = [d.get("name") for d in m.get("datasets", []) or []]
        mt_ids = [x.get("id") for x in m.get("metrics", []) or []]
        terms = [c.get("term") for c in m.get("concepts", []) or []]
        print(f"未找到 target：{t}（既不是数据集/物理表/字段/指标/概念）\n"
              f"  target 直接写名字，不带前缀：如 {ds_names[0] if ds_names else 'dataset_name'}、"
              f"{mt_ids[0] if mt_ids else 'metric_id'}\n"
              f"  可用数据集：{ds_names}\n"
              f"  可用指标：{mt_ids[:10]}{'…' if len(mt_ids) > 10 else ''}\n"
              f"  可用概念：{terms}", file=sys.stderr)
        return 2

    # ---- 由命中面扩散 ----
    affected_ds = {d["name"] for d in hit_datasets} | set(hit_fields)
    # 数据集命中 → 其全部字段进入影响面
    field_names = set()
    for d in hit_datasets:
        field_names |= {f["name"] for f in d.get("fields", [])}
    field_names.add(t)

    aff_concepts = set()
    for c in m.get("concepts", []):
        ex = c.get("expand") or {}
        if ex.get("dataset") in affected_ds or ex.get("field") in field_names:
            aff_concepts.add(c.get("term"))
    for c in hit_concepts:
        aff_concepts.add(c.get("term"))

    aff_metrics = set()
    for mt in m.get("metrics", []):
        if (mt.get("dataset") in affected_ds
                or any(mentions(metric_text(mt), f) for f in field_names)):
            aff_metrics.add(f"{mt.get('id')}（{mt.get('name')}）")
    for mt in hit_metrics:
        aff_metrics.add(f"{mt.get('id')}（{mt.get('name')}）")
        if mt.get("dataset"):
            affected_ds.add(mt["dataset"])

    aff_rels, aff_paths = [], []
    for r in m.get("relationships", []):
        declared_keys = set()
        for key in ('join_key', 'join_key_from', 'join_key_to', 'from_columns', 'to_columns'):
            value = r.get(key)
            declared_keys.update([value] if isinstance(value, str) else value or [])
        if (r.get("from") in affected_ds or r.get("to") in affected_ds
                or declared_keys & field_names):
            aff_rels.append(f"{r.get('from')} → {r.get('to')}（{r.get('type', '?')}"
                            f"/{r.get('join_key', '-')}）")
    for p in m.get("multi_hop_paths", []):
        nodes = set(p.get("path") or [])
        join_fields = {str(j).split(".")[-1] for pair in (p.get("joins") or []) for j in pair}
        if nodes & affected_ds or join_fields & field_names:
            aff_paths.append(" → ".join(p.get("path") or []))

    # ---- gold 用例回归面 ----
    case_hits = []
    if args.cases:
        cases = json.load(open(args.cases, encoding="utf-8"))
        src_tables = {ds_by_name[dn].get("source") for dn in affected_ds if dn in ds_by_name}
        names = {mt.get("name") for mt in m.get("metrics", [])
                 if f"{mt.get('id')}（{mt.get('name')}）" in aff_metrics}
        for c in cases:
            sql = c.get("gold_sql") or ""
            if any(mentions(sql, tbl) for tbl in src_tables if tbl):
                case_hits.append(f"{c.get('id')}: {c.get('question', '')[:40]}")
            elif any(n and n in (c.get("question") or "") for n in names):
                case_hits.append(f"{c.get('id')}: {c.get('question', '')[:40]}（问句命中）")

    # ---- 输出 ----
    print(f"# 影响面分析：{t}\n")
    if hit_datasets:
        print(f"命中数据集：{[d['name'] for d in hit_datasets]}")
    if hit_fields:
        print(f"命中字段：{hit_fields}")
    if hit_metrics:
        print(f"命中指标：{[x['id'] for x in hit_metrics]}")
    if hit_concepts:
        print(f"命中概念：{[c['term'] for c in hit_concepts]}")
    print(f"\n受影响数据集（{len(affected_ds)}）：{sorted(affected_ds)}")
    print(f"受影响概念（{len(aff_concepts)}）：{sorted(aff_concepts) or '无'}")
    print(f"受影响指标（{len(aff_metrics)}）：")
    for x in sorted(aff_metrics):
        print(f"  - {x}")
    print(f"受影响关系（{len(aff_rels)}）：")
    for x in aff_rels:
        print(f"  - {x}")
    if aff_paths:
        print(f"受影响多跳路径（{len(aff_paths)}）：")
        for x in aff_paths:
            print(f"  - {x}")
    if args.cases:
        print(f"需回归的 gold 用例（{len(case_hits)}）：")
        for x in case_hits:
            print(f"  - {x}")
    print("\n建议：改动落地后，对上述用例跑 run_eval.py 定向回归，再走 release_gate.py。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
