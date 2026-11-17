#!/usr/bin/env python3
"""harvest_metrics.py — 盘点段：既有指标库 → metrics_raw.yaml（ai-data-delivery v0.0.4）

把既有指标/报表导出（哪怕是中文伪代码 SQL）收成结构化盘点资产，
每条指标三分：可执行候选 / 需改写（伪代码） / 无来源（数据缺口）。

用法：
  python harvest_metrics.py --metrics 指标与规则全量导出.json --out inventory/
  python harvest_metrics.py --model semantic.yaml --out inventory/        # 存量模型收割（legacy_formula）
  python harvest_metrics.py --metrics x.json --mapping 表名映射.yaml --out inventory/

存量项目要点：导出记录往往没有 table 字段——本工具自动从口径式 FROM 子句解析来源表；
中文/拼音源表名用 --mapping（yaml：{源表名: 物理宽表名}）映射到宽表，不再误判"无来源"；
宽表 meta 已建成时直接 `--from-meta meta/`，从 meta 的 sources 字段自动派生映射（范围写法自动展开）。

输入兼容：JSON/YAML，顶层为 list 或含 metrics 键的 dict；
记录字段按名兼容：id/name/table(或 tbl)/data_type(或 type)/formula(或 sql)/category/dims/status。

输出：
  metrics_raw.yaml  全量清单（含 status 三分与理由、映射后物理表）
  gaps.yaml         数据缺口台账（无来源指标逐条登记，供信息中心闭环）
"""
import argparse
import json
import os
import re
import sys

import yaml
from _contract import load as contract_load

CJK = re.compile(r"[一-鿿]")
FROM_RE = re.compile(r"\bFROM\s+([A-Za-z_][\w$]*|[一-鿿][\w$一-鿿]*)", re.I)


def load(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f) if path.endswith(".json") else yaml.safe_load(f)
    if isinstance(data, dict):
        for k in ("metrics", "指标", "items"):
            if k in data:
                return data[k]
        raise ValueError("找不到指标清单键（metrics/指标/items）")
    return data


def load_from_model(path):
    """存量场景：直接收割 semantic.yaml 里的 legacy_formula。"""
    m = contract_load(path)
    out = []
    for mt in m.get("metrics", []):
        out.append({"id": mt.get("id"), "name": mt.get("name"),
                    "type": mt.get("type"),
                    "table": None,  # 交给 FROM 解析 + mapping
                    "dataset": mt.get("dataset"),
                    "formula": mt.get("legacy_formula") or mt.get("formula") or "",
                    "category": mt.get("category_16") or mt.get("category"),
                    "status": mt.get("status")})
    return out


def strip_literals(sql):
    """去掉字符串字面量后再判断标识符是否含中文。"""
    return re.sub(r"'[^']*'", "''", sql or "")


def parse_from_table(formula):
    m = FROM_RE.search(formula or "")
    return m.group(1) if m else None


def expand_source(s):
    """sources 范围写法展开：smart_check_record_item1_detail .. item30_detail → 30 个表名。"""
    m = re.match(r"^(.*?)(\d+)(.*?)\s*\.\.\s*(.*?)(\d+)(.*?)$", str(s))
    if not m:
        return [str(s)]
    a, b = int(m.group(2)), int(m.group(5))
    if b < a or b - a > 500:
        return [str(s)]
    w = len(m.group(2))
    return [f"{m.group(1)}{i:0{w}d}{m.group(3)}" for i in range(a, b + 1)]


def mapping_from_meta(meta_dir):
    """从宽表 meta 目录派生 源表→宽表 映射（sources 字段，范围写法展开）。
    返回 (mapping, 占位sources的表清单)：sources 还是【待填】占位的表不参与映射并点名提醒。"""
    import glob
    mapping, placeholder_tables = {}, []
    for p in sorted(glob.glob(os.path.join(meta_dir, "*.yaml"))):
        m = contract_load(p)
        if not m or not m.get("table"):
            continue
        sources = m.get("sources") or []
        if any("【" in str(s) for s in sources):
            placeholder_tables.append(m["table"])
        for s in sources:
            if "【" in str(s):
                continue
            for t in expand_source(s):
                mapping[t] = m["table"]
    return mapping, placeholder_tables


