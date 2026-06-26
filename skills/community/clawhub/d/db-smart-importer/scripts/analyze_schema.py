#!/usr/bin/env python3
"""Analyze schema from databases or CSV/SQL files."""

import sys
import json
import sqlite3
import csv
import re
import argparse


def analyze_sqlite(db_path):
    """Extract schema from SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    result = {"type": "sqlite", "tables": []}

    for (table_name,) in tables:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        table_info = {
            "name": table_name,
            "columns": [{"name": col[1], "type": col[2]} for col in columns],
        }
        result["tables"].append(table_info)

    conn.close()
    return result


def analyze_csv(csv_path):
    """Extract column names and sample data from CSV."""
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []

        samples = []
        for i, row in enumerate(reader):
            if i >= 5:
                break
            samples.append(row)

        return {"type": "csv", "columns": columns, "sample_rows": samples}


def analyze_sql(sql_path):
    """Extract table and column definitions from SQL dump file."""
    with open(sql_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    tables = []
    create_table_pattern = (
        r"CREATE TABLE[^\(]*\(`?([^`]+)`?\)\s*\(([\s\S]*?)\)(?:;|\s*ENGINE|=)"
    )

    for match in re.finditer(create_table_pattern, content, re.IGNORECASE):
        table_name = match.group(1).strip().strip("`")
        columns_def = match.group(2)

        columns = []
        for col_match in re.finditer(r"`?(\w+)`?\s+(\w+)", columns_def):
            columns.append(
                {"name": col_match.group(1), "type": col_match.group(2).upper()}
            )

        if columns:
            tables.append({"name": table_name, "columns": columns})

    insert_pattern = r"INSERT INTO[^\(]*\(`?([^`]+)`?\)\s*\(([\s\S]*?)\)"
    sample_inserts = []
    for match in re.finditer(insert_pattern, content, re.IGNORECASE):
        table_name = match.group(1).strip().strip("`")
        if len(sample_inserts) >= 3:
            break
        sample_inserts.append(table_name)

    return {"type": "sql", "tables": tables, "sample_inserts": sample_inserts}


def analyze_mysql(db_path, host="localhost", user="root", password="", port=3306):
    """Extract schema from MySQL/MariaDB database."""
    try:
        import mysql.connector

        conn = mysql.connector.connect(
            host=host, user=user, password=password, port=port, database=db_path
        )
        cursor = conn.cursor()

        cursor.execute("SHOW TABLES")
        table_names = [row[0] for row in cursor.fetchall()]

        result = {"type": "mysql", "tables": []}

        for table_name in table_names:
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()

            table_info = {
                "name": table_name,
                "columns": [{"name": col[0], "type": col[1]} for col in columns],
            }
            result["tables"].append(table_info)

        conn.close()
        return result
    except ImportError:
        return {"error": "mysql-connector-python not installed", "type": "mysql"}
    except Exception as e:
        return {"error": str(e), "type": "mysql"}


def main():
    parser = argparse.ArgumentParser(
        description="Analyze schema from databases or files"
    )
    parser.add_argument(
        "type", choices=["sqlite", "csv", "sql", "mysql"], help="Type to analyze"
    )
    parser.add_argument("path", help="Path to file or database")
    parser.add_argument("--host", default="localhost", help="MySQL host")
    parser.add_argument("--user", default="root", help="MySQL user")
    parser.add_argument("--password", default="", help="MySQL password")
    parser.add_argument("--port", type=int, default=3306, help="MySQL port")
    parser.add_argument("--database", help="MySQL database name")

    args = parser.parse_args()

    try:
        if args.type == "sqlite":
            result = analyze_sqlite(args.path)
        elif args.type == "csv":
            result = analyze_csv(args.path)
        elif args.type == "sql":
            result = analyze_sql(args.path)
        elif args.type == "mysql":
            result = analyze_mysql(
                args.database or args.path,
                args.host,
                args.user,
                args.password,
                args.port,
            )

        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
