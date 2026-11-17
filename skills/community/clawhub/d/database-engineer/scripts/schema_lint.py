#!/usr/bin/env python3
"""schema_lint.py — SQL DDL 反模式检查器（零依赖）

解析 CREATE TABLE 语句，检出常见的 Schema 设计反模式。
支持 MySQL 与 PostgreSQL 方言的常见写法。

用法:
    python3 schema_lint.py schema.sql
    python3 schema_lint.py schema.sql --dialect mysql
    python3 schema_lint.py schema.sql --json
    cat schema.sql | python3 schema_lint.py -

退出码:
    0 = 无 error 级问题
    1 = 存在 error 级问题
    2 = 用法错误
"""
from __future__ import annotations

import argparse
import json
import re
import sys

# ---------------------------------------------------------------- 解析

# 顶层逗号切分（忽略括号内的逗号，如 DECIMAL(10,2)）
def split_top_level(text: str) -> list[str]:
    parts, depth, buf = [], 0, []
    for ch in text:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if "".join(buf).strip():
        parts.append("".join(buf))
    return [p.strip() for p in parts if p.strip()]


def strip_comments(sql: str) -> str:
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.S)
    sql = re.sub(r"--[^\n]*", " ", sql)
    sql = re.sub(r"(?m)^\s*#[^\n]*", " ", sql)
    return sql


CREATE_RE = re.compile(
    r"CREATE\s+(?:TEMPORARY\s+|UNLOGGED\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?"
    r"([`\"\[]?[\w.]+[`\"\]]?)\s*\(",
    re.I,
)


def find_tables(sql: str) -> list[tuple[str, str, str]]:
    """返回 [(表名, 列定义体, 尾部选项)]"""
    out = []
    for m in CREATE_RE.finditer(sql):
        name = m.group(1).strip('`"[]')
        start = m.end()  # 紧跟在 '(' 之后
        depth, i = 1, start
        while i < len(sql) and depth > 0:
            if sql[i] == "(":
                depth += 1
            elif sql[i] == ")":
                depth -= 1
            i += 1
        body = sql[start : i - 1]
        tail_end = sql.find(";", i)
        tail = sql[i : tail_end if tail_end != -1 else len(sql)]
        out.append((name, body, tail))
    return out


CONSTRAINT_KW = (
    "PRIMARY KEY", "FOREIGN KEY", "UNIQUE", "KEY ", "INDEX ",
    "CONSTRAINT", "CHECK", "EXCLUDE", "FULLTEXT", "SPATIAL",
)


def is_constraint(line: str) -> bool:
    u = line.upper().lstrip()
    return any(u.startswith(k) for k in CONSTRAINT_KW)


COL_RE = re.compile(r"^\s*[`\"\[]?(\w+)[`\"\]]?\s+([A-Za-z][\w ]*(?:\([^)]*\))?)")


def parse_table(name: str, body: str, tail: str) -> dict:
    cols, constraints = [], []
    for line in split_top_level(body):
        if is_constraint(line):
            constraints.append(line)
            continue
        m = COL_RE.match(line)
        if not m:
            continue
        cols.append(
            {
                "name": m.group(1),
                "type": m.group(2).strip().upper(),
                "raw": line,
                "raw_upper": line.upper(),
            }
        )
    return {"name": name, "cols": cols, "constraints": constraints,
            "tail": tail.upper(), "body_upper": body.upper()}


# ---------------------------------------------------------------- 规则

MONEY_HINT = re.compile(r"(amount|price|cost|balance|total|fee|salary|money|pay)", re.I)
FK_HINT = re.compile(r"^(\w+)_id$", re.I)


