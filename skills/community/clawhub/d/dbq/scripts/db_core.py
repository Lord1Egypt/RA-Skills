#!/usr/bin/env python3
"""dbq 数据库引擎 —— 驱动 / 连接 / 查询执行 / 表操作 / 日志。"""

from __future__ import annotations

import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

from db_config import (
    get_connection, load_env_config, _config_file_for, _load_any_config,
    ASSETS_DIR, SKILL_DIR,
)
import db_config  # 用于 LOG_DIR 等可被 monkey-patch 的常量
from db_guard import (
    _has_limit, _inject_limit, _format_number,
    _sql_type, _strip_sql_comments, _check_where_clause,
    _resolve_write_permission, format_output,
    DEFAULT_LIMIT, LARGE_TABLE_THRESHOLD,
)


# ── 数据库驱动 ──────────────────────────────────────────────

def _get_mysql_connection(conn_info: dict, timeout: int | None = None):
    try:
        import pymysql
    except ImportError:
        raise ImportError("需要 pymysql。请安装: pip install pymysql")
    kwargs = dict(
        host=conn_info["host"],
        port=conn_info.get("port", 3306),
        user=conn_info["user"],
        password=conn_info.get("password", ""),
        database=conn_info["database"],
        charset=conn_info.get("charset", "utf8mb4"),
        connect_timeout=conn_info.get("connect_timeout", 10),
        autocommit=True,
    )
    if timeout:
        kwargs["read_timeout"] = timeout
    return pymysql.connect(**kwargs)


def _get_pg_connection(conn_info: dict, timeout: int | None = None):
    try:
        import psycopg2
    except ImportError:
        raise ImportError("需要 psycopg2。请安装: pip install psycopg2-binary")
    kwargs = dict(
        host=conn_info["host"],
        port=conn_info.get("port", 5432),
        user=conn_info["user"],
        password=conn_info.get("password", ""),
        dbname=conn_info["database"],
        connect_timeout=conn_info.get("connect_timeout", 10),
    )
    conn = psycopg2.connect(**kwargs)
    conn.autocommit = True
    if timeout:
        kwargs["options"] = f"-c statement_timeout={timeout * 1000}"
    return psycopg2.connect(**kwargs)


def _get_sqlite_connection(conn_info: dict, timeout: int | None = None):
    """SQLite 驱动（使用标准库 sqlite3，零额外依赖）。"""
    import sqlite3
    path = conn_info.get("path", ":memory:")
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.isolation_level = None
    if timeout:
        conn.execute(f"PRAGMA busy_timeout = {timeout * 1000}")
    return conn


_DRIVER_MAP = {
    "mysql": _get_mysql_connection,
    "mariadb": _get_mysql_connection,
    "postgresql": _get_pg_connection,
    "postgres": _get_pg_connection,
    "sqlite": _get_sqlite_connection,
    "sqlite3": _get_sqlite_connection,
}


def _open_raw_connection(db_alias: str, env: str,
                         config_override: str | None = None,
                         timeout: int | None = None):
    """打开一条原始数据库连接，返回 (conn, db_type)。调用方负责关闭。"""
    conn_info = get_connection(db_alias, env, config_override)
    db_type = conn_info["type"].lower()
    if db_type not in _DRIVER_MAP:
        raise ValueError(
            f"不支持的数据库类型: {db_type}\n"
            f"支持: {', '.join(_DRIVER_MAP)}"
        )
    return _DRIVER_MAP[db_type](conn_info, timeout=timeout), db_type


# ── 查询日志 ────────────────────────────────────────────────

def _log_query(db_alias: str, env: str, sql: str, row_count: int,
               elapsed: float, status: str = "OK", op_type: str = ""):
    """将查询记录写入日志文件。日志位于 dbq/logs/YYYY-MM-DD.log。"""
    try:
        if not db_config.LOG_DIR.exists():
            db_config.LOG_DIR.mkdir(parents=True, exist_ok=True)
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = db_config.LOG_DIR / f"{today}.log"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tag = f" {op_type}" if op_type else ""
        line = (
            f"[{timestamp}] {env}:{db_alias} |{tag} "
            f"{sql} | "
            f"{row_count} rows | "
            f"{elapsed:.3f}s | "
            f"{status}\n"
        )
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass


# ── 查询执行 ────────────────────────────────────────────────

