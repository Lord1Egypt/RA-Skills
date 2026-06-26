import argparse
import csv
import json
import sqlite3
from collections import defaultdict
from pathlib import Path


def runtime_dir(base_dir):
    path = Path(base_dir) / ".runtime"
    path.mkdir(parents=True, exist_ok=True)
    return path


def db_path(base_dir):
    return runtime_dir(base_dir) / "expense-snap.db"


def get_connection(base_dir):
    connection = sqlite3.connect(db_path(base_dir))
    connection.row_factory = sqlite3.Row
    ensure_schema(connection)
    return connection


def ensure_schema(connection):
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            merchant TEXT NOT NULL,
            purchased_on TEXT NOT NULL,
            currency TEXT NOT NULL,
            total REAL NOT NULL,
            tax REAL,
            payment_method TEXT,
            category TEXT NOT NULL,
            notes TEXT,
            image_path TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS line_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            quantity REAL NOT NULL,
            category TEXT NOT NULL,
            FOREIGN KEY(receipt_id) REFERENCES receipts(id)
        );
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL UNIQUE,
            monthly_limit REAL NOT NULL,
            currency TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        """
    )
    connection.commit()


def now_iso():
    from datetime import datetime

    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def row_to_dict(row):
    return {key: row[key] for key in row.keys()}


def parse_line_item(raw_value):
    parts = [part.strip() for part in raw_value.split("|")]
    if len(parts) != 4:
        raise ValueError("line-item values must use description|amount|quantity|category")
    description, amount, quantity, category = parts
    return {
      "description": description,
      "amount": float(amount),
      "quantity": float(quantity),
      "category": category,
    }


def parse_budget(raw_value):
    parts = [part.strip() for part in raw_value.split("|")]
    if len(parts) != 2:
        raise ValueError("budget values must use category|monthly_limit")
    category, monthly_limit = parts
    return {"category": category, "monthly_limit": float(monthly_limit)}


def record_receipt(args):
    timestamp = now_iso()
    line_items = [parse_line_item(item) for item in args.line_item]
    budgets = [parse_budget(item) for item in args.budget]
    with get_connection(args.base_dir) as connection:
        cursor = connection.execute(
            """
            INSERT INTO receipts
                (merchant, purchased_on, currency, total, tax, payment_method, category, notes, image_path, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                args.merchant,
                args.date,
                args.currency,
                args.total,
                args.tax,
                args.payment_method,
                args.category,
                args.notes,
                args.image_path,
                timestamp,
                timestamp,
            ),
        )
        receipt_id = cursor.lastrowid
        for item in line_items:
            connection.execute(
                """
                INSERT INTO line_items (receipt_id, description, amount, quantity, category)
                VALUES (?, ?, ?, ?, ?)
                """,
                (receipt_id, item["description"], item["amount"], item["quantity"], item["category"]),
            )
        for budget in budgets:
            connection.execute(
                """
                INSERT INTO budgets (category, monthly_limit, currency, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(category) DO UPDATE SET
                    monthly_limit = excluded.monthly_limit,
                    currency = excluded.currency,
                    updated_at = excluded.updated_at
                """,
                (budget["category"], budget["monthly_limit"], args.currency, timestamp, timestamp),
            )
        connection.commit()
        receipt = connection.execute("SELECT * FROM receipts WHERE id = ?", (receipt_id,)).fetchone()
        print(json.dumps({"receipt": row_to_dict(receipt), "lineItems": line_items}, indent=2))


def list_receipts(args):
    query = "SELECT * FROM receipts"
    clauses = []
    values = []
    if args.month:
      clauses.append("substr(purchased_on, 1, 7) = ?")
      values.append(args.month)
    if args.category:
      clauses.append("category = ?")
      values.append(args.category)
    if clauses:
      query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY purchased_on DESC, id DESC LIMIT ?"
    values.append(args.limit)
    with get_connection(args.base_dir) as connection:
      rows = connection.execute(query, values).fetchall()
      print(json.dumps({"receipts": [row_to_dict(row) for row in rows]}, indent=2))


def monthly_report(args):
    with get_connection(args.base_dir) as connection:
        rows = connection.execute(
            """
            SELECT category, SUM(total) AS total
            FROM receipts
            WHERE substr(purchased_on, 1, 7) = ?
            GROUP BY category
            ORDER BY total DESC, category ASC
            """,
            (args.month,),
        ).fetchall()
        budget_rows = connection.execute("SELECT category, monthly_limit, currency FROM budgets").fetchall()
        budgets = {row["category"]: row_to_dict(row) for row in budget_rows}
        by_category = []
        grand_total = 0.0
        for row in rows:
            total = float(row["total"] or 0)
            grand_total += total
            budget = budgets.get(row["category"])
            by_category.append(
                {
                    "category": row["category"],
                    "total": round(total, 2),
                    "budget": budget["monthly_limit"] if budget else None,
                    "overBudget": round(total - budget["monthly_limit"], 2) if budget and total > budget["monthly_limit"] else 0.0,
                }
            )
        print(json.dumps({"month": args.month, "grandTotal": round(grand_total, 2), "byCategory": by_category}, indent=2))


def export_csv(args):
    with get_connection(args.base_dir) as connection:
        rows = connection.execute(
            """
            SELECT merchant, purchased_on, currency, total, category, payment_method, notes
            FROM receipts
            WHERE substr(purchased_on, 1, 7) = ?
            ORDER BY purchased_on ASC, id ASC
            """,
            (args.month,),
        ).fetchall()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["merchant", "purchased_on", "currency", "total", "category", "payment_method", "notes"])
        for row in rows:
            writer.writerow([row[key] for key in row.keys()])

    print(json.dumps({"output": str(output), "rows": len(rows)}, indent=2))


def build_parser():
    parser = argparse.ArgumentParser(description="Record and summarize expenses.")
    parser.add_argument("--base-dir", default=Path(__file__).resolve().parents[1], help="Skill directory")
    subparsers = parser.add_subparsers(dest="command", required=True)

    record_parser = subparsers.add_parser("record")
    record_parser.add_argument("--merchant", required=True)
    record_parser.add_argument("--date", required=True)
    record_parser.add_argument("--total", required=True, type=float)
    record_parser.add_argument("--currency", default="EUR")
    record_parser.add_argument("--tax", type=float)
    record_parser.add_argument("--payment-method")
    record_parser.add_argument("--category", default="uncategorized")
    record_parser.add_argument("--notes")
    record_parser.add_argument("--image-path")
    record_parser.add_argument("--line-item", action="append", default=[])
    record_parser.add_argument("--budget", action="append", default=[])
    record_parser.set_defaults(handler=record_receipt)

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--month")
    list_parser.add_argument("--category")
    list_parser.add_argument("--limit", type=int, default=50)
    list_parser.set_defaults(handler=list_receipts)

    report_parser = subparsers.add_parser("monthly-report")
    report_parser.add_argument("--month", required=True)
    report_parser.set_defaults(handler=monthly_report)

    export_parser = subparsers.add_parser("export-csv")
    export_parser.add_argument("--month", required=True)
    export_parser.add_argument("--output", required=True)
    export_parser.set_defaults(handler=export_csv)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
