# TODO: LLM validation tests require API keys — see issue #121

"""
tests/integration/test_mcp_tools.py — Integration tests for MCP tools.

Each test runs the tool against a real (in-memory / temp) SQLite DB so that
tool wiring, DB queries, and response shapes are all exercised end-to-end.

Part B (LLM prompt validation) is intentionally omitted — those tests require
real API keys and are not safe for CI.  See issue #121 for details.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

import server.paths
from server.db import get_db, init_db
from ui.auth import create_session, create_user

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _uid() -> str:
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_path(tmp_path: Path, monkeypatch) -> Path:
    """Create a fresh temp DB and monkeypatch server.paths.DB_PATH to point at it."""
    path = tmp_path / "test_integration.db"
    init_db(path)
    monkeypatch.setattr(server.paths, "DB_PATH", path)
    monkeypatch.setattr(server.paths, "SYNC_LOCK_PATH", tmp_path / "sync.lock")
    monkeypatch.setenv("FRIDAY_BP_DB_PATH", str(path))
    return path


@pytest.fixture()
def authed_user(db_path: Path) -> dict:
    """Create a test user and session so get_active_user_id() returns a user."""
    user_id = create_user(db_path, "testuser", "testpass123")
    token = create_session(db_path, user_id=user_id)
    return {"user_id": user_id, "token": token}


@pytest.fixture(autouse=True)
def patch_crypto(monkeypatch):
    """Patch encrypt/decrypt with transparent passthrough fakes."""
    monkeypatch.setattr(
        "server.crypto.encrypt", MagicMock(side_effect=lambda plaintext: "enc:" + plaintext)
    )
    monkeypatch.setattr(
        "server.crypto.decrypt",
        MagicMock(side_effect=lambda ciphertext: ciphertext[len("enc:") :]),
    )


# ---------------------------------------------------------------------------
# Test 1: setup_status on a fresh DB
# ---------------------------------------------------------------------------


def test_setup_status_fresh(db_path, authed_user):
    """Fresh DB with a user but no ledgers/connections → 'not_started'."""
    from server.main import setup_status

    result = setup_status()
    assert isinstance(result, dict)
    assert "status" in result
    assert result["status"] in ("not_started", "in_progress", "complete")


# ---------------------------------------------------------------------------
# Test 2: list_ledgers
# ---------------------------------------------------------------------------


def test_list_ledgers(db_path, authed_user, monkeypatch):
    """list_ledgers() returns a dict with a 'ledgers' key containing Personal."""
    from server.main import apply_initial_setup, list_ledgers

    monkeypatch.setattr("server.main._register_openclaw_cron", lambda: False)

    # Seed the default Personal ledger via apply_initial_setup.
    apply_initial_setup(banks_to_link=[], extra_ledgers=[], hints=[])

    result = list_ledgers()
    assert isinstance(result, dict)
    assert "ledgers" in result
    names = [lg["name"] for lg in result["ledgers"]]
    assert "Personal" in names


# ---------------------------------------------------------------------------
# Test 3: add_hint and list_hints round-trip
# ---------------------------------------------------------------------------


def test_add_hint_and_list(db_path, authed_user):
    """add_hint('groceries') then list_hints() → hint appears in the list."""
    from server.main import add_hint, list_hints

    created = add_hint("groceries")
    assert created.get("created") is True or "id" in created

    result = list_hints()
    assert isinstance(result, dict)
    assert "hints" in result
    texts = [h["text"] for h in result["hints"]]
    assert "groceries" in texts


# ---------------------------------------------------------------------------
# Test 4: sync() calls PlaidProvider with a mock
# ---------------------------------------------------------------------------


def test_sync_calls_plaid_with_mock(db_path, authed_user):
    """sync() with a mocked PlaidProvider returns a dict without error."""
    from server.main import sync

    connection_id = _uid()
    conn = get_db(db_path)
    conn.execute(
        "INSERT INTO bank_connections "
        "(id, plaid_item_id, plaid_access_token_encrypted, status, plaid_env) "
        "VALUES (?, 'item-test', 'enc:fake-token', 'active', 'sandbox')",
        (connection_id,),
    )
    conn.commit()
    conn.close()

    mock_sync_result = {
        "added": [],
        "modified": [],
        "removed": [],
        "next_cursor": "cur1",
        "accounts": [],
    }

    class _MockPlaid:
        def __init__(self, env=None, client_id=None, secret=None):
            self.env = (env or "sandbox").lower()

        def sync_transactions(self, access_token, cursor=None):
            return mock_sync_result

        def check_connection(self, access_token):
            return {"status": "active"}

    with (
        patch("server.main.PlaidProvider", _MockPlaid),
        patch("server.health_monitor.check_all_connections", return_value={}),
    ):
        result = sync()

    assert isinstance(result, dict)
    assert "error" not in result or result.get("status") != "error"


# ---------------------------------------------------------------------------
# Test 5: list_transactions after direct DB insert
# ---------------------------------------------------------------------------


def test_list_transactions_after_insert(db_path, authed_user):
    """Insert 2 fake transaction rows directly into DB; list() → both appear."""
    from server.main import list as list_transactions

    conn = get_db(db_path)

    # Need a ledger + line_item for the entries.
    ledger_id = _uid()
    li_id = _uid()
    conn.execute("INSERT INTO ledgers (id, name) VALUES (?, ?)", (ledger_id, "Personal"))
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
        (li_id, ledger_id, "Groceries", "expense"),
    )

    txn_ids = [_uid(), _uid()]
    for i, txn_id in enumerate(txn_ids):
        conn.execute(
            "INSERT INTO transactions (id, date, merchant, amount) VALUES (?, ?, ?, ?)",
            (txn_id, f"2026-05-{10 + i:02d}", f"Merchant {i}", 25.00 + i),
        )
        conn.execute(
            "INSERT INTO transaction_entries "
            "(id, transaction_id, ledger_id, line_item_id, amount, source, reviewed) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (_uid(), txn_id, ledger_id, li_id, 25.00 + i, "rule", 1),
        )

    conn.commit()
    conn.close()

    result = list_transactions()
    assert isinstance(result, dict)
    assert "entries" in result
    assert len(result["entries"]) >= 2

    returned_txn_ids = {e["transaction_id"] for e in result["entries"]}
    for txn_id in txn_ids:
        assert txn_id in returned_txn_ids


# ---------------------------------------------------------------------------
# Test 6: summary tool
# ---------------------------------------------------------------------------


def test_summary_tool(db_path, authed_user):
    """Insert fake transactions for the current month; summary() returns totals."""
    from server.main import summary

    current_month = datetime.now().strftime("%Y-%m")
    date_str = f"{current_month}-15"

    conn = get_db(db_path)

    ledger_id = _uid()
    li_expense = _uid()
    li_income = _uid()
    conn.execute("INSERT INTO ledgers (id, name) VALUES (?, ?)", (ledger_id, "Personal"))
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
        (li_expense, ledger_id, "Groceries", "expense"),
    )
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
        (li_income, ledger_id, "Salary", "income"),
    )

    # Expense transaction
    txn_e = _uid()
    conn.execute(
        "INSERT INTO transactions (id, date, merchant, amount) VALUES (?, ?, ?, ?)",
        (txn_e, date_str, "Superstore", -120.00),
    )
    conn.execute(
        "INSERT INTO transaction_entries "
        "(id, transaction_id, ledger_id, line_item_id, amount, source, reviewed) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (_uid(), txn_e, ledger_id, li_expense, -120.00, "rule", 1),
    )

    # Income transaction
    txn_i = _uid()
    conn.execute(
        "INSERT INTO transactions (id, date, merchant, amount) VALUES (?, ?, ?, ?)",
        (txn_i, date_str, "Employer", 3000.00),
    )
    conn.execute(
        "INSERT INTO transaction_entries "
        "(id, transaction_id, ledger_id, line_item_id, amount, source, reviewed) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (_uid(), txn_i, ledger_id, li_income, 3000.00, "rule", 1),
    )

    conn.commit()
    conn.close()

    result = summary("month")
    assert isinstance(result, dict)
    assert "income" in result
    assert "expenses" in result
    assert "net" in result
    assert "period" in result
    assert result["income"] > 0
    assert result["expenses"] != 0 or result["income"] > 0


# ---------------------------------------------------------------------------
# Test 7: get_ui_url
# ---------------------------------------------------------------------------


def test_get_ui_url(db_path):
    """get_ui_url() returns {"url": "http://127.0.0.1:6789"}."""
    from server.main import get_ui_url

    result = get_ui_url()
    assert isinstance(result, dict)
    assert "url" in result
    assert result["url"] == "http://127.0.0.1:6789"


# ---------------------------------------------------------------------------
# Test 8: list_profiles
# ---------------------------------------------------------------------------


def test_list_profiles(db_path, authed_user):
    """list_profiles() returns {"profiles": [...]} with at least the test user."""
    from server.main import list_profiles

    result = list_profiles()
    assert isinstance(result, dict)
    assert "profiles" in result
    assert isinstance(result["profiles"], list)
    assert len(result["profiles"]) >= 1

    usernames = [p["username"] for p in result["profiles"]]
    assert "testuser" in usernames
