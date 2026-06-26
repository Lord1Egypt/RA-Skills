"""Command-line entry point for database-skill.

Usage::

    python main.py --url jdbc:mysql://localhost:3306/mydb \\
        --user root --password '${DB_PASS}' --tables

See ``--help`` for full documentation.
"""
import argparse
import logging
import sys
import os
from typing import Optional

from connection_manager import (
    ConnectionManager,
    load_config,
    resolve_driver,
    resolve_env_vars,
)
from connections_store import ConnectionsStore, ConnectionRecord, _extract_host_db
from exceptions import DatabaseSkillError
from query_executor import QueryExecutor
from schema_inspector import SchemaInspector

logger = logging.getLogger(__name__)

_store = ConnectionsStore()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="database-skill",
        description="Database connectivity tool for opencode — MySQL, PostgreSQL, Oracle, SQL Server, SQLite.",
        epilog="Password can be passed via environment variable ${VAR_NAME} in config files.",
    )
    parser.add_argument(
        "--config",
        default="datasource.yml",
        help="Path to YAML config file (default: datasource.yml, falls back to classpath).",
    )
    parser.add_argument("--url", help="JDBC URL (e.g. jdbc:mysql://host:3306/db).")
    parser.add_argument("--user", help="Database username.")
    parser.add_argument("--password", help="Database password.")
    parser.add_argument(
        "--query",
        nargs="+",
        help="SELECT query with optional parameterized values. "
        "Use '?' as placeholder: --query \"SELECT * FROM t WHERE x = ?\" val1",
    )
    parser.add_argument(
        "--update",
        nargs="+",
        help="UPDATE/INSERT/DELETE with optional parameterized values.",
    )
    parser.add_argument(
        "--batch",
        help="File containing one SQL statement per line (no parameterized bindings).",
    )
    parser.add_argument(
        "--tables",
        action="store_true",
        help="List all tables in the current database.",
    )
    parser.add_argument(
        "--columns",
        help="Show column metadata for a specific table.",
    )
    parser.add_argument(
        "--list-connections",
        action="store_true",
        help="Show all saved database connections.",
    )
    parser.add_argument(
        "--forget",
        help="Remove a saved connection by URL.",
    )
    return parser


def _interactive_select_connection() -> bool:
    """If no --url or --config is given, show saved connections and let user pick.

    Returns True if a connection was selected (args updated via side-channel),
    False if caller should fall through.
    """
    records = _store.load_all()
    if not records:
        return False

    print("Saved connections:")
    for i, r in enumerate(records):
        display_url = r.url.split("?")[0].replace(r.username, "***") if r.username else r.url.split("?")[0]
        print(f"  [{i}] {r.label}  ({display_url})")
    print("  [N] Enter a new connection")
    try:
        choice = input("\nSelect a connection (number or N): ").strip()
        if choice.upper() == "N":
            return False
        idx = int(choice)
        record = _store.get_by_index(idx)
        if record is None:
            print("Invalid selection.")
            return False
        # Override via module-level trick: we return the record
        # and the caller applies it
        _apply_record(record)
        return True
    except (ValueError, IndexError):
        return False


_ACTIVE_RECORD: Optional["ConnectionRecord"] = None


def _apply_record(record: ConnectionRecord) -> None:
    global _ACTIVE_RECORD
    _ACTIVE_RECORD = record


