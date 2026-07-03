#!/usr/bin/env python3
"""dbq SQL 安全层 —— 纯分析函数（无数据库访问）。"""

from __future__ import annotations

import csv
import fnmatch
import json
import re
import sys
from pathlib import Path

from db_config import _config_file_for, _load_any_config, ASSETS_DIR

# ── 常量 ─────────────────────────────────────────────────────

DEFAULT_LIMIT = 100
LARGE_TABLE_THRESHOLD = 50000


# ── 格式化输出 ──────────────────────────────────────────────

def format_output(columns, rows, fmt="table", show_row_count=True):
    if fmt == "json":
        result = [dict(zip(columns, row)) for row in rows]
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif fmt == "csv":
        writer = csv.writer(sys.stdout)
        writer.writerow(columns)
        writer.writerows(rows)
    else:
        if not columns:
            print("(查询无返回列)")
            return
        col_widths = [len(c) for c in columns]
        for row in rows:
            for i, val in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(val)) if val is not None else 4)
        header = " | ".join(c.ljust(col_widths[i]) for i, c in enumerate(columns))
        sep = "-+-".join("-" * col_widths[i] for i in range(len(columns)))
        print(header)
        print(sep)
        for row in rows:
            line = " | ".join(
                (str(v) if v is not None else "NULL").ljust(col_widths[i])
                for i, v in enumerate(row)
            )
            print(line)
        if show_row_count:
            print(f"\n({len(rows)} 行)")


# ── SQL 分析与保护 ──────────────────────────────────────────


def _has_limit(sql: str) -> bool:
    cleaned = re.sub(r";\s*$", "", sql.strip())
    return bool(re.search(r"\bLIMIT\s+\d+\s*$", cleaned, re.IGNORECASE))


def _inject_limit(sql: str, limit: int, db_type: str = "mysql") -> str:
    """给 SQL 注入 LIMIT。支持 SELECT / DELETE / UPDATE（INSERT 不适用）。
    PostgreSQL 不支持 DELETE LIMIT，会用 CTE 子查询替代。
    """
    cleaned = re.sub(r";\s*$", "", sql.strip())
    upper = cleaned.upper()

    if upper.startswith("DELETE") and db_type in ("postgresql", "postgres"):
        m = re.match(
            r"DELETE\s+FROM\s+(\w+)\s+(WHERE\s+.+)", cleaned,
            re.IGNORECASE,
        )
        if m:
            table = m.group(1)
            where = m.group(2)
            return (
                f"DELETE FROM {table} "
                f"WHERE ctid IN (SELECT ctid FROM {table} {where} LIMIT {limit})"
            )

    return f"{cleaned} LIMIT {limit}"


def _format_number(n: int) -> str:
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


# ── SQL 分类 ────────────────────────────────────────────────

# 操作分级:
#   READ   — SELECT / SHOW / DESCRIBE / EXPLAIN（始终允许）
#   DML    — INSERT / UPDATE / DELETE / REPLACE（需配置 readonly: false）
#   DDL    — ALTER / CREATE / DROP / TRUNCATE / RENAME（需配置 allow_ddl: true）
#   BLOCKED— CALL / EXECUTE / PREPARE / GRANT / REVOKE / LOCK（始终拒绝）

_READ_PREFIXES = ("SELECT", "SHOW", "DESCRIBE", "EXPLAIN", "DESC ")
_DML_PREFIXES = ("INSERT", "UPDATE", "DELETE", "REPLACE")
_DDL_PREFIXES = ("ALTER", "CREATE", "DROP", "TRUNCATE", "RENAME")
_BLOCKED_PREFIXES = ("CALL", "EXECUTE", "EXEC", "PREPARE", "GRANT",
                     "REVOKE", "LOCK", "UNLOCK", "FLUSH", "KILL",
                     "RESET", "SET ", "HANDLER", "LOAD ")


