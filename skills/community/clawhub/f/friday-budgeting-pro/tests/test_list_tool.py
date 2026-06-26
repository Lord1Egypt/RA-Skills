"""
tests/test_list_tool.py — Tests for list() and get_needs_review() MCP tools.

Uses tmp_path + monkeypatch to inject a fresh SQLite database, so the
real ~/.friday-bp/data.db is never touched.
"""

from __future__ import annotations

import uuid
from pathlib import Path

import pytest

import server.main as main_module
import server.paths
from server.db import get_db, init_db

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _uid() -> str:
    return str(uuid.uuid4())


def seed_db(db_path: Path) -> dict:
    """Seed a small set of transactions and entries; return their IDs."""
    conn = get_db(db_path)

    # Ledgers
    ledger_a = _uid()
    ledger_b = _uid()
    conn.execute("INSERT INTO ledgers (id, name) VALUES (?, ?)", (ledger_a, "Personal"))
    conn.execute("INSERT INTO ledgers (id, name) VALUES (?, ?)", (ledger_b, "Business"))

    # Line items
    li_groceries = _uid()
    li_travel = _uid()
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
        (li_groceries, ledger_a, "Groceries", "expense"),
    )
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
        (li_travel, ledger_b, "Travel", "expense"),
    )

    # Transactions
    txn1 = _uid()
    txn2 = _uid()
    txn3 = _uid()
    conn.execute(
        "INSERT INTO transactions (id, date, merchant, amount) VALUES (?, ?, ?, ?)",
        (txn1, "2024-01-10", "Superstore", 50.00),
    )
    conn.execute(
        "INSERT INTO transactions (id, date, merchant, amount) VALUES (?, ?, ?, ?)",
        (txn2, "2024-02-15", "Air Canada", 300.00),
    )
    conn.execute(
        "INSERT INTO transactions (id, date, merchant, amount) VALUES (?, ?, ?, ?)",
        (txn3, "2024-03-20", "Amazon", 25.00),
    )

    # Transaction entries
    # entry1: ledger_a, groceries, rule, reviewed
    entry1 = _uid()
    conn.execute(
        "INSERT INTO transaction_entries "
        "(id, transaction_id, ledger_id, line_item_id, amount, source, reviewed) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (entry1, txn1, ledger_a, li_groceries, 50.00, "rule", 1),
    )
    # entry2: ledger_b, travel, llm, NOT reviewed
    entry2 = _uid()
    conn.execute(
        "INSERT INTO transaction_entries "
        "(id, transaction_id, ledger_id, line_item_id, amount, source, reviewed) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (entry2, txn2, ledger_b, li_travel, 300.00, "llm", 0),
    )
    # entry3: ledger_a, groceries, manual, NOT reviewed
    entry3 = _uid()
    conn.execute(
        "INSERT INTO transaction_entries "
        "(id, transaction_id, ledger_id, line_item_id, amount, source, reviewed) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (entry3, txn3, ledger_a, li_groceries, 25.00, "manual", 0),
    )

    conn.commit()
    conn.close()

    return {
        "ledger_a": ledger_a,
        "ledger_b": ledger_b,
        "li_groceries": li_groceries,
        "li_travel": li_travel,
        "txn1": txn1,
        "txn2": txn2,
        "txn3": txn3,
        "entry1": entry1,
        "entry2": entry2,
        "entry3": entry3,
    }


@pytest.fixture
def seeded_db(tmp_path: Path, monkeypatch):
    """Initialise + seed a temp DB and monkeypatch server.paths.DB_PATH."""
    db_path = tmp_path / "test.db"
    init_db(db_path)
    ids = seed_db(db_path)
    monkeypatch.setattr(server.paths, "DB_PATH", db_path)
    return ids


# ---------------------------------------------------------------------------
# Tests: list() with no filters
# ---------------------------------------------------------------------------


def test_list_no_filters_returns_all(seeded_db):
    result = main_module.list()
    assert "entries" in result
    assert len(result["entries"]) == 3


# ---------------------------------------------------------------------------
# Tests: list() with individual filters
# ---------------------------------------------------------------------------


def test_list_filter_date_from(seeded_db):
    result = main_module.list(filters={"date_from": "2024-02-01"})
    entries = result["entries"]
    assert len(entries) == 2
    for e in entries:
        assert e["date"] >= "2024-02-01"


def test_list_filter_date_to(seeded_db):
    result = main_module.list(filters={"date_to": "2024-02-28"})
    entries = result["entries"]
    assert len(entries) == 2
    for e in entries:
        assert e["date"] <= "2024-02-28"


def test_list_filter_date_range(seeded_db):
    result = main_module.list(filters={"date_from": "2024-02-01", "date_to": "2024-02-28"})
    entries = result["entries"]
    assert len(entries) == 1
    assert entries[0]["merchant"] == "Air Canada"


def test_list_filter_ledger_id(seeded_db):
    ids = seeded_db
    result = main_module.list(filters={"ledger_id": ids["ledger_b"]})
    entries = result["entries"]
    assert len(entries) == 1
    assert entries[0]["ledger_id"] == ids["ledger_b"]


def test_list_filter_line_item_id(seeded_db):
    ids = seeded_db
    result = main_module.list(filters={"line_item_id": ids["li_groceries"]})
    entries = result["entries"]
    assert len(entries) == 2
    for e in entries:
        assert e["line_item_id"] == ids["li_groceries"]


