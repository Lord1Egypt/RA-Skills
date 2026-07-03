#!/usr/bin/env python3
"""dbq CLI 入口 —— 多环境 SQL 查询 / 写入工具 (MySQL / PostgreSQL / SQLite)。

用法:
    python query.py <db_alias> "<SQL>"                              # 默认 dev
    python query.py --env prod <db_alias> "<SQL>"                    # 切环境
    python query.py --config other.yaml <db_alias> "<SQL>"           # 自定义配置
    python query.py --list                                           # 扫描所有环境
    python query.py <db_alias> --show                                # 列出表
    python query.py <db_alias> --desc <TABLE>                    # 表结构
    python query.py <db_alias> --desc ALL                        # 全部表结构
    python query.py <db_alias> --desc "user_*"                   # 通配符匹配
    python query.py <db_alias> --ddl user_info                   # 建表 DDL
    python query.py <db_alias> --ping                                # 连接测试
    python query.py --keychain-set <alias> --env prod                # 存密码
"""

from __future__ import annotations

import argparse
import fnmatch
import getpass
import subprocess
import sys
import time

from db_config import (
    _handle_init_config, _keychain_service, _resolve_password,
    get_connection, DEFAULT_ENV, SKILL_DIR,
)
from db_guard import (
    format_output, _has_limit, _inject_limit, _format_number,
    _sql_type, _split_sql_statements, _check_where_clause,
    DEFAULT_LIMIT, LARGE_TABLE_THRESHOLD,
)
from db_core import (
    _open_raw_connection, execute_query, _log_query,
    list_tables_with_info, get_table_comment, describe_table,
    describe_indexes, show_create_table, list_connections,
    _get_explain_info, _get_estimated_rows, _execute_count,
    _confirm_write, validate_sql, _resolve_table_names,
)


# ── 结构化命令处理（--desc / --ddl 共用）─────────────────

def _handle_structure_cmd(args, mode: str):
    """处理 --desc 或 --ddl 命令。

    mode: "desc" 表格模式 / "ddl" DDL 模式
    """
    env = args.env or DEFAULT_ENV
    label = f"{args.db_alias} ({env})"
    target = args.desc if mode == "desc" else args.ddl

    pattern_multi = target.upper() == "ALL" or "*" in target or "?" in target
    shared_conn = None

    try:
        if pattern_multi:
            shared_conn, _ = _open_raw_connection(args.db_alias, env, args.config)
            tables = _resolve_table_names(target, args.db_alias, env, args.config,
                                          _conn=shared_conn)
        else:
            tables = [target]

        for i, t in enumerate(tables):
            if i > 0:
                print()

            tbl_comment = get_table_comment(args.db_alias, t, env, args.config,
                                            _conn=shared_conn)
            comment_str = f"  COMMENT: {tbl_comment}" if tbl_comment else ""
            print(f"━━━ {t}{comment_str} ━━━  {label}")

            if mode == "desc":
                print()
                cols, rows = describe_table(args.db_alias, t, env, args.config,
                                            _conn=shared_conn)
                print(f"── 列 ({len(rows)}) ──")
                format_output(cols, rows, args.format, show_row_count=False)

                print()
                print("── 索引 ──")
                icols, irows = describe_indexes(args.db_alias, t, env, args.config,
                                                _conn=shared_conn)
                if irows:
                    format_output(icols, irows, args.format, show_row_count=False)
                else:
                    print("  (无显式索引)")

            elif mode == "ddl":
                print()
                ddl = show_create_table(args.db_alias, t, env, args.config,
                                       _conn=shared_conn)
                print(ddl)

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if shared_conn:
            shared_conn.close()


