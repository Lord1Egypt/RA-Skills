"""
tests/test_account_description.py — Tests for #127: account descriptions.

Covers:
  - set_account_description MCP tool (returns {"status": "ok", "account_id": ...})
  - description persists in DB
  - description appears in classification prompt when non-null
  - description absent → no change to classification prompt
  - schema migration: existing DBs without description column get it via init_db
"""

from __future__ import annotations

import json
import sqlite3
import uuid
from unittest.mock import patch

import pytest

import server.paths
from server.db import get_db, init_db

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def db_path(tmp_path, monkeypatch):
    """Fresh DB with monkeypatched server.paths.DB_PATH."""
    path = tmp_path / "data.db"
    init_db(path)
    monkeypatch.setattr(server.paths, "DB_PATH", path)
    return path


@pytest.fixture
def db_with_account(db_path):
    """Insert a bank_connection + bank_account; return (db_path, conn_id, acct_id)."""
    conn_id = str(uuid.uuid4())
    acct_id = str(uuid.uuid4())
    conn = get_db(db_path)
    conn.execute(
        "INSERT INTO bank_connections (id, plaid_item_id, plaid_access_token_encrypted, institution_name)"
        " VALUES (?, ?, ?, ?)",
        (conn_id, "item-1", "enc-token", "Test Bank"),
    )
    conn.execute(
        "INSERT INTO bank_accounts (id, connection_id, plaid_account_id, name, type)"
        " VALUES (?, ?, ?, ?, ?)",
        (acct_id, conn_id, "plaid-acct-1", "Chequing", "depository"),
    )
    conn.commit()
    conn.close()
    return db_path, conn_id, acct_id


# ---------------------------------------------------------------------------
# MCP tool: set_account_description
# ---------------------------------------------------------------------------


def test_set_account_description_ok(db_with_account):
    """set_account_description returns {'status': 'ok', 'account_id': ...}."""
    from server.main import set_account_description

    db_path, conn_id, acct_id = db_with_account

    result = set_account_description(account_id=acct_id, description="Day-to-day spending")

    assert result["status"] == "ok"
    assert result["account_id"] == acct_id


def test_set_account_description_persists(db_with_account):
    """Description is actually written to the DB."""
    from server.main import set_account_description

    db_path, conn_id, acct_id = db_with_account

    set_account_description(account_id=acct_id, description="Business card")

    conn = get_db(db_path)
    row = conn.execute("SELECT description FROM bank_accounts WHERE id = ?", (acct_id,)).fetchone()
    conn.close()

    assert row is not None
    assert row["description"] == "Business card"


def test_set_account_description_unknown_id(db_path):
    """Returns error status when account_id is not found."""
    from server.main import set_account_description

    result = set_account_description(account_id="nonexistent-id", description="X")

    assert result["status"] == "error"


def test_set_account_description_overwrite(db_with_account):
    """Calling set_account_description twice updates the value."""
    from server.main import set_account_description

    db_path, conn_id, acct_id = db_with_account

    set_account_description(account_id=acct_id, description="First")
    set_account_description(account_id=acct_id, description="Second")

    conn = get_db(db_path)
    row = conn.execute("SELECT description FROM bank_accounts WHERE id = ?", (acct_id,)).fetchone()
    conn.close()

    assert row["description"] == "Second"


# ---------------------------------------------------------------------------
# Classification context: description present
# ---------------------------------------------------------------------------


def _make_transaction(acct_id: str) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "merchant": "ACME Corp",
        "amount": 42.00,
        "date": "2025-01-15",
        "bank_account_id": acct_id,
    }


def _setup_ledger(conn) -> str:
    """Insert a ledger + line item; return the line_item id."""
    ledger_id = str(uuid.uuid4())
    li_id = str(uuid.uuid4())
    conn.execute("INSERT INTO ledgers (id, name) VALUES (?, ?)", (ledger_id, "Personal"))
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name) VALUES (?, ?, ?)",
        (li_id, ledger_id, "Misc"),
    )
    conn.commit()
    return li_id


def test_classification_prompt_includes_account_description(db_with_account):
    """When a description is set, 'Account Context' appears in the LLM prompt."""
    import server.classifier as clf

    db_path, conn_id, acct_id = db_with_account
    conn = get_db(db_path)

    # Set a description
    conn.execute(
        "UPDATE bank_accounts SET description = ? WHERE id = ?",
        ("Day-to-day spending", acct_id),
    )
    li_id = _setup_ledger(conn)

    captured: list[dict] = []

    def fake_chat(messages, temperature=0.0):
        captured.extend(messages)
        return json.dumps({"line_item_id": li_id, "confidence": 0.9, "reasoning": "test"})

    with patch("server.llm.chat", side_effect=fake_chat):
        clf.classify_with_llm(conn, _make_transaction(acct_id))

    conn.close()

    user_content = next(m["content"] for m in captured if m["role"] == "user")
    assert "Account Context" in user_content
    assert "Day-to-day spending" in user_content


def test_classification_prompt_no_account_description(db_with_account):
    """When no description is set, 'Account Context' is absent from the prompt."""
    import server.classifier as clf

    db_path, conn_id, acct_id = db_with_account
    conn = get_db(db_path)
    li_id = _setup_ledger(conn)

    captured: list[dict] = []

    def fake_chat(messages, temperature=0.0):
        captured.extend(messages)
        return json.dumps({"line_item_id": li_id, "confidence": 0.9, "reasoning": "test"})

    with patch("server.llm.chat", side_effect=fake_chat):
        clf.classify_with_llm(conn, _make_transaction(acct_id))

    conn.close()

    user_content = next(m["content"] for m in captured if m["role"] == "user")
    assert "Account Context" not in user_content


def test_classification_prompt_no_bank_account_id(db_with_account):
    """When transaction has no bank_account_id, 'Account Context' is absent."""
    import server.classifier as clf

    db_path, conn_id, acct_id = db_with_account
    conn = get_db(db_path)
    li_id = _setup_ledger(conn)

    captured: list[dict] = []

    def fake_chat(messages, temperature=0.0):
        captured.extend(messages)
        return json.dumps({"line_item_id": li_id, "confidence": 0.9, "reasoning": "test"})

    txn = {
        "id": str(uuid.uuid4()),
        "merchant": "Shop",
        "amount": 10.00,
        "date": "2025-01-15",
        # No bank_account_id key
    }

    with patch("server.llm.chat", side_effect=fake_chat):
        clf.classify_with_llm(conn, txn)

    conn.close()

    user_content = next(m["content"] for m in captured if m["role"] == "user")
    assert "Account Context" not in user_content


# ---------------------------------------------------------------------------
# Schema migration: description column on existing DBs
# ---------------------------------------------------------------------------


def test_init_db_adds_description_column_to_existing_db(tmp_path):
    """init_db migration adds description column if it doesn't exist."""
    db_path = tmp_path / "old.db"

    # Simulate an old DB without description column
    conn = sqlite3.connect(str(db_path))
    conn.execute(
        "CREATE TABLE bank_accounts ("
        "  id TEXT PRIMARY KEY,"
        "  connection_id TEXT,"
        "  plaid_account_id TEXT UNIQUE,"
        "  name TEXT, mask TEXT, type TEXT, subtype TEXT"
        ")"
    )
    conn.commit()
    conn.close()

    # Running init_db should add the column via migration
    init_db(db_path)

    conn = sqlite3.connect(str(db_path))
    cols = {row[1] for row in conn.execute("PRAGMA table_info(bank_accounts)")}
    conn.close()

    assert "description" in cols