def test_list_filter_reviewed_true(seeded_db):
    result = main_module.list(filters={"reviewed": True})
    entries = result["entries"]
    assert len(entries) == 1
    assert entries[0]["reviewed"] == 1


def test_list_filter_reviewed_false(seeded_db):
    result = main_module.list(filters={"reviewed": False})
    entries = result["entries"]
    assert len(entries) == 2
    for e in entries:
        assert e["reviewed"] == 0


def test_list_filter_source_rule(seeded_db):
    result = main_module.list(filters={"source": "rule"})
    entries = result["entries"]
    assert len(entries) == 1
    assert entries[0]["source"] == "rule"


def test_list_filter_source_llm(seeded_db):
    result = main_module.list(filters={"source": "llm"})
    entries = result["entries"]
    assert len(entries) == 1
    assert entries[0]["source"] == "llm"


def test_list_filter_source_manual(seeded_db):
    result = main_module.list(filters={"source": "manual"})
    entries = result["entries"]
    assert len(entries) == 1
    assert entries[0]["source"] == "manual"


# ---------------------------------------------------------------------------
# Tests: get_needs_review()
# ---------------------------------------------------------------------------


def _seed_needs_review_db(db_path: Path) -> dict:
    """Seed a DB with bank infra + uncertain/unrouted entries for get_needs_review tests."""
    import time

    conn = get_db(db_path)

    user_id = _uid()
    conn.execute(
        "INSERT INTO users (id, username, password_hash, created_at) VALUES (?, ?, ?, ?)",
        (user_id, "testuser", "hash", int(time.time())),
    )
    conn_id = _uid()
    conn.execute(
        "INSERT INTO bank_connections "
        "(id, plaid_access_token_encrypted, institution_name, user_id, plaid_env) "
        "VALUES (?, ?, ?, ?, ?)",
        (conn_id, "enc", "RBC", user_id, "sandbox"),
    )
    acct_id = _uid()
    conn.execute(
        "INSERT INTO bank_accounts (id, connection_id, plaid_account_id, name) VALUES (?, ?, ?, ?)",
        (acct_id, conn_id, _uid(), "Chequing"),
    )

    # 2 uncertain transactions, 1 reviewed (should not appear)
    txn1 = _uid()
    txn2 = _uid()
    txn3 = _uid()
    for txn_id, merchant in [(txn1, "Mystery A"), (txn2, "Mystery B"), (txn3, "Known")]:
        conn.execute(
            "INSERT INTO transactions (id, bank_account_id, plaid_transaction_id, date, merchant, amount) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (txn_id, acct_id, _uid(), "2024-01-01", merchant, 10.0),
        )

    # Uncertain entry (uncertain=1, unreviewed)
    e1 = _uid()
    conn.execute(
        "INSERT INTO transaction_entries "
        "(id, transaction_id, ledger_id, line_item_id, amount, entry_type, source, "
        " confidence, uncertain, reasoning, reviewed) "
        "VALUES (?, ?, NULL, NULL, 10.0, 'spending', 'llm', 0.4, 1, 'Not sure', 0)",
        (e1, txn1),
    )
    # Unrouted entry (line_item_id IS NULL, uncertain=0 but still unrouted)
    e2 = _uid()
    conn.execute(
        "INSERT INTO transaction_entries "
        "(id, transaction_id, ledger_id, line_item_id, amount, entry_type, source, "
        " confidence, uncertain, reasoning, reviewed) "
        "VALUES (?, ?, NULL, NULL, 10.0, 'spending', 'llm', 0.5, 0, 'Unrouted', 0)",
        (e2, txn2),
    )
    # Reviewed entry (should NOT appear)
    ledger_id = _uid()
    li_id = _uid()
    conn.execute("INSERT INTO ledgers (id, name) VALUES (?, ?)", (ledger_id, "Household"))
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name) VALUES (?, ?, ?)",
        (li_id, ledger_id, "Groceries"),
    )
    e3 = _uid()
    conn.execute(
        "INSERT INTO transaction_entries "
        "(id, transaction_id, ledger_id, line_item_id, amount, entry_type, source, "
        " confidence, uncertain, reviewed) "
        "VALUES (?, ?, ?, ?, 10.0, 'spending', 'llm', 0.95, 1, 1)",
        (e3, txn3, ledger_id, li_id),
    )

    conn.commit()
    conn.close()
    return {"user_id": user_id}


@pytest.fixture
def needs_review_db(tmp_path: Path, monkeypatch):
    """DB seeded with uncertain/unrouted entries for get_needs_review tests."""
    db_path = tmp_path / "nr_test.db"
    init_db(db_path)
    ids = _seed_needs_review_db(db_path)
    monkeypatch.setattr(server.paths, "DB_PATH", db_path)
    monkeypatch.setattr("server.main.get_active_user_id", lambda _: ids["user_id"])
    return ids


def test_get_needs_review_returns_only_unreviewed(needs_review_db):
    """get_needs_review returns uncertain + unrouted transactions, not reviewed ones."""
    result = main_module.get_needs_review()
    assert "transactions" in result
    transactions = result["transactions"]
    assert len(transactions) == 2


def test_get_needs_review_shape(needs_review_db):
    """Each transaction must have the expected fields."""
    result = main_module.get_needs_review()
    transactions = result["transactions"]
    assert len(transactions) > 0
    required_fields = {
        "id",
        "merchant",
        "amount",
        "date",
        "account_name",
        "reasoning",
    }
    for txn in transactions:
        assert required_fields.issubset(
            txn.keys()
        ), f"Missing fields: {required_fields - txn.keys()}"
