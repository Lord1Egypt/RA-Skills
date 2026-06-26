#!/usr/bin/env python3
"""
Query AccountantPriv SQLite databases.

Usage:
    uv run python query_db.py --db hapoalim --sql "SELECT * FROM hapoalim_transactions LIMIT 5"
    uv run python query_db.py --db isracard --sql "SELECT category, SUM(billed_amount) FROM isracard_transactions GROUP BY category"
    uv run python query_db.py --db max --sql "SELECT * FROM max_transactions LIMIT 5"
    uv run python query_db.py --db hapoalim --list-tables
"""

import argparse
import sqlite3
import json
from pathlib import Path

# Database paths
BASE_DIR = Path("/Users/sharontourjeman/accountantpriv/output")
DB_PATHS = {
    "hapoalim": BASE_DIR / "hapoalim.db",
    "isracard": BASE_DIR / "isracard.db",
    "max": BASE_DIR / "max.db",
}


def get_db_path(db_name: str) -> Path:
    """Get database path by name."""
    if db_name not in DB_PATHS:
        raise ValueError(f"Unknown database: {db_name}. Available: {list(DB_PATHS.keys())}")
    return DB_PATHS[db_name]


def list_tables(db_path: Path) -> list[str]:
    """List all tables in the database."""
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables


def get_table_schema(db_path: Path, table_name: str) -> list[dict]:
    """Get column info for a table."""
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [
        {"cid": row[0], "name": row[1], "type": row[2], "notnull": row[3], "default": row[4], "pk": row[5]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return columns


def execute_query(db_path: Path, sql: str, params: tuple = ()) -> list[dict]:
    """Execute a SELECT query and return results as list of dicts."""
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, params)
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def main():
    parser = argparse.ArgumentParser(description="Query AccountantPriv databases")
    parser.add_argument("--db", required=True, choices=list(DB_PATHS.keys()), help="Database to query")
    parser.add_argument("--sql", help="SQL query to execute")
    parser.add_argument("--list-tables", action="store_true", help="List all tables")
    parser.add_argument("--schema", help="Get schema for a specific table")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    db_path = get_db_path(args.db)

    if args.list_tables:
        tables = list_tables(db_path)
        if args.json:
            print(json.dumps({"tables": tables}, indent=2))
        else:
            print(f"Tables in {args.db}:")
            for table in tables:
                print(f"  - {table}")
        return

    if args.schema:
        schema = get_table_schema(db_path, args.schema)
        if args.json:
            print(json.dumps(schema, indent=2))
        else:
            print(f"Schema for {args.schema}:")
            for col in schema:
                pk = " [PK]" if col["pk"] else ""
                print(f"  {col['name']}: {col['type']}{pk}")
        return

    if args.sql:
        try:
            results = execute_query(db_path, args.sql)
            if args.json:
                print(json.dumps(results, indent=2, default=str))
            else:
                if not results:
                    print("No results.")
                    return
                # Print as table
                headers = list(results[0].keys())
                print(" | ".join(headers))
                print("-" * (len(headers) * 20))
                for row in results:
                    print(" | ".join(str(v) for v in row.values()))
        except sqlite3.Error as e:
            print(f"SQL Error: {e}")
            return
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