def classify(rec, mapping):
    table = (rec.get("table") or rec.get("tbl") or "").strip()
    formula = (rec.get("formula") or rec.get("sql") or "").strip()
    mapped = None
    if not table:
        table = parse_from_table(formula) or ""
    if table and mapping and table in mapping:
        mapped = mapping[table]
    if not table or table in ("-", "—") or "NO_TABLE" in formula:
        return "无来源", "来源表缺失（无 table 字段且口径式无 FROM 可解析），记数据缺口", None
    if not formula:
        return "需改写", "无口径式，需人工补口径", mapped
    if CJK.search(strip_literals(formula)):
        if mapped:
            return "需改写", f"中文伪代码口径；表已映射 {table} → {mapped}，剩列名/枚举翻译", mapped
        return "需改写", f"口径式为中文伪代码（标识符含中文），源表 {table} 待映射", mapped
    if mapped:
        return "可执行候选", f"口径式形态可执行；表映射 {table} → {mapped}（仍需落宽表字段并验算）", mapped
    return "可执行候选", "口径式形态可执行（仍需落宽表字段并验算）", mapped


def main():
    ap = argparse.ArgumentParser(description="既有指标库盘点收割")
    ap.add_argument("--metrics", help="指标导出 json/yaml")
    ap.add_argument("--model", help="semantic.yaml（存量模型收割 legacy_formula）")
    ap.add_argument("--mapping", help="表名映射 yaml：{源表名: 物理宽表名}")
    ap.add_argument("--from-meta", dest="from_meta",
                    help="宽表 meta 目录：从 sources 字段自动派生映射（与 --mapping 可叠加，显式映射优先）")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    if not args.metrics and not args.model:
        print("错误：需 --metrics 或 --model", file=sys.stderr)
        return 2

    raw = load_from_model(args.model) if args.model else load(args.metrics)
    mapping = {}
    if args.from_meta:
        meta_map, placeholder_tables = mapping_from_meta(args.from_meta)
        mapping.update(meta_map)
        if placeholder_tables:
            print(f"提醒：以下宽表 meta 的 sources 仍是占位，未参与映射（先补 sources 或显式 --mapping）："
                  f"{placeholder_tables}", file=sys.stderr)
    if args.mapping:
        mapping.update(contract_load(args.mapping) or {})

    out, gaps = [], []
    for r in raw:
        status, reason, mapped = classify(r, mapping)
        item = {"id": r.get("id"), "name": r.get("name"),
                "type": r.get("data_type") or r.get("type"),
                "source_table": (r.get("table") or r.get("tbl") or "").strip()
                                or parse_from_table(r.get("formula") or r.get("sql") or ""),
                "mapped_table": mapped,
                "category": r.get("category") or None,
                "dims": r.get("dims") or [],
                "formula_raw": (r.get("formula") or r.get("sql") or "").strip(),
                "status": status, "reason": reason,
                "rule_bound": bool(r.get("is_rule_source"))}
        out.append(item)
        if status == "无来源":
            gaps.append({"metric_id": item["id"], "metric_name": item["name"],
                         "issue": "无来源表", "owner": "信息中心",
                         "action": "确认数据源接入或显式标记暂不落地"})

    from collections import Counter
    dist = Counter(i["status"] for i in out)
    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "metrics_raw.yaml"), "w", encoding="utf-8") as f:
        yaml.safe_dump({"total": len(out), "status_dist": dict(dist), "metrics": out},
                       f, allow_unicode=True, sort_keys=False)
    with open(os.path.join(args.out, "gaps.yaml"), "w", encoding="utf-8") as f:
        yaml.safe_dump({"gap_count": len(gaps), "gaps": gaps}, f, allow_unicode=True, sort_keys=False)

    print(f"收割 {len(out)} 个指标：{dict(dist)}")
    n_mapped = sum(1 for i in out if i["mapped_table"])
    if n_mapped:
        print(f"表名映射命中 {n_mapped} 条（mapped_table 已写入）")
    print(f"数据缺口 {len(gaps)} 条 → gaps.yaml（信息中心闭环依据）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
