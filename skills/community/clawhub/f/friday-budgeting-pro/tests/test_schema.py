"""
Tests for db/schema.sql — creates an in-memory SQLite DB from the schema
and asserts all tables and key columns exist.
"""

import pathlib
import sqlite3

SCHEMA_PATH = pathlib.Path(__file__).parent.parent / "db" / "schema.sql"


def get_connection() -> sqlite3.Connection:
    sql = SCHEMA_PATH.read_text()
    conn = sqlite3.connect(":memory:")
    conn.executescript(sql)
    return conn


def tables(conn: sqlite3.Connection) -> set[str]:
    rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    return {r[0] for r in rows}


def columns(conn: sqlite3.Connection, table: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return {r[1] for r in rows}


def test_all_tables_exist():
    conn = get_connection()
    expected = {
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
    assert expected <= tables(conn), f"Missing tables: {expected - tables(conn)}"


def test_bank_connections_columns():
    conn = get_connection()
    cols = columns(conn, "bank_connections")
    assert {
        "id",
        "plaid_item_id",
        "plaid_access_token_encrypted",
        "institution_name",
        "status",
        "last_synced_at",
    } <= cols


def test_bank_accounts_columns():
    conn = get_connection()
    cols = columns(conn, "bank_accounts")
    assert {"id", "connection_id", "plaid_account_id", "name", "mask", "type", "subtype"} <= cols


def test_ledgers_columns():
    conn = get_connection()
    cols = columns(conn, "ledgers")
    assert {"id", "name"} <= cols


def test_line_items_columns():
    conn = get_connection()
    cols = columns(conn, "line_items")
    assert {"id", "ledger_id", "name", "item_type"} <= cols


def test_transactions_columns():
    conn = get_connection()
    cols = columns(conn, "transactions")
    assert {
        "id",
        "bank_account_id",
        "plaid_transaction_id",
        "date",
        "merchant",
        "amount",
        "plaid_category",
        "pending",
    } <= cols


def test_transaction_entries_columns():
    conn = get_connection()
    cols = columns(conn, "transaction_entries")
    assert {
        "id",
        "transaction_id",
        "ledger_id",
        "line_item_id",
        "amount",
        "source",
        "confidence",
        "reviewed",
    } <= cols


def test_routing_rules_columns():
    conn = get_connection()
    cols = columns(conn, "routing_rules")
    assert {"id", "merchant_pattern", "line_item_id"} <= cols


def test_classification_hints_columns():
    conn = get_connection()
    cols = columns(conn, "classification_hints")
    assert {"id", "text"} <= cols


def test_sync_cursors_columns():
    conn = get_connection()
    cols = columns(conn, "sync_cursors")
    assert {"connection_id", "cursor", "last_synced_at"} <= cols


def test_app_config_columns():
    conn = get_connection()
    cols = columns(conn, "app_config")
    assert {"id", "ui_password_hash", "ui_password_set_at"} <= cols


def test_sessions_columns():
    conn = get_connection()
    cols = columns(conn, "sessions")
    assert {"id", "created_at", "last_seen_at", "expires_at", "user_agent"} <= cols


def test_schema_loads_twice_idempotent():
    """IF NOT EXISTS means re-running the schema is safe."""
    conn = get_connection()
    sql = SCHEMA_PATH.read_text()
    conn.executescript(sql)  # second run — should not raise
    assert "transactions" in tables(conn)