def execute_query(db_alias: str, sql: str, env: str,
                  config_override: str | None = None,
                  _conn=None, _timeout: int | None = None,
                  _op_type: str = ""):
    """执行 SQL。返回:
      - 如果是 SELECT: (columns, rows)
      - 如果是 DML/DDL: ([], affected_rows)
    """
    own_conn = False
    if _conn is not None:
        conn = _conn
    else:
        if _timeout is not None:
            conn, _ = _open_raw_connection(db_alias, env, config_override, timeout=_timeout)
        else:
            conn, _ = _open_raw_connection(db_alias, env, config_override)
        own_conn = True
    try:
        cursor = conn.cursor()
        start = time.time()
        cursor.execute(sql)
        elapsed = time.time() - start

        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            _log_query(db_alias, env, sql.strip(), len(rows), elapsed,
                       op_type=_op_type)
            return columns, rows
        else:
            affected = cursor.rowcount
            _log_query(db_alias, env, sql.strip(), affected, elapsed,
                       op_type=_op_type or "WRITE")
            return [], affected
    except Exception:
        elapsed = time.time() - start
        _log_query(db_alias, env, sql.strip(), 0, elapsed, "ERROR", _op_type)
        raise
    finally:
        if own_conn:
            conn.close()


def list_tables(db_alias: str, env: str, config_override: str | None = None,
                _conn=None):
    conn_info = get_connection(db_alias, env, config_override)
    db_type = conn_info["type"].lower()
    if db_type in ("mysql", "mariadb"):
        sql = "SHOW TABLES"
    elif db_type in ("postgresql", "postgres"):
        sql = (
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema = 'public' ORDER BY table_name"
        )
    elif db_type in ("sqlite", "sqlite3"):
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    else:
        raise ValueError(f"不支持的表列表查询: {db_type}")
    columns, rows = execute_query(db_alias, sql, env, config_override, _conn=_conn)
    return [r[0] for r in rows]