def _handle_multi_query(args):
    """处理 --multi 多条 SELECT：一次连接，逐条执行。

    约束:
    - 只允许 READ 语句（SELECT/SHOW/DESCRIBE/EXPLAIN）
    - 不支持 --count / --dry-run
    """
    env = args.env or DEFAULT_ENV
    label = f"{args.db_alias} ({env})"

    if args.count:
        print("[ERROR] --multi 不支持 --count", file=sys.stderr)
        sys.exit(1)
    if args.dry_run:
        print("[ERROR] --multi 不支持 --dry-run", file=sys.stderr)
        sys.exit(1)

    statements = _split_sql_statements(args.sql)
    if not statements:
        print("[ERROR] 没有有效的 SQL 语句", file=sys.stderr)
        sys.exit(1)

    for seq, stmt in statements:
        op_type = _sql_type(stmt)
        if op_type != "READ":
            raise ValueError(
                f"--multi 仅支持查询 (SELECT/SHOW/DESCRIBE/EXPLAIN)\n"
                f"第 {seq} 条: {op_type} (不允许)\n"
                f"SQL: {stmt[:100]}"
            )

    if args.timeout is not None:
        conn, db_type = _open_raw_connection(args.db_alias, env, args.config,
                                             timeout=args.timeout)
    else:
        conn, db_type = _open_raw_connection(args.db_alias, env, args.config)

    try:
        print(f"━━━ {label} — {len(statements)} 条查询 ━━━")

        for seq, stmt in statements:
            try:
                est, summary = _get_explain_info(args.db_alias, stmt, env,
                                                 args.config, _conn=conn)
            except Exception:
                summary = None

            effective_limit = None
            sql_to_run = stmt
            has_limit = _has_limit(stmt)

            if args.no_limit:
                pass
            elif args.limit is not None and args.limit > 0:
                if not has_limit:
                    sql_to_run = _inject_limit(stmt, args.limit, db_type)
                    effective_limit = args.limit
            elif not has_limit:
                sql_to_run = _inject_limit(stmt, DEFAULT_LIMIT, db_type)
                effective_limit = DEFAULT_LIMIT

            cursor = conn.cursor()
            start = time.time()
            cursor.execute(sql_to_run)
            elapsed = time.time() - start
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            _log_query(args.db_alias, env, stmt.strip(), len(rows), elapsed,
                       op_type="READ")

            print(f"\n── [{seq}/{len(statements)}] {stmt[:60]}{'...' if len(stmt) > 60 else ''}")
            if summary:
                print(f"📊 EXPLAIN: {summary}")
            format_output(columns, rows, args.format)
            if effective_limit and len(rows) == effective_limit:
                print(f"(已截断至 {effective_limit} 行)")

    except Exception:
        raise
    finally:
        conn.close()


# ── Keychain 辅助 ────────────────────────────────────────────

def _handle_keychain_set(alias: str, env: str, args):
    if sys.platform != "darwin":
        print("[ERROR] Keychain 仅支持 macOS", file=sys.stderr)
        sys.exit(1)
    if alias:
        pass
    else:
        alias = args.db_alias
    if not alias:
        print("[ERROR] 请提供别名: --keychain-set <别名>", file=sys.stderr)
        sys.exit(1)
    service = _keychain_service(env, alias)
    pwd = getpass.getpass(f"请输入 [{alias}] ({env}) 密码: ")
    subprocess.run(
        [
            "security", "add-generic-password",
            "-a", "dbq",
            "-s", service,
            "-w", pwd,
            "-U",
        ],
        check=True,
    )
    print(f"密码已存入 Keychain (service={service})")


def _handle_keychain_get(alias: str, env: str):
    if sys.platform != "darwin":
        print("[ERROR] Keychain 仅支持 macOS", file=sys.stderr)
        sys.exit(1)
    try:
        pwd = _resolve_password(env, alias)
        print(pwd)
    except RuntimeError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