def _sql_type(stripped_sql: str) -> str:
    """返回 SQL 操作级别: READ / DML / DDL / BLOCKED"""
    s = stripped_sql.upper()
    for p in _BLOCKED_PREFIXES:
        if s.startswith(p):
            return "BLOCKED"
    for p in _DDL_PREFIXES:
        if s.startswith(p):
            return "DDL"
    for p in _DML_PREFIXES:
        if s.startswith(p):
            return "DML"
    for p in _READ_PREFIXES:
        if s.startswith(p):
            return "READ"
    return "BLOCKED"


def _strip_sql_comments(sql: str) -> str:
    """去掉 SQL 前缀的注释，返回大写开头的纯净 SQL"""
    stripped = sql.strip().upper()
    while stripped.startswith("--") or stripped.startswith("/*"):
        if stripped.startswith("--"):
            nl = stripped.find("\n")
            stripped = stripped[nl + 1:].strip() if nl != -1 else ""
        elif stripped.startswith("/*"):
            end = stripped.find("*/")
            stripped = stripped[end + 2:].strip() if end != -1 else ""
        else:
            break
    return stripped


def _split_sql_statements(sql: str) -> list:
    """按分号拆分多条 SQL 语句。返回 [(序号, 语句), ...]。"""
    parts = sql.split(";")
    result = []
    seq = 0
    for p in parts:
        s = p.strip()
        if s:
            seq += 1
            result.append((seq, s))
    return result


def _resolve_write_permission(db_alias: str, env: str,
                              config_override: str | None = None) -> tuple:
    """解析写权限。返回 (allow_dml: bool, allow_ddl: bool)。

    优先级: 连接级 > 环境级 > 全局默认(禁用)
    """
    if config_override:
        path = Path(config_override)
        if not path.is_absolute():
            path = ASSETS_DIR / path
    else:
        path = _config_file_for(env)

    settings: dict = {}
    conn: dict = {}
    try:
        if path.exists():
            raw = _load_any_config(path)
            settings = raw.get("settings", {})
            if isinstance(settings, dict):
                pass
            else:
                settings = {}
            connections = raw.get("connections", {})
            conn = connections.get(db_alias, {})
            if not isinstance(conn, dict):
                conn = {}
    except (FileNotFoundError, ImportError, RuntimeError, OSError):
        pass

    global_readonly: bool | None = settings.get("readonly_mode") if isinstance(settings, dict) else None
    global_allow_ddl: bool = settings.get("allow_ddl", False) if isinstance(settings, dict) else False

    conn_readonly: bool | None = conn.get("readonly") if isinstance(conn, dict) else None
    conn_allow_ddl: bool | None = conn.get("allow_ddl") if isinstance(conn, dict) else None

    if conn_readonly is not None:
        readonly = conn_readonly
    elif global_readonly is not None:
        readonly = global_readonly
    else:
        readonly = True

    if conn_allow_ddl is not None:
        allow_ddl = conn_allow_ddl
    elif global_allow_ddl is not None:
        allow_ddl = global_allow_ddl
    else:
        allow_ddl = False

    return (not readonly), bool(allow_ddl)


def _check_where_clause(sql: str, op_type: str):
    """检查 DELETE/UPDATE 是否有 WHERE 子句。无 WHERE 时拒绝。"""
    if op_type != "DML":
        return
    upper = sql.upper()
    if upper.startswith("DELETE") or upper.startswith("UPDATE"):
        if " WHERE " not in upper:
            raise ValueError(
                f"拒绝无 WHERE 的 {upper.split()[0]} 操作，这会修改整表数据。"
                f"\n如确认需要全表操作，请添加 WHERE 1=1。"
            )


# ── 表名通配符匹配 ──────────────────────────────────────────

def _filter_by_pattern(tables: list, pattern: str) -> list:
    """根据通配符模式过滤表名列表（纯函数，不访问数据库）。
    返回 list 或 None。
    """
    if pattern.upper() == "ALL":
        return tables
    if "*" in pattern or "?" in pattern:
        return [t for t in tables if fnmatch.fnmatch(t, pattern)]
    return None