def list_tables_with_info(db_alias: str, env: str,
                          config_override: str | None = None,
                          _conn=None) -> tuple:
    """获取表列表（含 COMMENT + 预估行数）。返回: (columns, rows)"""
    conn_info = get_connection(db_alias, env, config_override)
    db_type = conn_info["type"].lower()

    if db_type in ("mysql", "mariadb"):
        sql = (
            "SELECT TABLE_NAME, TABLE_ROWS, TABLE_COMMENT "
            "FROM information_schema.TABLES "
            "WHERE TABLE_SCHEMA = DATABASE() "
            "ORDER BY TABLE_NAME"
        )
    elif db_type in ("postgresql", "postgres"):
        sql = (
            "SELECT "
            "  t.table_name, "
            "  COALESCE(c.reltuples::bigint, 0), "
            "  pg_catalog.obj_description(c.oid) "
            "FROM information_schema.tables t "
            "LEFT JOIN pg_class c ON c.relname = t.table_name "
            "WHERE t.table_schema = 'public' "
            "ORDER BY t.table_name"
        )
    elif db_type in ("sqlite", "sqlite3"):
        sql = (
            "SELECT name, 0, '' FROM sqlite_master "
            "WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
    else:
        raise ValueError(f"不支持的数据库类型: {db_type}")

    columns, rows = execute_query(db_alias, sql, env, config_override, _conn=_conn)
    columns = ["Table", "Rows", "Comment"]
    return columns, rows


def show_create_table(db_alias: str, table_name: str, env: str,
                     config_override: str | None = None,
                     _conn=None) -> str:
    """获取表的 CREATE TABLE DDL 语句。"""
    conn_info = get_connection(db_alias, env, config_override)
    db_type = conn_info["type"].lower()

    if db_type in ("mysql", "mariadb"):
        sql = f"SHOW CREATE TABLE {table_name}"
        columns, rows = execute_query(db_alias, sql, env, config_override, _conn=_conn)
        if rows and len(rows[0]) >= 2:
            return rows[0][1]
        return f"-- 无法获取 {table_name} 的 DDL"

    elif db_type in ("postgresql", "postgres"):
        col_sql = (
            "SELECT "
            "  c.column_name, "
            "  c.data_type, "
            "  c.character_maximum_length, "
            "  c.is_nullable, "
            "  c.column_default, "
            "  pg_catalog.col_description(c.table_name::regclass, c.ordinal_position) AS comment "
            "FROM information_schema.columns c "
            f"WHERE c.table_name = '{table_name}' "
            "ORDER BY c.ordinal_position"
        )
        col_cols, col_rows = execute_query(db_alias, col_sql, env, config_override, _conn=_conn)

        idx_sql = (
            "SELECT indexname, indexdef FROM pg_indexes "
            f"WHERE tablename = '{table_name}' ORDER BY indexname"
        )
        _, idx_rows = execute_query(db_alias, idx_sql, env, config_override, _conn=_conn)

        lines = [f"CREATE TABLE {table_name} ("]
        for r in col_rows:
            name = r[0]
            dtype = r[1]
            maxlen = r[2]
            nullable = r[3]
            default = r[4]
            comment = r[5]

            if dtype in ("character varying", "character", "varchar") and maxlen:
                dtype = f"varchar({maxlen})"

            col_def = f"  {name} {dtype}"
            if nullable == "NO":
                col_def += " NOT NULL"
            if default:
                col_def += f" DEFAULT {default}"
            lines.append(col_def + ",")

        lines.append(");")
        ddl = "\n".join(lines)

        if idx_rows:
            ddl += "\n"
            for idx in idx_rows:
                ddl += f"\n{idx[1]};"

        return ddl

    elif db_type in ("sqlite", "sqlite3"):
        sql = "SELECT sql FROM sqlite_master WHERE type='table' AND name=?"
        params_sql = sql.replace("?", f"'{table_name}'")
        columns, rows = execute_query(db_alias, params_sql, env, config_override, _conn=_conn)
        if rows and rows[0][0]:
            return rows[0][0]
        return f"-- 无法获取 {table_name} 的 DDL（可能是虚拟表或系统表）"

    else:
        raise ValueError(f"不支持的表结构查询: {db_type}")


def describe_table(db_alias: str, table_name: str, env: str,
                  config_override: str | None = None,
                  _conn=None):
    """获取完整表结构 (列定义 + 注释)。"""
    conn_info = get_connection(db_alias, env, config_override)
    db_type = conn_info["type"].lower()
    if db_type in ("mysql", "mariadb"):
        sql = f"SHOW FULL COLUMNS FROM {table_name}"
        columns, rows = execute_query(db_alias, sql, env, config_override, _conn=_conn)
        skip = {"Collation", "Privileges"}
        idx_map = [i for i, c in enumerate(columns) if c not in skip]
        columns = [columns[i] for i in idx_map]
        rows = [tuple(r[i] for i in idx_map) for r in rows]
    elif db_type in ("postgresql", "postgres"):
        sql = (
            "SELECT "
            "  c.column_name AS Field, "
            "  c.data_type AS Type, "
            "  c.is_nullable AS Null, "
            "  c.column_default AS Default, "
            "  pg_catalog.col_description(c.table_name::regclass, c.ordinal_position) AS Comment "
            "FROM information_schema.columns c "
            f"WHERE c.table_name = '{table_name}' "
            "ORDER BY c.ordinal_position"
        )
        columns, rows = execute_query(db_alias, sql, env, config_override, _conn=_conn)
    elif db_type in ("sqlite", "sqlite3"):
        sql = f"PRAGMA table_info({table_name})"
        columns, rows = execute_query(db_alias, sql, env, config_override, _conn=_conn)
        columns = ["Field", "Type", "Null", "Default", "Key", "Extra", "Comment"]
        rows = [
            (r[1], r[2], "NO" if r[3] else "YES", r[4] or "",
             "PRI" if r[5] else "", "",
             "")
            for r in rows
        ]
    else:
        raise ValueError(f"不支持的表结构查询: {db_type}")
    return columns, rows


def get_table_comment(db_alias: str, table_name: str, env: str,
                      config_override: str | None = None,
                      _conn=None) -> str:
    """获取表 COMMENT 信息。"""
    try:
        conn_info = get_connection(db_alias, env, config_override)
        db_type = conn_info["type"].lower()
        if db_type in ("mysql", "mariadb"):
            sql = f"SHOW TABLE STATUS WHERE Name = '{table_name}'"
            columns, rows = execute_query(db_alias, sql, env, config_override, _conn=_conn)
            if rows and "Comment" in columns:
                idx = columns.index("Comment")
                comment = rows[0][idx]
                return comment if comment else ""
        elif db_type in ("postgresql", "postgres"):
            sql = (
                "SELECT obj_description(c.oid) "
                "FROM pg_class c "
                "JOIN pg_namespace n ON n.oid = c.relnamespace "
                f"WHERE c.relname = '{table_name}' AND n.nspname = 'public'"
            )
            _, rows = execute_query(db_alias, sql, env, config_override, _conn=_conn)
            if rows and rows[0][0]:
                return rows[0][0]
    except (FileNotFoundError, ImportError, RuntimeError, OSError):
        pass
    return ""


def describe_indexes(db_alias: str, table_name: str, env: str,
                     config_override: str | None = None,
                     _conn=None):
    """获取表索引信息。"""
    conn_info = get_connection(db_alias, env, config_override)
    db_type = conn_info["type"].lower()
    if db_type in ("mysql", "mariadb"):
        sql = f"SHOW INDEX FROM {table_name}"
        columns, rows = execute_query(db_alias, sql, env, config_override, _conn=_conn)
        keep = {"Non_unique", "Key_name", "Seq_in_index", "Column_name",
                "Null", "Index_type", "Comment"}
        idx_map = [i for i, c in enumerate(columns) if c in keep]
        columns = [columns[i] for i in idx_map]
        rows = [tuple(r[i] for i in idx_map) for r in rows]
        return columns, rows
    elif db_type in ("postgresql", "postgres"):
        sql = (
            "SELECT "
            "  indexname AS Key_name, "
            "  indexdef AS Index_def "
            "FROM pg_indexes "
            f"WHERE tablename = '{table_name}' "
            "ORDER BY indexname"
        )
    elif db_type in ("sqlite", "sqlite3"):
        sql = f"PRAGMA index_list({table_name})"
        columns, rows = execute_query(db_alias, sql, env, config_override, _conn=_conn)
        columns = ["Non_unique", "Key_name", "Column_name", "Index_type"]
        result_rows = []
        for r in rows:
            idx_name = r[1]
            is_unique = r[2]
            info_sql = f"PRAGMA index_info({idx_name})"
            _, info_rows = execute_query(db_alias, info_sql, env, config_override, _conn=_conn)
            for ir in info_rows:
                result_rows.append((0 if is_unique else 1, idx_name, ir[2], "btree"))
        return columns, result_rows
    else:
        raise ValueError(f"不支持的数据库类型: {db_type}")
    columns, rows = execute_query(db_alias, sql, env, config_override, _conn=_conn)
    return columns, rows


def list_connections(env: str | None = None,
                     config_override: str | None = None):
    """列出所有已配置的数据库别名。"""
    from db_config import DEFAULT_ENV
    all_envs = []

    if config_override:
        path = Path(config_override)
        if not path.is_absolute():
            path = ASSETS_DIR / path
        if path.exists():
            config = _load_any_config(path)
            conns = config.get("connections", {})
            if conns:
                all_envs.append((path.stem, conns))
    else:
        for f in sorted(ASSETS_DIR.glob("connections.*.yaml")):
            env_name = f.stem.replace("connections.", "")
            if env and env_name != env:
                continue
            try:
                config = _load_any_config(f)
                conns = config.get("connections", {})
                if conns:
                    all_envs.append((env_name, conns))
            except Exception:
                continue

    if not all_envs:
        print("(无已配置的数据库连接)")
        return

    header = f"{'环境':<10} {'别名':<22} {'类型':<12} {'主机':<20} {'端口':<8} {'数据库'}"
    print(f"默认环境: {DEFAULT_ENV}\n")
    print(header)
    print("-" * 82)
    for env_name, conns in all_envs:
        for alias, info in conns.items():
            db_type = info.get("type", "unknown")
            host = info.get("host", "-")
            port = str(info.get("port", "-"))
            db_name = info.get("database", "-")
            mark = " *" if env_name == DEFAULT_ENV else ""
            print(f"{env_name + mark:<10} {alias:<22} {db_type:<12} {host:<20} {port:<8} {db_name}")


# ── EXPLAIN / COUNT ──────────────────────────────────────────

def _get_explain_info(db_alias: str, sql: str, env: str,
                      config_override: str | None = None,
                      _conn=None):
    """运行 EXPLAIN，返回 (预估行数, 索引摘要字符串)。"""
    conn_info = get_connection(db_alias, env, config_override)
    db_type = conn_info["type"].lower()

    own_conn = False
    if _conn is not None:
        conn = _conn
    else:
        driver_fn = _DRIVER_MAP[db_type]
        conn = driver_fn(conn_info)
        own_conn = True

    t0 = time.time()
    try:
        cursor = conn.cursor()
        if db_type in ("mysql", "mariadb"):
            explain_sql = f"EXPLAIN {sql}"
            cursor.execute(explain_sql)
            rows = cursor.fetchall()
            elapsed = time.time() - t0
            _log_query(db_alias, env, explain_sql, len(rows), elapsed)
            if not rows:
                return None, ""
            cols = [desc[0].lower() for desc in cursor.description] if cursor.description else []

            try:
                row_idx = cols.index("rows")
                estimated = sum(int(r[row_idx] or 0) for r in rows)
            except (ValueError, IndexError):
                estimated = None

            parts = []
            try:
                t = rows[0][cols.index("type")]
                if t:
                    label = str(t)
                    if str(t).upper() == "ALL":
                        label = "ALL (全表扫描)"
                    parts.append(f"type={label}")
            except (ValueError, IndexError):
                pass
            try:
                k = rows[0][cols.index("key")]
                if k:
                    parts.append(f"key={k}")
                else:
                    parts.append("key=NULL")
            except (ValueError, IndexError):
                pass
            try:
                r = rows[0][cols.index("rows")]
                parts.append(f"rows={_format_number(int(r or 0))}")
            except (ValueError, IndexError):
                pass
            try:
                extra = str(rows[0][cols.index("extra")] or "")
                if "Using filesort" in extra:
                    parts.append("Using filesort")
                if "Using temporary" in extra:
                    parts.append("Using temporary")
            except (ValueError, IndexError):
                pass

            summary = " | ".join(parts)
            return estimated, summary

        elif db_type in ("postgresql", "postgres"):
            explain_sql = f"EXPLAIN (FORMAT JSON) {sql}"
            cursor.execute(explain_sql)
            result = cursor.fetchone()
            elapsed = time.time() - t0
            _log_query(db_alias, env, explain_sql, 1 if result else 0, elapsed)
            if result and result[0]:
                plan = result[0][0].get("Plan", {})
                estimated = int(plan.get("Plan Rows", 0))
                node_type = plan.get("Node Type", "")
                index_name = plan.get("Index Name", plan.get("Relation Name", ""))
                scan = plan.get("Index Cond", plan.get("Filter", ""))
                part_str = f"type={node_type}"
                if index_name:
                    part_str += f" | key={index_name}"
                if scan:
                    part_str += f" | cond={str(scan)[:40]}"
                return estimated, part_str

        elif db_type in ("sqlite", "sqlite3"):
            explain_sql = f"EXPLAIN QUERY PLAN {sql}"
            cursor.execute(explain_sql)
            rows = cursor.fetchall()
            elapsed = time.time() - t0
            _log_query(db_alias, env, explain_sql, len(rows), elapsed)
            if not rows:
                return None, ""
            details = [r[3] for r in rows if len(r) > 3 and r[3]]
            summary = " | ".join(details[:3])
            return None, summary

        elapsed = time.time() - t0
        _log_query(db_alias, env, sql, 0, elapsed, "EMPTY")
        return None, ""
    except Exception:
        elapsed = time.time() - t0
        _log_query(db_alias, env, f"EXPLAIN {sql}", 0, elapsed, "ERROR")
        return None, ""
    finally:
        if own_conn:
            conn.close()


def _get_estimated_rows(db_alias: str, sql: str, env: str,
                        config_override: str | None = None):
    """兼容旧接口，只返回预估行数。"""
    est, _summary = _get_explain_info(db_alias, sql, env, config_override)
    return est


def _execute_count(db_alias: str, sql: str, env: str,
                   config_override: str | None = None):
    count_sql = re.sub(
        r"\bORDER\s+BY\s+.+?(\bLIMIT\b|$)", "", sql,
        flags=re.IGNORECASE | re.DOTALL,
    )
    count_sql = re.sub(r"\bLIMIT\s+\d+", "", count_sql, flags=re.IGNORECASE)
    count_sql = re.sub(
        r"SELECT\s+.+?\s+FROM", "SELECT COUNT(*) FROM",
        count_sql, count=1,
        flags=re.IGNORECASE | re.DOTALL,
    )
    columns, rows = execute_query(db_alias, count_sql, env, config_override)
    if rows and len(rows) > 0:
        return int(rows[0][0])
    return 0


# ── 写操作确认 ──────────────────────────────────────────────

def _confirm_write(env: str, db_alias: str, conn_info: dict,
                   sql: str, op_type: str):
    """写操作确认提示。prod 环境强制确认，非交互式通过环境变量跳过。"""
    assume_yes = os.environ.get("DB_QUERY_ASSUME_YES", "").strip() in ("1", "yes", "true")

    label = "DDL" if op_type == "DDL" else "DML"
    host_info = conn_info.get("host", conn_info.get("path", "?"))
    database = conn_info.get("database", conn_info.get("path", "?"))

    msg = (
        f"\n⚠️  即将执行 {label} 操作:\n"
        f"    环境: {env}\n"
        f"    连接: {db_alias} ({host_info}/{database})\n"
        f"    SQL:  {sql[:200]}\n"
    )

    if env == "prod":
        if assume_yes:
            print(msg + "    确认: 已跳过 (DB_QUERY_ASSUME_YES=1)")
            return
        print(msg + "\n    [prod 环境] 输入 yes 确认执行: ", end="", flush=True)
        try:
            answer = sys.stdin.readline().strip()
        except (EOFError, KeyboardInterrupt):
            raise RuntimeError("已取消写操作")
        if answer.lower() != "yes":
            raise RuntimeError("已取消写操作")
    elif assume_yes:
        print(msg + "    确认: 已跳过 (DB_QUERY_ASSUME_YES=1)")
    else:
        print(msg + "    确认: 非 prod 环境，自动确认执行")


# ── SQL 校验 ─────────────────────────────────────────────────

def validate_sql(sql: str, db_alias: str | None = None, env: str | None = None,
                 config_override: str | None = None, dry_run: bool = False):
    """校验 SQL 操作级别，根据配置放行或拒绝。

    返回: (op_type: str)  — "READ" / "DML" / "DDL"
    抛出: ValueError 如果操作被拒绝
    """
    stripped = _strip_sql_comments(sql)
    op_type = _sql_type(stripped)

    if op_type == "BLOCKED":
        raise ValueError(
            f"拒绝执行此语句类型，收到: {sql[:50]}...\n"
            f"支持: SELECT/SHOW/DESCRIBE/EXPLAIN/INSERT/UPDATE/DELETE/REPLACE\n"
            f"受控: ALTER/CREATE/DROP/TRUNCATE (需 allow_ddl: true)"
        )

    if op_type == "READ":
        return op_type

    if db_alias is None or env is None:
        raise ValueError(
            f"{'DDL' if op_type == 'DDL' else 'DML'} 操作被拒绝：写操作未启用。"
            f"\n请在 YAML 中设置 readonly: false (DML) 或 allow_ddl: true (DDL)。"
        )

    allow_dml, allow_ddl = _resolve_write_permission(db_alias, env, config_override)

    if op_type == "DML" and not allow_dml:
        raise ValueError(
            f"DML 操作被拒绝: [{db_alias}] ({env}) 写操作未启用。"
            f"\n请在配置中设置 readonly: false"
        )

    if op_type == "DDL" and not allow_ddl:
        raise ValueError(
            f"DDL 操作被拒绝: [{db_alias}] ({env}) DDL 未启用。"
            f"\n请在配置中设置 allow_ddl: true"
        )

    return op_type


# ── 表名解析 ─────────────────────────────────────────────────

def _resolve_table_names(pattern: str, db_alias: str, env: str,
                         config_override: str | None = None,
                         _conn=None) -> list:
    """解析表名参数，支持 ALL / 通配符(*, ?) / 精确表名。"""
    from db_guard import _filter_by_pattern
    is_multi = pattern.upper() == "ALL" or "*" in pattern or "?" in pattern
    if is_multi:
        tables = list_tables(db_alias, env, config_override, _conn=_conn)
        result = _filter_by_pattern(tables, pattern)
        if not result:
            print(f"[WARN] 没有匹配 '{pattern}' 的表", file=sys.stderr)
        return result
    else:
        return [pattern]
