#!/usr/bin/env python3
"""profile_db.py — 盘点段：连库出实测画像（ai-data-delivery v0.0.4）

对源库逐表实测：行数、枚举实测值（低基数列）、空值率、近似粒度（唯一键基数）。
敏感列（身份证/手机号等）只出计数与空值率，不取样值。

用法：
  python profile_db.py --db path/to.db --out inventory/profile.yaml [--enum-max 20]

输出 profile.yaml：
  tables[]: name / row_count / columns[]{name,type,distinct,null_rate,enum_values?,note}
"""
import os
import argparse
import re
import sqlite3
import sys

import yaml

SENSITIVE_PAT = re.compile(r"身份证|手机号|电话|资格证号|证件号|id_card|phone|mobile", re.I)


def profile_table(conn, table, enum_max):
    cols = conn.execute(f"PRAGMA table_info('{table}')").fetchall()
    # PRAGMA: cid, name, type, notnull, dflt_value, pk
    row_count = conn.execute(f"SELECT COUNT(*) FROM '{table}'").fetchone()[0]
    out_cols = []
    for _, cname, ctype, _, _, pk in cols:
        rec = {"name": cname, "type": ctype or "", "pk": bool(pk)}
        n = conn.execute(
            f"SELECT COUNT(DISTINCT \"{cname}\") FROM '{table}'").fetchone()[0]
        nulls = conn.execute(
            f"SELECT COUNT(*) FROM '{table}' WHERE \"{cname}\" IS NULL").fetchone()[0]
        rec["distinct"] = n
        rec["null_rate"] = round(nulls / row_count, 4) if row_count else 0
        if pk and row_count:
            rec["grain_hint"] = "唯一" if n == row_count else f"有重复({row_count - n} 行)"
        if SENSITIVE_PAT.search(cname):
            rec["note"] = "敏感列：不取样"
        elif 0 < n <= enum_max:
            vals = [r[0] for r in conn.execute(
                f"SELECT DISTINCT \"{cname}\" FROM '{table}' WHERE \"{cname}\" IS NOT NULL "
                f"ORDER BY 1 LIMIT {enum_max}").fetchall()]
            rec["enum_values"] = [str(v) for v in vals]
        out_cols.append(rec)
    return {"name": table, "row_count": row_count, "columns": out_cols}


def main():
    ap = argparse.ArgumentParser(description="源库实测画像")
    ap.add_argument("--db", required=True)
    ap.add_argument("--out", required=True, help="输出文件路径（如 profile.yaml；注意：是文件不是目录）")
    ap.add_argument("--enum-max", type=int, default=20, help="枚举候选列的基数上限")
    args = ap.parse_args()

    if os.path.isdir(args.out):
        print(f"错误：--out 应为输出文件路径（如 profile.yaml），不是目录：{args.out}", file=sys.stderr)
        return 2
    if not os.path.isfile(args.db):
        print(f"错误：--db 数据库文件不存在：{args.db}\n"
              f"检查路径拼写；相对路径以当前工作目录为基准。", file=sys.stderr)
        return 2

    conn = sqlite3.connect(args.db)
    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
    profile = [profile_table(conn, t, args.enum_max) for t in sorted(tables)]
    conn.close()

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        yaml.safe_dump({"db": args.db, "table_count": len(profile), "tables": profile},
                       f, allow_unicode=True, sort_keys=False)
    enum_cols = sum(1 for t in profile for c in t["columns"] if "enum_values" in c)
    print(f"画像完成：{len(profile)} 张表，{enum_cols} 个枚举候选列 → {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