def entry_point() -> None:
    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s: %(message)s",
    )
    parser = _build_parser()
    args = parser.parse_args()

    # --- handle connection metadata commands ---
    if args.list_connections:
        records = _store.load_all()
        if not records:
            print("No saved connections.")
            return
        print("Saved connections:")
        for i, r in enumerate(records):
            pwd_info = f"env:${r.password_env_var}" if r.has_password() else "manual input"
            print(f"  [{i}] {r.label}")
            print(f"       URL:  {r.url}")
            print(f"       User: {r.username}")
            print(f"       Type: {r.driver}")
            print(f"       Password: {pwd_info}")
        return

    if args.forget:
        _store.remove(args.forget)
        print(f"Removed connection: {args.forget}")
        return

    # --- resolve connection parameters ---
    url = ""
    username = ""
    password = ""
    password_env_var = ""

    def _fill_from_cache(u: str, usr: str) -> None:
        nonlocal password, password_env_var
        for r in _store.load_all():
            if r.identity() == f"{usr}@{_extract_host_db(u)}":
                if r.has_password():
                    password_env_var = r.password_env_var
                    password = r.get_password()
                    print(f"Using saved connection: {r.label}")
                    print(f"  Password: from env ${password_env_var}")
                return

    import re as _re
    _ENV_RE = _re.compile(r"\$\{(\w+)\}")

    if args.url:
        url = args.url
        username = args.user or ""
        raw_password = args.password or ""
        # Detect "${VAR_NAME}", "${env:VAR_NAME}", "$env:VAR_NAME", or plain "VAR_NAME"
        m = _re.match(r"^\$\{(?:env:)?(\w+)\}$", raw_password)
        if m:
            password_env_var = m.group(1)
            password = os.environ.get(password_env_var, "")
        elif _re.match(r"^\$env:(\w+)$", raw_password, _re.IGNORECASE):
            password_env_var = _re.match(r"^\$env:(\w+)$", raw_password, _re.IGNORECASE).group(1)
            password = os.environ.get(password_env_var, "")
        elif _re.match(r"^[A-Z_][A-Z0-9_]*$", raw_password.upper()) and not _re.match(r"^\d", raw_password):
            password_env_var = raw_password
            password = os.environ.get(password_env_var, "")
        elif raw_password:
            password = raw_password
        if not password:
            _fill_from_cache(url, username)
    elif _ACTIVE_RECORD is not None:
        url = _ACTIVE_RECORD.url
        username = _ACTIVE_RECORD.username
        if _ACTIVE_RECORD.has_password():
            password_env_var = _ACTIVE_RECORD.password_env_var
            password = _ACTIVE_RECORD.get_password()
            print(f"Using saved connection: {_ACTIVE_RECORD.label}")
            print(f"  URL:  {url}  User: {username}")
            print(f"  Password: from env ${password_env_var}")
        else:
            print(f"Using saved connection: {_ACTIVE_RECORD.label}")
            print(f"  URL:  {url}  User: {username}")
            pwd = input("  Password (leave blank if none): ").strip()
            password = pwd
    else:
        config = load_config(args.config)
        ds = config.get("datasource", {})
        raw_url = ds.get("url", "")
        raw_username = ds.get("username", "")
        raw_password = ds.get("password", "")
        cfg_url = resolve_env_vars(raw_url)
        cfg_user = resolve_env_vars(raw_username)
        if cfg_url:
            url = cfg_url
            username = cfg_user
            pm = _ENV_RE.search(raw_password or "")
            if pm:
                password_env_var = pm.group(1)
                password = resolve_env_vars(raw_password)
            if not password:
                _fill_from_cache(url, username)
        else:
            if _interactive_select_connection() and _ACTIVE_RECORD is not None:
                url = _ACTIVE_RECORD.url
                username = _ACTIVE_RECORD.username
                if _ACTIVE_RECORD.has_password():
                    password_env_var = _ACTIVE_RECORD.password_env_var
                    password = _ACTIVE_RECORD.get_password()
                    print(f"Using saved connection: {_ACTIVE_RECORD.label}")
                    print(f"  URL:  {url}  User: {username}")
                    print(f"  Password: from env ${password_env_var}")
                else:
                    print(f"Using saved connection: {_ACTIVE_RECORD.label}")
                    print(f"  URL:  {url}  User: {username}")
                    pwd = input("  Password (leave blank if none): ").strip()
                    password = pwd

    driver = resolve_driver(url)
    cm = ConnectionManager(url, username, password, driver)
    executor = QueryExecutor(cm)
    inspector = SchemaInspector(cm)

    try:
        if args.query:
            _do_query(executor, args.query)
        elif args.update:
            _do_update(executor, args.update)
        elif args.batch:
            _do_batch(executor, args.batch)
        elif args.tables:
            _do_tables(inspector)
        elif args.columns:
            _do_columns(inspector, args.columns)
        else:
            parser.print_help()
        # Save connection on success
        record = ConnectionRecord(
            url=url, username=username, driver=driver,
            password_env_var=password_env_var,
        )
        _store.save(record)
    except DatabaseSkillError as exc:
        logger.error(str(exc))
        sys.exit(1)
    finally:
        cm.shutdown()


def _do_query(executor: QueryExecutor, query_args: list) -> None:
    sql = query_args[0]
    params = query_args[1:]
    results = executor.execute_query(sql, *params)
    if not results:
        print("(no rows)")
        return
    print(f"({len(results)} rows)\n")
    for row in results:
        print(dict(row))


def _do_update(executor: QueryExecutor, update_args: list) -> None:
    sql = update_args[0]
    params = update_args[1:]
    affected = executor.execute_update(sql, *params)
    print(f"OK ({affected} rows affected)")


def _do_batch(executor: QueryExecutor, file_path: str) -> None:
    with open(file_path, "r") as f:
        sql_list = [line.strip() for line in f if line.strip()]
    results = executor.execute_batch(sql_list)
    print(f"Batch complete: {len(results)} statements executed")


def _do_tables(inspector: SchemaInspector) -> None:
    tables = inspector.get_tables()
    if not tables:
        print("(no tables)")
        return
    print(f"Tables ({len(tables)}):")
    for t in tables:
        print(f"  {t['name']} ({t['type']})")


def _do_columns(inspector: SchemaInspector, table_name: str) -> None:
    columns = inspector.get_columns(table_name)
    if not columns:
        print("(no columns or table not found)")
        return
    print(f"Columns of {table_name}:")
    for col in columns:
        pk = " PK" if col.get("primaryKey") else ""
        auto = " AUTO" if col.get("autoIncrement") else ""
        print(f"  {col['name']} {col['type']}{pk}{auto}")


if __name__ == "__main__":
    entry_point()
