#!/usr/bin/env python3
"""check_consistency.py — 运营段：上游表结构漂移巡检（ai-data-delivery v0.0.4）

RULE-STATE-01 的运营面：语义模型/宽表 meta 是对物理库的"快照承诺"，上游加列、删列、
换类型后模型不会自动知道——巡检比对，漂移即报警。

用法：
  python check_consistency.py --meta meta/ --db physical.db        # meta/*.yaml vs 物理库
  python check_consistency.py --model semantic.yaml --db physical.db

判定：
  ERROR 表消失 / 字段消失（meta 承诺了但库里没有）→ 模型会答错，必须修
  WARN  库里新增字段（meta 未收录，可能是新能力）/ 类型宽严变化
退出码：0 无 ERROR；1 有 ERROR；2 用法错误。
"""
import argparse
import glob
import os
import sqlite3
import sys

import yaml
from _contract import load

TYPE_CLASSES = {
    "int": "num", "integer": "num", "bigint": "num", "smallint": "num",
    "float": "num", "double": "num", "real": "num", "decimal": "num", "numeric": "num",
    "varchar": "text", "char": "text", "text": "text", "string": "text", "nvarchar": "text",
    "date": "time", "datetime": "time", "timestamp": "time", "time": "time",
}


def type_class(t):
    t = (t or "").lower().split("(")[0].strip()
    return TYPE_CLASSES.get(t, t or "unknown")


def db_structure(db_path):
    conn = sqlite3.connect(db_path)
    tables = {}
    for (tbl,) in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
        cols = {r[1]: r[2] for r in conn.execute(f"PRAGMA table_info({tbl})")}
        tables[tbl] = cols
    conn.close()
    return tables


def load_expectations(args):
    """返回 {物理表名: {字段名: 类型}}"""
    exp = {}
    if args.meta:
        for p in sorted(glob.glob(os.path.join(args.meta, "*.yaml"))):
            m = load(p)
            if not m or not m.get("table"):
                continue
            exp[m["table"]] = {c["name"]: c.get("type", "") for c in m.get("columns", [])}
    elif args.model:
        m = load(args.model)
        for ds in m.get("datasets", []):
            tbl = ds.get("source") or ds.get("name")
            exp[tbl] = {f["name"]: f.get("type", "") for f in ds.get("fields", [])}
    return exp


def main():
    ap = argparse.ArgumentParser(description="上游表结构漂移巡检")
    ap.add_argument("--meta", help="宽表 meta 目录（*.yaml）")
    ap.add_argument("--model", help="semantic.yaml（与 --meta 二选一）")
    ap.add_argument("--db", required=True, help="物理库（sqlite）")
    args = ap.parse_args()
    if not args.meta and not args.model:
        print("错误：需 --meta 或 --model", file=sys.stderr)
        return 2

    actual = db_structure(args.db)
    expected = load_expectations(args)
    errors, warns = [], []

    for tbl, cols in sorted(expected.items()):
        if tbl not in actual:
            errors.append(f"表 {tbl} 在物理库中不存在")
            continue
        db_cols = actual[tbl]
        for c, t in sorted(cols.items()):
            if c not in db_cols:
                errors.append(f"{tbl}.{c} 字段消失（meta 承诺了，库里没有）")
            elif type_class(t) != type_class(db_cols[c]) and "unknown" not in (
                    type_class(t), type_class(db_cols[c])):
                warns.append(f"{tbl}.{c} 类型变化：meta={t} vs 库={db_cols[c]}")
        for c in sorted(set(db_cols) - set(cols)):
            warns.append(f"{tbl}.{c} 库中新增字段，meta 未收录")

    for w in warns:
        print(f"[WARN] {w}")
    for e in errors:
        print(f"[ERROR] {e}")
    print(f"\n巡检 {len(expected)} 张表：ERROR {len(errors)}，WARN {len(warns)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
