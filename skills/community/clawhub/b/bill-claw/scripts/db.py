"""SQLite access: transactions + user_categories migration."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

DEFAULT_EXPENSE_CATEGORIES = (
    "正餐",
    "零食饮料",
    "出行",
    "购物",
    "日常开销",
    "娱乐",
    "居住",
    "医疗健康",
    "家人",
    "社交",
    "其他",
)
DEFAULT_INCOME_CATEGORIES = ("工资", "奖金", "投资", "家人", "其他收入")


def default_db_path() -> Path:
    # scripts/db.py -> project root/db/expenses.db
    root = Path(__file__).resolve().parent.parent
    return root / "db" / "expenses.db"


def connect(db_path: Path | str | None = None) -> sqlite3.Connection:
    path = Path(db_path) if db_path else default_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def migrate(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            note TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            source TEXT DEFAULT 'manual'
        );
        CREATE INDEX IF NOT EXISTS idx_date ON transactions(date);
        CREATE INDEX IF NOT EXISTS idx_type ON transactions(type);
        CREATE INDEX IF NOT EXISTS idx_category ON transactions(category);

        CREATE TABLE IF NOT EXISTS user_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            kind TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()


@contextmanager
def get_connection(db_path: Path | str | None = None) -> Iterator[sqlite3.Connection]:
    conn = connect(db_path)
    try:
        migrate(conn)
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def insert_transaction(
    conn: sqlite3.Connection,
    *,
    date: str,
    type_: str,
    category: str,
    amount: float,
    note: str | None = None,
    source: str = "manual",
) -> int:
    cur = conn.execute(
        """
        INSERT INTO transactions (date, type, category, amount, note, source)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (date, type_, category, amount, note, source),
    )
    return int(cur.lastrowid)


def _transaction_filter_clauses(
    *,
    date_from: str | None = None,
    date_to: str | None = None,
    type_: str | None = None,
    category: str | None = None,
    category_like: str | None = None,
    note_like: str | None = None,
    keyword_in_note: str | None = None,
) -> tuple[list[str], list[Any]]:
    clauses: list[str] = ["1=1"]
    params: list[Any] = []
    if date_from:
        clauses.append("date >= ?")
        params.append(date_from)
    if date_to:
        clauses.append("date <= ?")
        params.append(date_to)
    if type_:
        clauses.append("type = ?")
        params.append(type_)
    if category:
        clauses.append("category = ?")
        params.append(category)
    if category_like:
        clauses.append("category LIKE ?")
        params.append(f"%{category_like}%")
    if note_like:
        clauses.append("note LIKE ?")
        params.append(f"%{note_like}%")
    if keyword_in_note:
        clauses.append("(note LIKE ? OR category LIKE ?)")
        params.extend([f"%{keyword_in_note}%", f"%{keyword_in_note}%"])
    return clauses, params


def query_transactions(
    conn: sqlite3.Connection,
    *,
    date_from: str | None = None,
    date_to: str | None = None,
    type_: str | None = None,
    category: str | None = None,
    category_like: str | None = None,
    note_like: str | None = None,
    keyword_in_note: str | None = None,
    limit: int | None = 500,
    offset: int = 0,
) -> list[dict[str, Any]]:
    clauses, params = _transaction_filter_clauses(
        date_from=date_from,
        date_to=date_to,
        type_=type_,
        category=category,
        category_like=category_like,
        note_like=note_like,
        keyword_in_note=keyword_in_note,
    )
    where = " AND ".join(clauses)
    sql = f"SELECT * FROM transactions WHERE {where} ORDER BY date DESC, id DESC"
    if limit is not None:
        sql += f" LIMIT {int(limit)} OFFSET {int(offset)}"
    rows = conn.execute(sql, params).fetchall()
    return [_row_to_dict(r) for r in rows]


def count_transactions(
    conn: sqlite3.Connection,
    *,
    date_from: str | None = None,
    date_to: str | None = None,
    type_: str | None = None,
    category: str | None = None,
    category_like: str | None = None,
    note_like: str | None = None,
    keyword_in_note: str | None = None,
) -> int:
    clauses, params = _transaction_filter_clauses(
        date_from=date_from,
        date_to=date_to,
        type_=type_,
        category=category,
        category_like=category_like,
        note_like=note_like,
        keyword_in_note=keyword_in_note,
    )
    where = " AND ".join(clauses)
    row = conn.execute(
        f"SELECT COUNT(*) FROM transactions WHERE {where}", params
    ).fetchone()
    return int(row[0])


def get_transaction_by_id(conn: sqlite3.Connection, tid: int) -> dict[str, Any] | None:
    row = conn.execute("SELECT * FROM transactions WHERE id = ?", (tid,)).fetchone()
    return _row_to_dict(row) if row else None


def delete_by_ids(conn: sqlite3.Connection, ids: list[int]) -> int:
    if not ids:
        return 0
    placeholders = ",".join("?" * len(ids))
    cur = conn.execute(f"DELETE FROM transactions WHERE id IN ({placeholders})", ids)
    return cur.rowcount


