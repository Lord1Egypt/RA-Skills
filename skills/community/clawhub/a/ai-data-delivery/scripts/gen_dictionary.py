#!/usr/bin/env python3
"""gen_dictionary.py — 运营段：指标口径字典生成（ai-data-delivery v0.0.4）

RULE-CONSUME-01：模型只有沉淀为"人能读的口径字典"，信息中心与甲方才接得住、审得了。
从 semantic.yaml 一键生成 markdown 字典：数据集 / 业务概念 / 指标口径（含文号依据）/
未结构化清单（治理 backlog）。

用法：python gen_dictionary.py --model semantic.yaml --out dictionary.md
"""
import os
import argparse
import sys
import json

import yaml
from _contract import load


def fmt_metric(m):
    parts = []
    if m.get("expr"):
        parts.append(f"`{m['expr']}`")
    elif m.get("numerator") and m.get("denominator"):
        parts.append(f"`{m['numerator'].get('expr')}` / `{m['denominator'].get('expr')}`")
    else:
        parts.append("（未结构化）")
    scopes = []
    for f in m.get('filters') or []:
        scopes.append(f"{f.get('field', '字段待定')} IN {json.dumps(f.get('values', []), ensure_ascii=False)}")
    if m.get('extra_where'):
        scopes.append(m['extra_where'])
    if scopes:
        parts.append('WHERE ' + ' AND '.join('(' + item + ')' for item in scopes))
    return ' '.join(parts).replace('|', '&#124;').replace('\n', '<br>')


def main(argv=None):
    ap = argparse.ArgumentParser(description="指标口径字典生成")
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    m = load(args.model)
    ds_list = m.get("datasets", [])
    metrics = m.get("metrics", [])
    concepts = m.get("concepts", [])
    structured = [x for x in metrics if x.get("structured")]

    L = []
    L.append(f"# {m.get('name', '语义模型')} 口径字典")
    L.append("")
    L.append(f"- 模型版本：{m.get('version', '?')}")
    L.append(f"- 数据集 {len(ds_list)} 个 / 指标 {len(metrics)} 个（结构化 {len(structured)} 个）"
             f" / 业务概念 {len(concepts)} 个 / 关系 {len(m.get('relationships', []))} 条")
    if m.get("tenant_dimension"):
        L.append(f"- 租户维度：{m['tenant_dimension']}")
    L.append("")

    L.append("## 一、数据集（宽表）")
    L.append("")
    L.append("| 数据集 | 物理表 | 粒度 | 字段数 |")
    L.append("| --- | --- | --- | --- |")
    for d in ds_list:
        L.append(f"| {d.get('name')} | {d.get('source', '?')} | {d.get('grain', '?')} "
                 f"| {len(d.get('fields', []))} |")
    L.append("")

    L.append("## 二、业务概念（同义词与展开口径）")
    L.append("")
    L.append("| 概念 | 别名 | 展开口径 | 说明 |")
    L.append("| --- | --- | --- | --- |")
    for c in concepts:
        ex = c.get("expand") or {}
        expand = (f"`{ex.get('dataset')}.{ex.get('field')}` ∈ {ex.get('values')}"
                  if ex else "—")
        L.append(f"| {c.get('term')} | {('、'.join(c.get('aliases') or []) or '—')} "
                 f"| {expand} | {c.get('note', '—')} |")
    L.append("")

    L.append("## 三、指标口径")
    L.append("")
    L.append("| 指标 | 名称 | 数据集 | 口径 | 时间字段 | 依据 | 状态 |")
    L.append("| --- | --- | --- | --- | --- | --- | --- |")
    for x in metrics:
        cal = x.get("caliber") or {}
        basis = cal.get("basis", "—")
        note = cal.get("note", "")
        basis_cell = basis + (f"（{note}）" if note else "")
        time_label = '当前状态' if x.get('time_requirement') == 'current' else (x.get('time_field') or '待明确')
        L.append(f"| {x.get('id')} | {x.get('name')} | {x.get('dataset', '—')} "
                 f"| {fmt_metric(x)} | {time_label} | {basis_cell} "
                 f"| {x.get('status', '?')} |")
    L.append("")

    unstr = [x for x in metrics if not x.get("structured")]
    L.append("## 四、未结构化指标清单（治理 backlog）")
    L.append("")
    if unstr:
        L.append("以下指标有定义但未落地为可执行口径，按优先级推进结构化：")
        L.append("")
        for x in unstr:
            L.append(f"- **{x.get('name')}**（{x.get('id')}，{x.get('dataset', '无挂载')}）"
                     f"：{x.get('formula', x.get('legacy_formula', '无公式'))}")
    else:
        L.append("（无）")
    L.append("")

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"字典已生成 → {args.out}")
    print(f"  数据集 {len(ds_list)} / 指标 {len(metrics)}（结构化 {len(structured)}）"
          f" / 概念 {len(concepts)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
