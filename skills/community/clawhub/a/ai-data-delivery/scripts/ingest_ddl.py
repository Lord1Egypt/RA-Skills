#!/usr/bin/env python3
"""ingest_ddl.py — 盘点段：DDL → 源表清单（ai-data-delivery v0.0.5）

把"所有业务系统的 SQL 结构"变成可计算的盘点资产。

用法：
  python ingest_ddl.py --ddl path/to/ddl.sql [--ddl more.sql] --out inventory/
  python ingest_ddl.py --ddl-dir path/to/sql_dir --out inventory/

输出（inventory/ 下）：
  tables.yaml   每表：字段数、主键猜测、时间列、命名前缀、来源文件
  columns.yaml  每表每字段：名/类型/是否主键/是否疑似时间列

支持 MySQL/SQLite 方言的 CREATE TABLE；注释（-- 与 # 行尾、COMMENT 'x'）尽量保留。
"""
import argparse
import os
import re
import sys
from collections import Counter

import yaml

TIME_NAME_HINT = re.compile(r"_date$|_time$|_at$|deadline$|_year$|_month$|_day$|^rq$|^sj$", re.I)
TIME_TYPE_HINT = re.compile(r"DATE|TIME", re.I)


def is_time_col(cname, ctype):
    """时间列双重判定：严格后缀名 或 类型含 DATE/TIME。
    （子串 day/date 会误伤 overdue_days 这类时长度量，漏判 deadline 这类裸名。）"""
    return bool(TIME_NAME_HINT.search(cname) or TIME_TYPE_HINT.search(ctype))
COL_RE = re.compile(
    r"^\s*[`\"]?(\w+)[`\"]?\s+([A-Za-z]+(?:\s*\([^)]*\))?(?:\s+UNSIGNED)?)(.*)$", re.I | re.S)
PK_INLINE = re.compile(r"PRIMARY\s+KEY", re.I)
COMMENT_RE = re.compile(r"COMMENT\s+'([^']*)'", re.I)


def split_columns(body):
    """Top-level commas only; preserve commas inside types and quoted defaults."""
    parts, start, depth, quoted, index = [], 0, 0, None, 0
    while index < len(body):
        char = body[index]
        if quoted:
            if char == quoted:
                if index + 1 < len(body) and body[index + 1] == quoted:
                    index += 1
                else:
                    quoted = None
        elif char in "'\"`":
            quoted = char
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            parts.append(body[start:index].strip())
            start = index + 1
        index += 1
    parts.append(body[start:].strip())
    if depth or quoted:
        raise ValueError("unbalanced DDL columns")
    return parts


CREATE_RE = re.compile(
    r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`\"]?(\w+)[`\"]?\s*\(", re.I)


def extract_table_bodies(text):
    """按平衡括号扫描提取每张 CREATE TABLE 的列定义体。

    非贪婪正则会把 VARCHAR(20) COMMENT 'x' 的 `) COMMENT` 误判为表结束；
    这里从开括号起做深度计数（尊重引号），找到真正的配对闭括号。
    括号不平衡的尾巴返回 None，由调用方记台账。
    """
    pos = 0
    while True:
        m = CREATE_RE.search(text, pos)
        if not m:
            return
        name = m.group(1)
        index = m.end()
        start = index
        depth, quoted = 1, None
        truncated = False
        while index < len(text):
            char = text[index]
            if quoted:
                if char == quoted:
                    if index + 1 < len(text) and text[index + 1] == quoted:
                        index += 1
                    else:
                        quoted = None
            elif char in "'\"`":
                quoted = char
            elif char == ";" and re.match(r"\s*(?:CREATE\b|$)", text[index + 1:], re.I | re.S):
                # 括号未闭合却到了语句结束符且后随新表/文件尾：DDL 截断，记台账并在此重新同步
                truncated = depth > 0
                break
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    yield name, text[start:index]
                    break
            index += 1
        else:
            yield name, None
            return
        if truncated:
            yield name, None
        pos = index + 1