def update_category_for_ids(
    conn: sqlite3.Connection, ids: list[int], new_category: str
) -> int:
    if not ids:
        return 0
    placeholders = ",".join("?" * len(ids))
    cur = conn.execute(
        f"UPDATE transactions SET category = ? WHERE id IN ({placeholders})",
        [new_category, *ids],
    )
    return cur.rowcount


def list_user_categories(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute(
        "SELECT id, name, kind, created_at FROM user_categories ORDER BY name"
    ).fetchall()
    return [dict(r) for r in rows]


def add_user_category(conn: sqlite3.Connection, name: str, kind: str) -> int:
    cur = conn.execute(
        "INSERT INTO user_categories (name, kind) VALUES (?, ?)", (name, kind)
    )
    return int(cur.lastrowid)


def user_category_exists(conn: sqlite3.Connection, name: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM user_categories WHERE name = ?", (name,)
    ).fetchone()
    return row is not None


def aggregate_by_category(
    conn: sqlite3.Connection,
    *,
    date_from: str | None = None,
    date_to: str | None = None,
    type_: str | None = None,
) -> list[dict[str, Any]]:
    clauses: list[str] = ["1=1"]
    params: list[Any] = []
    if date_from:
        clauses.append("date >= ?")
        params.append(date_from)
    if date_to:
        clauses.append("date <= ?")
        params.append(date_to)
    if type_:
        clauses.append("type = ?")
        params.append(type_)
    where = " AND ".join(clauses)
    sql = f"""
        SELECT category, type, SUM(amount) AS total, COUNT(*) AS cnt
        FROM transactions
        WHERE {where}
        GROUP BY category, type
        ORDER BY total DESC
    """
    rows = conn.execute(sql, params).fetchall()
    return [dict(r) for r in rows]


def totals(
    conn: sqlite3.Connection,
    *,
    date_from: str | None = None,
    date_to: str | None = None,
) -> dict[str, float]:
    clauses: list[str] = ["1=1"]
    params: list[Any] = []
    if date_from:
        clauses.append("date >= ?")
        params.append(date_from)
    if date_to:
        clauses.append("date <= ?")
        params.append(date_to)
    where = " AND ".join(clauses)
    income = conn.execute(
        f"SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE {where} AND type = ?",
        [*params, "收入"],
    ).fetchone()[0]
    expense = conn.execute(
        f"SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE {where} AND type = ?",
        [*params, "支出"],
    ).fetchone()[0]
    return {
        "income": float(income),
        "expense": float(expense),
        "balance": float(income) - float(expense),
    }


def daily_totals(
    conn: sqlite3.Connection,
    *,
    date_from: str | None = None,
    date_to: str | None = None,
) -> list[dict[str, Any]]:
    clauses: list[str] = ["1=1"]
    params: list[Any] = []
    if date_from:
        clauses.append("date >= ?")
        params.append(date_from)
    if date_to:
        clauses.append("date <= ?")
        params.append(date_to)
    where = " AND ".join(clauses)
    rows = conn.execute(
        f"""
        SELECT date,
               SUM(CASE WHEN type = '收入' THEN amount ELSE 0 END) AS income,
               SUM(CASE WHEN type = '支出' THEN amount ELSE 0 END) AS expense
        FROM transactions
        WHERE {where}
        GROUP BY date
        ORDER BY date
        """,
        params,
    ).fetchall()
    return [
        {
            "date": r["date"],
            "income": float(r["income"] or 0),
            "expense": float(r["expense"] or 0),
        }
        for r in rows
    ]


def monthly_totals(
    conn: sqlite3.Connection,
    *,
    date_from: str | None = None,
    date_to: str | None = None,
) -> list[dict[str, Any]]:
    clauses, params = _transaction_filter_clauses(
        date_from=date_from, date_to=date_to
    )
    where = " AND ".join(clauses)
    rows = conn.execute(
        f"""
        SELECT substr(date, 1, 7) AS month,
               SUM(CASE WHEN type = '收入' THEN amount ELSE 0 END) AS income,
               SUM(CASE WHEN type = '支出' THEN amount ELSE 0 END) AS expense
        FROM transactions
        WHERE {where}
        GROUP BY substr(date, 1, 7)
        ORDER BY month
        """,
        params,
    ).fetchall()
    return [
        {
            "month": r["month"],
            "income": float(r["income"] or 0),
            "expense": float(r["expense"] or 0),
        }
        for r in rows
    ]


def transaction_date_bounds(conn: sqlite3.Connection) -> dict[str, str | None]:
    row = conn.execute(
        "SELECT MIN(date) AS dmin, MAX(date) AS dmax FROM transactions"
    ).fetchone()
    return {"date_min": row["dmin"], "date_max": row["dmax"]}


def _row_to_dict(row: sqlite3.Row | None) -> dict[str, Any]:
    if row is None:
        return {}
    d = dict(row)
    if "amount" in d and d["amount"] is not None:
        d["amount"] = float(d["amount"])
    return d


def is_valid_builtin_category(category: str, kind: str) -> bool:
    if kind == "支出":
        return category in DEFAULT_EXPENSE_CATEGORIES
    if kind == "收入":
        return category in DEFAULT_INCOME_CATEGORIES
    return False