def lint_table(t: dict, dialect: str) -> list[dict]:
    issues: list[dict] = []

    def add(level, code, msg, col=None):
        issues.append({"table": t["name"], "column": col, "level": level,
                       "code": code, "message": msg})

    cols = t["cols"]
    all_constraints = " ".join(t["constraints"]).upper()
    col_names = {c["name"].lower() for c in cols}

    # S001 无主键
    has_pk = "PRIMARY KEY" in all_constraints or any(
        "PRIMARY KEY" in c["raw_upper"] for c in cols
    )
    if not has_pk:
        add("error", "S001", "表没有主键：复制、在线 DDL 工具(gh-ost/pt-osc)、"
                             "逻辑复制均依赖主键")

    # S002 money 用浮点
    for c in cols:
        if MONEY_HINT.search(c["name"]) and re.search(r"\b(FLOAT|DOUBLE|REAL)\b", c["type"]):
            add("error", "S002",
                f"金额类列使用浮点类型 {c['type']}，会有精度误差；应用 DECIMAL/NUMERIC",
                c["name"])

    # S003 MySQL utf8 假 UTF-8
    if re.search(r"CHARSET\s*=\s*utf8\b(?!mb4)", t["tail"], re.I) or re.search(
        r"CHARACTER\s+SET\s+utf8\b(?!mb4)", t["body_upper"] + t["tail"], re.I
    ):
        add("error", "S003", "使用 utf8（3 字节）字符集，无法存储 emoji 等 4 字节字符；"
                             "应改为 utf8mb4")

    # S004 外键列疑似缺索引
    indexed = set()
    for c in t["constraints"]:
        for m in re.finditer(r"\(([^)]*)\)", c):
            first = m.group(1).split(",")[0].strip().strip('`"[] ')
            if first:
                indexed.add(first.lower())
    for c in cols:
        if "PRIMARY KEY" in c["raw_upper"] or "UNIQUE" in c["raw_upper"]:
            indexed.add(c["name"].lower())
    for c in cols:
        if FK_HINT.match(c["name"]) and c["name"].lower() not in indexed:
            lvl = "error" if dialect == "postgres" else "warning"
            add(lvl, "S004",
                f"疑似外键列 {c['name']} 没有索引"
                + ("（PostgreSQL 不会自动建，父表删除会全表扫描）"
                   if dialect == "postgres" else "（请确认已被联合索引覆盖）"),
                c["name"])

    # S005 VARCHAR(255) 惯性默认值
    v255 = [c["name"] for c in cols if re.search(r"VARCHAR\s*\(\s*255\s*\)", c["type"])]
    if len(v255) >= 3:
        add("warning", "S005",
            f"{len(v255)} 个列使用 VARCHAR(255)（{', '.join(v255[:5])}…）："
            "多半是惯性默认值而非业务约束，应按真实长度收紧")

    # S006 缺时间戳审计列
    if not ({"created_at", "create_time", "created", "ctime", "inserted_at"} & col_names):
        add("warning", "S006", "缺少 created_at 类时间戳列，问题排查与数据归档会很困难")

    # S007 TIMESTAMP 2038 问题（MySQL）
    for c in cols:
        if re.match(r"^TIMESTAMP\b", c["type"]) and dialect != "postgres":
            add("warning", "S007",
                f"{c['name']} 使用 TIMESTAMP，MySQL 上限为 2038-01-19；"
                "存未来日期请用 DATETIME", c["name"])

    # S008 TEXT/BLOB 过多
    big = [c["name"] for c in cols
           if re.search(r"\b(TEXT|LONGTEXT|MEDIUMTEXT|BLOB|LONGBLOB|JSON|JSONB)\b", c["type"])]
    if len(big) >= 4:
        add("warning", "S008",
            f"{len(big)} 个大对象列（{', '.join(big[:5])}…）：考虑垂直拆表，"
            "避免主表行过宽拖慢全表扫描")

    # S009 列数过多
    if len(cols) > 40:
        add("warning", "S009", f"表有 {len(cols)} 列，超过 40，通常意味着职责不单一")

    # S010 ENUM（MySQL）
    for c in cols:
        if re.match(r"^ENUM\b", c["type"]):
            add("warning", "S010",
                f"{c['name']} 使用 ENUM：增删枚举值需要 ALTER TABLE，"
                "建议改用 VARCHAR + CHECK 或关联表", c["name"])

    # S011 CHAR 存可变长文本
    for c in cols:
        m = re.match(r"^CHAR\s*\(\s*(\d+)\s*\)", c["type"])
        if m and int(m.group(1)) > 8:
            add("info", "S011",
                f"{c['name']} 使用 CHAR({m.group(1)})，定长会补空格；"
                "非定长内容应用 VARCHAR", c["name"])

    # S012 无符号自增主键容量
    for c in cols:
        if "AUTO_INCREMENT" in c["raw_upper"] and re.search(r"\bINT\b", c["type"]) \
                and not re.search(r"\bBIGINT\b", c["type"]):
            add("warning", "S012",
                f"自增主键 {c['name']} 为 INT（上限约 21 亿）；"
                "高写入表建议 BIGINT，事后改类型需重建全表", c["name"])

    # S013 可空列比例过高
    nullable = [c for c in cols
                if "NOT NULL" not in c["raw_upper"] and "PRIMARY KEY" not in c["raw_upper"]]
    if cols and len(nullable) / len(cols) > 0.8 and len(cols) >= 5:
        add("info", "S013",
            f"{len(nullable)}/{len(cols)} 列可空：NULL 语义易出错（如 NOT IN 的三值逻辑），"
            "能给默认值就加 NOT NULL")

    return issues


