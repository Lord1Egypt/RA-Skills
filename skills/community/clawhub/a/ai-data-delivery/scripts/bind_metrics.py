#!/usr/bin/env python3
"""bind_metrics.py — 建模段：指标 → 宽表字段绑定建议（ai-data-delivery v0.0.4）

把 metrics_raw 的每条指标绑到宽表数据集：来源表 → meta sources 反查宽表；
口径式标识符 ∩ 数据集字段 → 字段级绑定证据。绑不上的进缺口台账。

用法：
  python bind_metrics.py --metrics-raw inventory/metrics_raw.yaml \
      --meta meta/ --model semantic.yaml --out bindings.yaml

输出 bindings.yaml：每条指标 {bind: 数据集|null, fields: 命中字段, missing: 缺口字段, status}
  status ∈ 可绑定 / 部分绑定（字段缺口） / 表级缺口（无宽表认领来源表） / 无来源
"""
import argparse
import os
import re
import sys

import yaml
from _contract import load

IDENT = re.compile(r"\b([a-zA-Z_]\w*)\b")
SQL_KEYWORDS = {"select", "from", "where", "and", "or", "not", "in", "is", "null", "count",
                "sum", "avg", "max", "min", "round", "distinct", "as", "by", "group", "order",
                "desc", "asc", "limit", "date", "curdate", "case", "when", "then", "else", "end",
                "like", "between", "join", "on", "left", "right", "inner", "union", "all"}


def formula_fields(formula):
    """抽取口径式里疑似字段的标识符（去 SQL 关键字、去表名前缀）。"""
    sql = re.sub(r"'[^']*'", "", formula or "")
    ids = set()
    for tok in IDENT.findall(sql):
        low = tok.lower()
        if low not in SQL_KEYWORDS and not low.isdigit():
            ids.add(tok.split(".")[-1])
    return ids


def expand_source(src):
    """展开范围写法：smart_check_record_item1_detail .. item30_detail → 30 个表名。"""
    m = re.match(r"^(.*?)(\d+)(.*?)\s*\.\.\s*(\S+)$", src)
    if not m:
        return [src]
    head, n1, tail, rhs = m.group(1), int(m.group(2)), m.group(3), m.group(4)
    m2 = re.search(r"(\d+)", rhs)  # 右端允许缩写（item30_detail），只取其序号
    if not m2:
        return [src]
    n2 = int(m2.group(1))
    if n2 < n1 or n2 - n1 > 500:
        return [src]
    return [f"{head}{i}{tail}" for i in range(n1, n2 + 1)]


def main():
    ap = argparse.ArgumentParser(description="指标→宽表字段绑定建议")
    ap.add_argument("--metrics-raw", required=True)
    ap.add_argument("--meta", required=True, help="meta/ 目录（用 sources 反查）")
    ap.add_argument("--model", default=None, help="semantic.yaml（字段级校验，可选但推荐）")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    raw = load(args.metrics_raw)["metrics"]

    # 来源表 → 宽表 反查表（meta sources）
    table2dws = {}
    meta_fields = {}
    for fn in os.listdir(args.meta):
        if not fn.endswith((".yaml", ".yml")):
            continue
        meta = load(os.path.join(args.meta, fn))
        for src in meta.get("sources", []) or []:
            if isinstance(src, str) and not src.startswith("【"):
                for expanded in expand_source(src):
                    table2dws.setdefault(expanded, meta["table"])
        meta_fields[meta["table"]] = {c["name"] for c in meta.get("columns", [])}

    # 模型字段（更权威的字段校验来源）
    model_fields, model_sources = {}, {}
    if args.model:
        m = load(args.model)
        for ds in m.get("datasets", []):
            model_fields[ds["name"]] = {f["name"] for f in ds.get("fields", [])}
            model_sources[ds.get("source")] = ds["name"]

    bindings, dist = [], {}
    for r in raw:
        src = r.get("source_table")
        status, dws, note = None, None, ""
        if r.get("status") == "无来源":
            status, note = "无来源", r.get("reason", "")
        else:
            dws = table2dws.get(src) or model_sources.get(src)
            if not dws:
                status, note = "表级缺口", f"来源表 {src!r} 未被任何宽表 sources 认领"
            else:
                fields = formula_fields(r.get("formula_raw"))
                fields.discard(src)  # FROM 后的来源表名不是字段
                fields -= set(table2dws.keys())  # 其它已知表名同样剔除
                known = model_fields.get(dws) or meta_fields.get(dws) or set()
                hit = sorted(f for f in fields if f in known)
                missing = sorted(f for f in fields - set(hit)
                                 if not re.fullmatch(r"[a-z]{1,3}", f))  # 过滤短别名噪音
                status = "可绑定" if not missing else "部分绑定"
                note = "" if not missing else f"字段缺口：{missing}"
                bindings.append({"metric_id": r["id"], "metric_name": r["name"],
                                 "source_table": src, "dataset": dws,
                                 "fields_hit": hit, "fields_missing": missing,
                                 "status": status, "note": note})
                dist[status] = dist.get(status, 0) + 1
                continue
        bindings.append({"metric_id": r["id"], "metric_name": r["name"],
                         "source_table": src, "dataset": dws,
                         "fields_hit": [], "fields_missing": [], "status": status, "note": note})
        dist[status] = dist.get(status, 0) + 1

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        yaml.safe_dump({"total": len(bindings), "status_dist": dist, "bindings": bindings},
                       f, allow_unicode=True, sort_keys=False)
    print(f"绑定完成：{dist}（共 {len(bindings)} 条）→ {args.out}")
    print("提醒：绑定是提案——口径由 PM 确认，来源由信息中心确认，写模型走 patch_model.py --db 验算")
    return 0


if __name__ == "__main__":
    sys.exit(main())
