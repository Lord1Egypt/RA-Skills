#!/usr/bin/env python3
"""Execute CSV import into SQLite, MySQL, or MariaDB with column mapping."""

import sys
import json
import sqlite3
import csv
import argparse


def import_csv_to_sqlite(csv_path, db_path, table_name, mapping):
    """Import CSV data into SQLite table."""
    if isinstance(mapping, str):
        mapping = json.loads(mapping)

    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV has no columns")

        dest_columns = list(mapping.values())
        placeholders = ", ".join(["?" for _ in dest_columns])

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        )
        if not cursor.fetchone():
            raise ValueError(f"Table '{table_name}' does not exist")

        inserted = 0
        for row in reader:
            values = [row.get(src, "") for src in mapping.keys()]
            try:
                cursor.execute(
                    f"INSERT INTO {table_name} ({', '.join(dest_columns)}) VALUES ({placeholders})",
                    values,
                )
                inserted += 1
            except Exception as e:
                print(f"Warning: Skipping row: {e}", file=sys.stderr)
                continue

        conn.commit()
        conn.close()
        return inserted


def import_csv_to_mysql(
    csv_path,
    table_name,
    mapping,
    host="localhost",
    user="root",
    password="",
    port=3306,
    database="",
):
    """Import CSV data into MySQL/MariaDB table."""
    try:
        import mysql.connector
    except ImportError:
        raise ImportError(
            "mysql-connector-python not installed. Run: pip install mysql-connector-python"
        )

    if isinstance(mapping, str):
        mapping = json.loads(mapping)

    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV has no columns")

        dest_columns = list(mapping.values())
        placeholders = ", ".join(["%s" for _ in dest_columns])

        conn = mysql.connector.connect(
            host=host, user=user, password=password, port=port, database=database
        )
        cursor = conn.cursor()

        inserted = 0
        for row in reader:
            values = [row.get(src, "") for src in mapping.keys()]
            try:
                cursor.execute(
                    f"INSERT INTO {table_name} ({', '.join(dest_columns)}) VALUES ({placeholders})",
                    values,
                )
                inserted += 1
            except Exception as e:
                print(f"Warning: Skipping row: {e}", file=sys.stderr)
                continue

        conn.commit()
        conn.close()
        return inserted


def import_sql_dump(
    sql_path,
    db_type,
    db_path="",
    host="localhost",
    user="root",
    password="",
    port=3306,
    database="",
):
    """Execute SQL dump file against database."""
    with open(sql_path, "r", encoding="utf-8", errors="ignore") as f:
        sql_content = f.read()

    statements = [
        s.strip()
        for s in sql_content.split(";")
        if s.strip() and not s.strip().startswith("--")
    ]

    if db_type == "sqlite":
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        executed = 0
        for stmt in statements:
            try:
                cursor.execute(stmt)
                executed += 1
            except Exception as e:
                print(f"Warning: Skipping statement: {e}", file=sys.stderr)
        conn.commit()
        conn.close()
        return executed
    else:
        try:
            import mysql.connector
        except ImportError:
            raise ImportError("mysql-connector-python not installed")

        conn = mysql.connector.connect(
            host=host, user=user, password=password, port=port, database=database
        )
        cursor = conn.cursor()
        executed = 0
        for stmt in statements:
            try:
                cursor.execute(stmt)
                executed += 1
            except Exception as e:
                print(f"Warning: Skipping statement: {e}", file=sys.stderr)
        conn.commit()
        conn.close()
        return executed


def main():
    parser = argparse.ArgumentParser(description="Import CSV or SQL into databases")
    parser.add_argument("type", choices=["csv", "sql"], help="Import type")
    parser.add_argument("path", help="Path to CSV or SQL file")
    parser.add_argument(
        "--db-type", choices=["sqlite", "mysql"], default="sqlite", help="Database type"
    )
    parser.add_argument("--db-path", help="Path to SQLite database")
    parser.add_argument("--table", help="Target table name for CSV import")
    parser.add_argument("--mapping", help="JSON mapping for CSV import")
    parser.add_argument("--host", default="localhost", help="MySQL host")
    parser.add_argument("--user", default="root", help="MySQL user")
    parser.add_argument("--password", default="", help="MySQL password")
    parser.add_argument("--port", type=int, default=3306, help="MySQL port")
    parser.add_argument("--database", help="MySQL database name")

    args = parser.parse_args()

    try:
        if args.type == "csv":
            if not args.table or not args.mapping:
                print("Error: --table and --mapping required for CSV import")
                sys.exit(1)

            if args.db_type == "sqlite":
                count = import_csv_to_sqlite(
                    args.path, args.db_path, args.table, args.mapping
                )
            else:
                count = import_csv_to_mysql(
                    args.path,
                    args.table,
                    args.mapping,
                    args.host,
                    args.user,
                    args.password,
                    args.port,
                    args.database,
                )
            print(f"Successfully imported {count} rows")

        elif args.type == "sql":
            count = import_sql_dump(
                args.path,
                args.db_type,
                args.db_path,
                args.host,
                args.user,
                args.password,
                args.port,
                args.database,
            )
            print(f"Successfully executed {count} statements")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
