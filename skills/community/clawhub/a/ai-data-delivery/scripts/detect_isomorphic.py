#!/usr/bin/env python3
"""detect_isomorphic.py — 盘点段：同构表族检测（ai-data-delivery v0.0.4）

发现 smart_check_record_item1~30 这类"同一结构、按序号拆表"的表族——
不合并则跨项聚合问题永久无解（本项目实测最关键的一刀）。

判定（满足其一即为一族）：
  1. 序号命名：表名去序号后缀后相同（item1..item30 / log_202401..log_202412）
  2. 结构指纹相同：字段名+类型集合一致（≥3 张才报）

用法：
  python detect_isomorphic.py --tables inventory/tables.yaml --columns inventory/columns.yaml \
      --out inventory/isomorphic.yaml
"""
import os
import argparse
import re
import sys
from collections import defaultdict

import yaml
from _contract import load

def family_key(name):
    """序号归一：名内数字段替换为 #（item1_detail→item#_detail；log_202401→log_#）。
    含数字才返回 stem，否则 None。"""
    if not re.search(r"\d", name):
        return None
    return re.sub(r"\d+", "#", name)


def main():
    ap = argparse.ArgumentParser(description="同构表族检测")
    ap.add_argument("--tables", required=True)
    ap.add_argument("--columns", required=True)
    ap.add_argument("--out", required=True, help="输出文件路径（如 isomorphic.yaml；注意：是文件不是目录）")
    args = ap.parse_args()

    if os.path.isdir(args.out):
        print(f"错误：--out 应为输出文件路径（如 isomorphic.yaml），不是目录：{args.out}", file=sys.stderr)
        return 2

    tables_doc = load(args.tables)
    if not isinstance(tables_doc, dict) or "tables" not in tables_doc:
        print(f"错误：--tables 文件缺少顶层键 tables:：{args.tables}", file=sys.stderr)
        return 2
    cols = load(args.columns)
    if not isinstance(cols, list):
        print(f"错误：--columns 文件应为列清单（YAML 列表，每项含 table/name/type）：{args.columns}",
              file=sys.stderr)
        return 2
    tables = tables_doc["tables"]
    sig = defaultdict(list)
    for c in cols:
        sig[c["table"]].append(f'{c["name"]}:{c["type"]}')
    fingerprint = {t["name"]: tuple(sorted(sig.get(t["name"], []))) for t in tables}

    # 序号族
    by_stem = defaultdict(list)
    for t in tables:
        stem = family_key(t["name"])
        if stem:
            by_stem[stem].append(t["name"])
    # 结构族
    by_fp = defaultdict(list)
    for name, fp in fingerprint.items():
        if fp:
            by_fp[fp].append(name)

    families, seen = [], set()
    for stem, members in sorted(by_stem.items()):
        if len(members) >= 2:
            merged_name = re.sub(r"_+", "_", stem.replace("#", "x")).strip("_")
            families.append({"kind": "序号命名", "stem": stem,
                             "members": sorted(members), "count": len(members),
                             "same_schema": len({fingerprint[x] for x in members}) == 1,
                             "suggestion": f"合并为 1 张宽表（UNION ALL + 新增编码维度列），如 dws_{merged_name}"})
            seen.update(members)
    for fp, members in sorted(by_fp.items(), key=lambda kv: -len(kv[1])):
        rest = [x for x in members if x not in seen]
        if len(rest) >= 3:
            families.append({"kind": "结构相同", "members": sorted(rest), "count": len(rest),
                             "suggestion": "结构指纹一致，评估合并"})
            seen.update(rest)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        yaml.safe_dump({"family_count": len(families), "families": families},
                       f, allow_unicode=True, sort_keys=False)
    if families:
        for fam in families:
            print(f"发现同构族[{fam['kind']}]：{fam.get('stem', '')} × {fam['count']} 张"
                  f" → {fam['suggestion']}")
    else:
        print("未发现同构表族（若源表已按主题域合并建模，此为预期结果）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
