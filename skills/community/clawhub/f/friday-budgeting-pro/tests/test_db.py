"""
tests/test_db.py — Tests for server/db.py

Covers:
- init_db creates all expected tables
- insert + select rows from a few tables
- foreign key enforcement (IntegrityError on bad FK)
- transaction context manager commits on success / rolls back on exception
"""

import sqlite3
import uuid
from pathlib import Path

import pytest

from server.db import get_db, init_db, transaction

# All tables defined in db/schema.sql
EXPECTED_TABLES = {
    "bank_connections",
    "bank_accounts",
    "ledgers",
    "line_items",
    "transactions",
    "transaction_entries",
    "routing_rules",
    "classification_hints",
    "sync_cursors",
    "app_config",
    "sessions",
}


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    """Return a path to a freshly initialised temp database."""
    p = tmp_path / "test.db"
    init_db(p)
    return p


@pytest.fixture
def conn(db_path: Path):
    """Open a connection to the temp DB, yield it, then close."""
    c = get_db(db_path)
    yield c
    c.close()


# ---------------------------------------------------------------------------
# init_db: all expected tables exist
# ---------------------------------------------------------------------------


def test_init_db_creates_all_tables(db_path: Path) -> None:
    conn = get_db(db_path)
    rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    conn.close()
    actual = {r["name"] for r in rows}
    assert EXPECTED_TABLES.issubset(actual), f"Missing tables: {EXPECTED_TABLES - actual}"


def test_init_db_is_idempotent(db_path: Path) -> None:
    """Calling init_db a second time must not raise."""
    init_db(db_path)  # second call — schema uses IF NOT EXISTS


# ---------------------------------------------------------------------------
# get_db: row_factory and foreign keys
# ---------------------------------------------------------------------------


def test_get_db_row_factory(conn: sqlite3.Connection) -> None:
    """Rows must be accessible by column name (sqlite3.Row factory)."""
    conn.execute("INSERT INTO ledgers (id, name) VALUES (?, ?)", ("led-1", "Personal"))
    row = conn.execute("SELECT id, name FROM ledgers WHERE id = 'led-1'").fetchone()
    assert row["id"] == "led-1"
    assert row["name"] == "Personal"


# ---------------------------------------------------------------------------
# Insert + select from multiple tables
# ---------------------------------------------------------------------------


def test_insert_select_ledger_and_line_item(conn: sqlite3.Connection) -> None:
    """Insert a ledger and a line_item; verify they round-trip correctly."""
    lid = str(uuid.uuid4())
    conn.execute("INSERT INTO ledgers (id, name) VALUES (?, ?)", (lid, "Personal"))

    iid = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
        (iid, lid, "Groceries", "expense"),
    )
    conn.commit()

    row = conn.execute("SELECT name, item_type FROM line_items WHERE id = ?", (iid,)).fetchone()
    assert row["name"] == "Groceries"
    assert row["item_type"] == "expense"


def test_insert_select_classification_hint(conn: sqlite3.Connection) -> None:
    hid = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO classification_hints (id, text) VALUES (?, ?)",
        (hid, "Amazon charges are usually Shopping → Household"),
    )
    conn.commit()
    row = conn.execute("SELECT text FROM classification_hints WHERE id = ?", (hid,)).fetchone()
    assert "Amazon" in row["text"]


# ---------------------------------------------------------------------------
# Foreign key enforcement
# ---------------------------------------------------------------------------


def test_foreign_key_enforced(conn: sqlite3.Connection) -> None:
    """Inserting a line_item with a non-existent ledger_id must raise IntegrityError."""
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO line_items (id, ledger_id, name) VALUES (?, ?, ?)",
            (str(uuid.uuid4()), "nonexistent-ledger-id", "Bad Item"),
        )


# ---------------------------------------------------------------------------
# transaction() context manager
# ---------------------------------------------------------------------------


def test_transaction_commits_on_success(db_path: Path) -> None:
    c = get_db(db_path)
    lid = str(uuid.uuid4())
    with transaction(c):
        c.execute("INSERT INTO ledgers (id, name) VALUES (?, ?)", (lid, "Committed"))

    # Re-open to confirm the row persisted
    c2 = get_db(db_path)
    row = c2.execute("SELECT name FROM ledgers WHERE id = ?", (lid,)).fetchone()
    c2.close()
    c.close()
    assert row is not None
    assert row["name"] == "Committed"


def test_transaction_rolls_back_on_exception(db_path: Path) -> None:
    c = get_db(db_path)
    lid = str(uuid.uuid4())
    with pytest.raises(ValueError):
        with transaction(c):
            c.execute("INSERT INTO ledgers (id, name) VALUES (?, ?)", (lid, "ShouldRollBack"))
            raise ValueError("simulated error")

    # Re-open to confirm the row was NOT persisted
    c2 = get_db(db_path)
    row = c2.execute("SELECT name FROM ledgers WHERE id = ?", (lid,)).fetchone()
    c2.close()
    c.close()
    assert row is None
