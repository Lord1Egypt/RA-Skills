#!/usr/bin/env python3
"""gen_metadata.py — 建模段：宽表 DDL + 实测画像 → meta/*.yaml 草稿（ai-data-delivery v0.0.4）

生成表级 15 项 / 字段级 12 项的元数据骨架：枚举值从 profile 自动填实测值，
敏感字段按命名模式预标记（sensitive + allow_llm: false），维度/度量/时间角色自动推断。
草稿必须人审（中文名、粒度、口径表达式是机器猜不了的）。

用法：
  python gen_metadata.py --tables inventory/tables.yaml --columns inventory/columns.yaml \
      --profile inventory/profile.yaml --out meta/

角色推断：pk（DDL 主键）→ fk（非主键 *_id）→ time（时间列）→ measure（数值 + 度量命名）
         → attr（描述/编码类文本）→ dim（其余文本）。
"""
import argparse
import os
import re
import sys
from collections import defaultdict

import yaml
from _contract import load

MEASURE_HINT = re.compile(r"_cnt$|_count$|_days$|_rate$|_sec$|_hours$|_minutes$|"
                          r"_amount$|_total$|_num$|_years$|mileage|duration", re.I)
ATTR_HINT = re.compile(r"_no$|_code$|_desc$|_name$|编号|代码|描述", re.I)
SENSITIVE_PAT = re.compile(r"身份证|手机号|电话|资格证号|证件号|id_card|phone|mobile", re.I)
FLAG_HINT = re.compile(r"^is_|^has_|^flag_|_flag$|_yn$", re.I)   # 0/1 标志位 → 维度
TIME_NAME = re.compile(r"_date$|_time$|_at$|deadline$|_year$|_month$", re.I)


def guess_role(c, is_pk, enum_values=None):
    if is_pk:
        return "pk"
    name, ctype = c["name"], (c.get("type") or "").upper()
    if c["name"].endswith("_id"):
        return "fk"
    if FLAG_HINT.search(name):
        return "dim"  # is_overdue 这类标志位是维度，不是度量
    if enum_values and {str(v) for v in enum_values} <= {"0", "1"}:
        return "dim"  # 实测取值只有 0/1 → 布尔维度
    if TIME_NAME.search(name):
        return "time"  # 严格后缀命名即时间列（ingest 侧 is_time 只做参考，不再双重门槛）
    numeric = any(k in ctype for k in ("INT", "REAL", "NUMERIC", "DECIMAL", "DOUBLE", "FLOAT"))
    if numeric and MEASURE_HINT.search(c["name"]):
        return "measure"
    if numeric:
        return "measure"
    if ATTR_HINT.search(c["name"]):
        return "attr"
    return "dim"


def main():
    ap = argparse.ArgumentParser(description="宽表元数据草稿生成")
    ap.add_argument("--tables", required=True)
    ap.add_argument("--columns", required=True)
    ap.add_argument("--profile", default=None, help="profile.yaml（枚举实测值/空值率自动填充）")
    ap.add_argument("--out", required=True, help="输出目录（meta/）")
    args = ap.parse_args()

    tables = load(args.tables)["tables"]
    columns = load(args.columns)
    profile = {}
    if args.profile:
        p = load(args.profile)
        profile = {t["name"]: {c["name"]: c for c in t["columns"]} for t in p["tables"]}

    by_table = defaultdict(list)
    for c in columns:
        by_table[c["table"]].append(c)

    os.makedirs(args.out, exist_ok=True)
    for t in tables:
        name = t["name"]
        cols, dims, measures, times = [], [], [], []
        for c in by_table.get(name, []):
            pc = profile.get(name, {}).get(c["name"])
            role = guess_role(c, c.get("pk"), (pc or {}).get("enum_values"))
            rec = {"name": c["name"], "cn": c.get("comment") or "【待填中文名】", "role": role,
                   "type": (c.get("type") or "").lower()}
            if c.get("comment"):
                rec["cn_source"] = "DDL COMMENT 预填，人审确认"
            if pc:
                if pc.get("enum_values") and role == "dim":
                    rec["enum"] = {v: f"【待确认含义：{v}】" for v in pc["enum_values"]}
                if pc.get("null_rate", 0) > 0.5:
                    rec["note"] = f"空值率 {pc['null_rate']:.0%}，口径需谨慎"
            if SENSITIVE_PAT.search(c["name"]):
                rec["sensitive"] = True
                rec["allow_llm"] = False
            if role == "measure":
                rec["aggregatable"] = "sum"  # 比率型必须改 formula + no_row_avg，人审
            cols.append(rec)
            {"dim": dims, "measure": measures, "time": times}.get(role, dims).append(c["name"]) \
                if role in ("dim", "measure", "time") else None

        meta = {
            "table": name,
            "cn_name": "【待填】",
            "grain": "【必填：一行代表什么】",
            "refresh": "【待填：如 daily 02:30】",
            "description": "【待填：能答什么/不能答什么/必带过滤——写给模型的路由+边界指令】",
            "primary_key": [c["name"] for c in by_table.get(name, []) if c.get("pk")],
            "dimensions": dims, "measures": measures, "time_fields": times,
            "time_fence": "【必填：可查询最新数据日期，随抽取更新】",
            "sources": ["【待填：上游来源表】"],
            "metrics": ["【待填：覆盖的指标 id】"],
            "owner": "产品/FDE", "status": "草案",
            "columns": cols,
        }
        with open(os.path.join(args.out, f"{name}.yaml"), "w", encoding="utf-8") as f:
            yaml.safe_dump(meta, f, allow_unicode=True, sort_keys=False, width=120)

    print(f"生成 {len(tables)} 份元数据草稿 → {args.out}/")
    print("提醒：【】占位项与 aggregatable 默认值必须人审；比率型度量必须改 formula + no_row_avg")
    return 0


if __name__ == "__main__":
    sys.exit(main())