# ── 入口 ─────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="数据库查询工具 —— 多环境 SQL 查询/写入 (MySQL/PostgreSQL/SQLite)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python query.py mydb "SELECT * FROM users"                   # 默认 dev
  python query.py --env test mydb "SELECT * FROM users"        # test 环境
  python query.py --env prod mydb "SELECT * FROM users"        # prod 环境
  python query.py --limit 500 --env prod mydb "SELECT ..."     # 指定行数
  python query.py mydb "SELECT ..." --count                    # 只看行数
  python query.py mydb "SELECT ..." --timeout 30               # 30s 超时
  python query.py mydb "DELETE FROM logs WHERE id<100" --limit 500 --dry-run  # 预览
  python query.py --list                                       # 扫描所有环境
  python query.py --list --env prod                            # 只看 prod
  python query.py --env prod mydb --show                       # 列出 prod 全部表
  python query.py mydb --show "user_*"                        # 通配符匹配表名
  python query.py mydb -s user_info                           # 查单表元信息
  python query.py mydb --desc goods_gift                       # 查看表结构（表格）
  python query.py mydb --desc ALL                               # 全部表结构
  python query.py mydb --desc "user_*"                      # 通配符匹配
  python query.py mydb --ddl user_info                      # 查看 DDL
  python query.py mydb --ping                                    # 连接测试
  python query.py --keychain-set mydb --env prod               # 存密码
        """,
    )
    parser.add_argument("db_alias", nargs="?", help="数据库别名")
    parser.add_argument("sql", nargs="?", help="SQL 语句 (SELECT/INSERT/UPDATE/DELETE/REPLACE)")
    parser.add_argument(
        "--env", "-e", metavar="ENV",
        help="目标环境: dev / test / prod (默认: dev, 可通过 DB_QUERY_DEFAULT_ENV 环境变量修改)"
    )
    parser.add_argument(
        "--config", "-c", metavar="FILE",
        help="指定独立配置文件路径 (如 prod.yaml)"
    )
    parser.add_argument(
        "--format", "-f", choices=["table", "json", "csv"], default="table",
        help="输出格式 (默认: table)"
    )
    parser.add_argument(
        "--list", "-l", action="store_true",
        help="列出所有已配置的数据库连接"
    )
    parser.add_argument(
        "--show", "-s", nargs="?", const="ALL", default=False, metavar="TABLE",
        help="列出数据库表 (可指定表名 / 通配符: user_*, 默认 ALL)"
    )
    parser.add_argument(
        "--desc", "-d", metavar="TABLE",
        help="查看表结构 (TABLE=表名 / ALL=全部表 / user_*=通配符)"
    )
    parser.add_argument(
        "--ddl", metavar="TABLE",
        help="查看建表 DDL (TABLE=表名 / ALL=全部表 / user_*=通配符)"
    )
    parser.add_argument(
        "--ping", action="store_true",
        help="测试数据库连接是否可用"
    )
    parser.add_argument(
        "--keychain-set", dest="keychain_set", metavar="ALIAS",
        help="将密码存入 macOS Keychain"
    )
    parser.add_argument(
        "--keychain-get", dest="keychain_get", metavar="ALIAS",
        help="从 macOS Keychain 读取密码"
    )
    parser.add_argument(
        "--limit", metavar="N", type=int,
        help=f"限制行数 (SELECT 默认: {DEFAULT_LIMIT}; DELETE/UPDATE 需手动指定)"
    )
    parser.add_argument(
        "--no-limit", action="store_true",
        help="取消自动 LIMIT 限制（⚠️ 大表可能卡死）"
    )
    parser.add_argument(
        "--count", action="store_true",
        help="只执行 COUNT(*) 预估行数，不取数据（仅对 SELECT 有效）"
    )
    parser.add_argument(
        "--timeout", metavar="N", type=int,
        help="查询超时时间 (秒)，超时自动断开"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="预览 DML/DDL 操作，显示 EXPLAIN + SQL 但不执行"
    )
    parser.add_argument(
        "--multi", action="store_true",
        help="执行多条 SELECT（分号分隔），一次连接全部执行"
    )
    parser.add_argument(
        "--init-config", action="store_true",
        help="生成配置模板文件到 assets/ 目录（已存在则跳过）"
    )

    args = parser.parse_args()

    # ── --init-config ──
    if args.init_config:
        _handle_init_config()
        return

    env = args.env or DEFAULT_ENV

    # ── Keychain 操作 ──
    if args.keychain_set:
        _handle_keychain_set(args.keychain_set, env, args)
        return
    if args.keychain_get:
        _handle_keychain_get(args.keychain_get, env)
        return

    # ── --list ──
    if args.list:
        list_env = args.env
        list_connections(list_env, args.config)
        return

    if not args.db_alias:
        parser.print_help()
        sys.exit(1)

    # ── --ping ──
    if args.ping:
        try:
            start = time.time()
            conn, db_type = _open_raw_connection(args.db_alias, env, args.config)
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                elapsed = time.time() - start
                print(f"✅ [{args.db_alias}] ({env}) 连接成功 ({db_type}) - {elapsed:.3f}s")
            finally:
                conn.close()
        except Exception as e:
            print(f"❌ [{args.db_alias}] ({env}) 连接失败: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # ── --show ──
    if args.show is not False:
        try:
            pattern = args.show if isinstance(args.show, str) and args.show else None
            cols, all_rows = list_tables_with_info(args.db_alias, env, args.config)

            if pattern and (pattern.upper() == "ALL" or "*" in pattern or "?" in pattern):
                if pattern.upper() != "ALL":
                    all_rows = [r for r in all_rows if fnmatch.fnmatch(str(r[0]), pattern)]
            elif pattern:
                all_rows = [r for r in all_rows if str(r[0]) == pattern]

            label = f"{args.db_alias} ({env})"
            print(f"━━━ {label} — {len(all_rows)} 张表 ━━━")
            if all_rows:
                format_output(cols, all_rows, args.format, show_row_count=False)
            else:
                print("  (无匹配的表)")
        except Exception as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            sys.exit(1)
        return

    # ── --desc ──
    if args.desc:
        _handle_structure_cmd(args, "desc")
        return

    # ── --ddl ──
    if args.ddl:
        _handle_structure_cmd(args, "ddl")
        return

    # ── --multi 多条 SELECT ──
    if args.multi:
        _handle_multi_query(args)
        return

    # ── 查询 / 写操作 ──
    if not args.sql:
        parser.print_help()
        sys.exit(1)

    try:
        op_type = validate_sql(args.sql, args.db_alias, env, args.config,
                               dry_run=args.dry_run)
        sql = args.sql.strip()
        is_write = op_type in ("DML", "DDL")

        if args.count:
            if is_write:
                print("[ERROR] --count 仅适用于 SELECT 语句", file=sys.stderr)
                sys.exit(1)
            cnt = _execute_count(args.db_alias, sql, env, args.config)
            est, summary = _get_explain_info(args.db_alias, sql, env, args.config)
            print(f"环境: {env}")
            print(f"COUNT(*): {cnt:,}")
            if summary:
                print(f"📊 EXPLAIN: {summary}")
            return

        if is_write:
            _check_where_clause(sql, op_type)
            conn_info = get_connection(args.db_alias, env, args.config)
            db_type = conn_info["type"].lower()

            if not sql.upper().startswith("INSERT"):
                est, summary = _get_explain_info(args.db_alias, sql, env, args.config)
                if summary:
                    print(f"📊 [{env}] EXPLAIN: {summary}")
                if est is not None and est > LARGE_TABLE_THRESHOLD:
                    print(f"   ⚠️  预估影响 {_format_number(est)} 行 (大表)")

            if args.dry_run:
                print(f"\n🔍 [DRY-RUN] 以下操作未实际执行:")
                print(f"    SQL: {sql[:300]}")
                return

            _confirm_write(env, args.db_alias, conn_info, sql, op_type)

            effective_limit = None
            upper = sql.upper()
            if args.limit is not None and args.limit > 0:
                if (upper.startswith("DELETE") or upper.startswith("UPDATE")):
                    if not _has_limit(sql):
                        sql = _inject_limit(sql, args.limit, db_type)
                        effective_limit = args.limit

        else:
            est, summary = _get_explain_info(args.db_alias, sql, env, args.config)
            effective_limit = None

            has_limit = _has_limit(sql)
            if args.no_limit:
                pass
            elif args.limit is not None:
                if args.limit > 0:
                    if not has_limit:
                        sql = _inject_limit(sql, args.limit, db_type="mysql")
                    effective_limit = args.limit
            elif not has_limit:
                sql = _inject_limit(sql, DEFAULT_LIMIT, db_type="mysql")
                effective_limit = DEFAULT_LIMIT

            if est is not None and est > LARGE_TABLE_THRESHOLD:
                print(f"⚠️  [{env}] EXPLAIN: {summary}")
                if effective_limit and not args.no_limit:
                    print(f"   预估 {_format_number(est)} 行 (大表)，已自动 LIMIT {effective_limit}")
            elif summary:
                print(f"📊 [{env}] EXPLAIN: {summary}")

        columns, rows = execute_query(args.db_alias, sql, env, args.config,
                                      _timeout=args.timeout, _op_type=op_type)

        if is_write:
            print(f"✅ Query OK, {rows} row(s) affected")
        else:
            format_output(columns, rows, args.format)
            if effective_limit and len(rows) == effective_limit:
                print(f"(已截断至 {effective_limit} 行，数据可能不完整 • --no-limit 查看全部)")

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