# ---------------------------------------------------------------- 主流程

LEVEL_ORDER = {"error": 0, "warning": 1, "info": 2}
ICON = {"error": "✗", "warning": "!", "info": "·"}


def main() -> int:
    ap = argparse.ArgumentParser(
        description="SQL DDL 反模式检查器（零依赖）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n  python3 schema_lint.py schema.sql --dialect postgres\n"
               "  cat schema.sql | python3 schema_lint.py -",
    )
    ap.add_argument("file", help="SQL 文件路径，用 - 表示从 stdin 读取")
    ap.add_argument("--dialect", choices=["mysql", "postgres", "auto"], default="auto",
                    help="SQL 方言（默认 auto 自动探测）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--strict", action="store_true",
                    help="warning 也视为失败（退出码 1）")
    args = ap.parse_args()

    try:
        raw = sys.stdin.read() if args.file == "-" else open(
            args.file, encoding="utf-8").read()
    except OSError as e:
        print(f"无法读取文件: {e}", file=sys.stderr)
        return 2

    sql = strip_comments(raw)

    dialect = args.dialect
    if dialect == "auto":
        if re.search(r"ENGINE\s*=|AUTO_INCREMENT|`", sql, re.I):
            dialect = "mysql"
        elif re.search(r"SERIAL|BIGSERIAL|JSONB|::", sql, re.I):
            dialect = "postgres"
        else:
            dialect = "mysql"

    tables = find_tables(sql)
    if not tables:
        print("未找到 CREATE TABLE 语句", file=sys.stderr)
        return 2

    all_issues: list[dict] = []
    for name, body, tail in tables:
        all_issues.extend(lint_table(parse_table(name, body, tail), dialect))

    order = {name: n for n, (name, _, _) in enumerate(tables)}
    all_issues.sort(key=lambda i: (order.get(i["table"], 0),
                                   LEVEL_ORDER[i["level"]], i["code"]))
    counts = {lv: sum(1 for i in all_issues if i["level"] == lv)
              for lv in ("error", "warning", "info")}

    if args.json:
        print(json.dumps({"dialect": dialect, "tables": len(tables),
                          "counts": counts, "issues": all_issues},
                         ensure_ascii=False, indent=2))
    else:
        print(f"\nschema_lint  方言={dialect}  表数={len(tables)}\n")
        cur = None
        for i in all_issues:
            if i["table"] != cur:
                cur = i["table"]
                print(f"  [{cur}]")
            col = f" {i['column']}:" if i["column"] else ""
            print(f"    {ICON[i['level']]} {i['code']}{col} {i['message']}")
        if not all_issues:
            print("  未发现问题")
        print(f"\n汇总: error={counts['error']}  "
              f"warning={counts['warning']}  info={counts['info']}\n")

    if counts["error"] or (args.strict and counts["warning"]):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