def parse_sql(text, source_file):
    tables, failures = [], []
    # Protect SQL literals before stripping comments.
    text = re.sub(r"'(?:''|[^'])*'|\"(?:\"\"|[^\"])*\"|--[^\n]*|\#[^\n]*|/\*.*?\*/",
                  lambda x: x.group() if x.group().startswith(("'", '"')) else " ", text, flags=re.S)
    # 去掉 -- 与 # 行注释，但保留 COMMENT 'x' 内联注释
    for name, body in extract_table_bodies(text):
        if body is None:
            failures.append({"table": name, "source_file": source_file,
                             "reason": "括号不平衡，疑似 DDL 截断"})
            continue
        try:
            raw_columns = split_columns(body)
        except ValueError as exc:
            failures.append({"table": name, "source_file": source_file,
                             "reason": f"列定义解析失败：{exc}"})
            continue
        cols, pks = [], []
        for raw in raw_columns:
            line = raw.strip().rstrip(",")
            if not line:
                continue
            if re.match(r"(?:PRIMARY\s+KEY|UNIQUE|KEY|INDEX|CONSTRAINT|FOREIGN\s+KEY|CHECK)\b", line, re.I):
                pk = re.search(r"PRIMARY\s+KEY\s*\(([^)]+)\)", line, re.I)
                if pk:
                    pks += [x.strip().strip('`"') for x in pk.group(1).split(",")]
                continue
            cm = COL_RE.match(line)
            if not cm:
                tk = re.match(r"(?:PRIMARY\s+KEY|UNIQUE|KEY|INDEX|CONSTRAINT)", line, re.I)
                if tk and "PRIMARY" in line.upper():
                    pks += re.findall(r"`(\w+)`", line)
                continue
            cname, ctype, rest = cm.group(1), cm.group(2).upper(), cm.group(3)
            is_pk = bool(PK_INLINE.search(rest))
            if is_pk:
                pks.append(cname)
            comment = ""
            cmm = COMMENT_RE.search(rest)
            if cmm:
                comment = cmm.group(1)
            cols.append({"name": cname, "type": ctype, "pk": is_pk,
                         "is_time": is_time_col(cname, ctype),
                         "comment": comment})
        for column in cols:
            column["pk"] = column["name"] in pks
        tables.append({"name": name, "source_file": source_file,
                       "column_count": len(cols), "pk_guess": pks,
                       "time_cols": [c["name"] for c in cols if c["is_time"]],
                       "columns": cols})
    return tables, failures


def main():
    ap = argparse.ArgumentParser(description="DDL → 源表盘点清单")
    ap.add_argument("--ddl", action="append", default=[])
    ap.add_argument("--ddl-dir", default=None)
    ap.add_argument("--out", required=True, help="输出目录（inventory/）")
    ap.add_argument("--model-out", help="可选：生成部分 semantic.yaml 草案，不猜 grain/业务关系/口径")
    args = ap.parse_args()

    files = list(args.ddl)
    if args.ddl_dir:
        for root, _, fs in os.walk(args.ddl_dir):
            files += [os.path.join(root, f) for f in fs if f.lower().endswith(".sql")]
    if not files:
        print("错误：需要 --ddl 或 --ddl-dir", file=sys.stderr)
        return 2

    all_tables, all_failures = [], []
    for fp in sorted(files):
        with open(fp, encoding="utf-8-sig") as f:
            tables, failures = parse_sql(f.read(), os.path.basename(fp))
        all_tables += tables
        all_failures += failures

    if not all_tables:
        print("错误：未解析到任何 CREATE TABLE", file=sys.stderr)
        return 2
    for fail in all_failures:
        print(f"警告：跳过表 {fail['table']}（{fail['source_file']}）：{fail['reason']}",
              file=sys.stderr)

    prefix_counter = Counter(re.match(r"[a-zA-Z]+_", t["name"]).group(0)
                             if re.match(r"[a-zA-Z]+_", t["name"]) else "(无前缀)"
                             for t in all_tables)
    os.makedirs(args.out, exist_ok=True)
    tables_yaml = [{"name": t["name"], "source_file": t["source_file"],
                    "column_count": t["column_count"], "pk_guess": t["pk_guess"],
                    "time_cols": t["time_cols"],
                    "prefix": re.match(r"[a-zA-Z]+_", t["name"]).group(0)
                    if re.match(r"[a-zA-Z]+_", t["name"]) else "(无前缀)"}
                   for t in all_tables]
    columns_yaml = [{"table": t["name"], **{k: c[k] for k in ("name", "type", "pk", "is_time", "comment")}}
                    for t in all_tables for c in t["columns"]]

    with open(os.path.join(args.out, "tables.yaml"), "w", encoding="utf-8") as f:
        yaml.safe_dump({"table_count": len(all_tables),
                        "prefix_clusters": dict(prefix_counter.most_common()),
                        "parse_failures": all_failures,
                        "tables": tables_yaml}, f, allow_unicode=True, sort_keys=False)
    with open(os.path.join(args.out, "columns.yaml"), "w", encoding="utf-8") as f:
        yaml.safe_dump(columns_yaml, f, allow_unicode=True, sort_keys=False)

    if args.model_out:
        from _contract import write
        if os.path.exists(args.model_out):
            print("错误：model-out 已存在，拒绝覆盖", file=sys.stderr)
            return 2
        write(args.model_out, {"version": "draft-1", "datasets": [
            {"name": t["name"], "source": t["name"], "primary_key": t["pk_guess"],
             "fields": [{"name": c["name"], "type": c["type"],
                         "role": "pk" if c["pk"] else ("time" if c["is_time"] else "attr"),
                         "cn": c["comment"]} for c in t["columns"]]} for t in all_tables],
            "metrics": [], "concepts": [], "relationships": []})
    print(f"解析 {len(files)} 个文件 → {len(all_tables)} 张表 / {len(columns_yaml)} 个字段")
    print("命名前缀聚类：", dict(prefix_counter.most_common()))
    print(f"输出：{args.out}/tables.yaml, columns.yaml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
