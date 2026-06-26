"""
tests/test_multi_currency.py — Tests for issue #160: multi-currency foundation.

Covers:
  - Schema: currency columns exist on bank_accounts and transactions
  - format_amount() helper function
  - accounts.html renders currency prefix on balances
  - After sync mock, bank_accounts.currency is populated
"""

from __future__ import annotations

import uuid
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_path(tmp_path: Path, monkeypatch) -> Path:
    """Initialise a fresh SQLite DB and monkeypatch DB_PATH."""
    import server.paths as paths
    from server.db import init_db

    db = tmp_path / "test.db"
    init_db(db)

    monkeypatch.setattr(paths, "DB_PATH", db)
    monkeypatch.setattr(paths, "APP_DIR", tmp_path)
    return db


@pytest.fixture()
def authed_user(db_path: Path):
    """Return (db_path, user_id) after creating a test user."""
    from ui.auth import create_user

    uid = create_user(db_path, "testuser", "testpassword123")
    return db_path, uid


# ---------------------------------------------------------------------------
# Schema tests
# ---------------------------------------------------------------------------


def test_bank_accounts_has_currency_column(db_path: Path):
    """bank_accounts.currency column exists after init_db."""
    import sqlite3

    conn = sqlite3.connect(str(db_path))
    cols = {row[1] for row in conn.execute("PRAGMA table_info(bank_accounts)")}
    conn.close()
    assert "currency" in cols, "bank_accounts.currency column missing"


def test_transactions_has_currency_column(db_path: Path):
    """transactions.currency column exists after init_db."""
    import sqlite3

    conn = sqlite3.connect(str(db_path))
    cols = {row[1] for row in conn.execute("PRAGMA table_info(transactions)")}
    conn.close()
    assert "currency" in cols, "transactions.currency column missing"


# ---------------------------------------------------------------------------
# format_amount tests
# ---------------------------------------------------------------------------


def test_format_amount_cad():
    from server.currency import format_amount

    assert format_amount(500, "CAD") == "C$500.00"


def test_format_amount_usd():
    from server.currency import format_amount

    assert format_amount(500, "USD") == "US$500.00"


def test_format_amount_none():
    from server.currency import format_amount

    assert format_amount(None, "CAD") == "\u2014"


def test_format_amount_eur():
    from server.currency import format_amount

    assert format_amount(1234.56, "EUR") == "\u20ac1,234.56"


def test_format_amount_gbp():
    from server.currency import format_amount

    assert format_amount(99.99, "GBP") == "\xa399.99"


def test_format_amount_unknown_currency():
    from server.currency import format_amount

    result = format_amount(100, "JPY")
    assert result == "JPY 100.00"


def test_format_amount_large_number():
    from server.currency import format_amount

    assert format_amount(1234.56, "CAD") == "C$1,234.56"


# ---------------------------------------------------------------------------
# accounts.html — currency prefix in balance display
# ---------------------------------------------------------------------------


def test_accounts_html_renders_cad_prefix(authed_user):
    """GET /accounts shows C$ prefix for CAD accounts."""
    db_path, user_id = authed_user
    from fastapi.testclient import TestClient

    from server.db import get_db
    from ui.auth import SESSION_COOKIE, create_session
    from ui.server import app

    # Insert a bank connection + account with CAD currency
    conn_id = str(uuid.uuid4())
    acct_id = str(uuid.uuid4())
    db = get_db(db_path)
    db.execute(
        "INSERT INTO bank_connections (id, plaid_item_id, plaid_access_token_encrypted,"
        " institution_name, status, user_id, plaid_env)"
        " VALUES (?, ?, ?, ?, 'active', ?, 'sandbox')",
        (conn_id, "item-cad", "enc-cad", "Test Bank CAD", user_id),
    )
    db.execute(
        "INSERT INTO bank_accounts (id, connection_id, plaid_account_id, name,"
        " type, currency, balance_current)"
        " VALUES (?, ?, ?, ?, 'depository', 'CAD', 1234.56)",
        (acct_id, conn_id, "plaid-cad-acct", "Chequing"),
    )
    db.commit()
    db.close()

    token = create_session(db_path, user_agent="pytest", user_id=user_id)
    client = TestClient(app, follow_redirects=False)
    client.cookies.set(SESSION_COOKIE, token)

    resp = client.get("/accounts")
    assert resp.status_code == 200
    assert "C$" in resp.text, "Expected C$ prefix on CAD balance"
    assert "1234.56" in resp.text


def test_accounts_html_renders_usd_prefix(authed_user):
    """GET /accounts shows US$ prefix for USD accounts."""
    db_path, user_id = authed_user
    from fastapi.testclient import TestClient

    from server.db import get_db
    from ui.auth import SESSION_COOKIE, create_session
    from ui.server import app

    conn_id = str(uuid.uuid4())
    acct_id = str(uuid.uuid4())
    db = get_db(db_path)
    db.execute(
        "INSERT INTO bank_connections (id, plaid_item_id, plaid_access_token_encrypted,"
        " institution_name, status, user_id, plaid_env)"
        " VALUES (?, ?, ?, ?, 'active', ?, 'sandbox')",
        (conn_id, "item-usd", "enc-usd", "US Bank", user_id),
    )
    db.execute(
        "INSERT INTO bank_accounts (id, connection_id, plaid_account_id, name,"
        " type, currency, balance_current)"
        " VALUES (?, ?, ?, ?, 'depository', 'USD', 500.00)",
        (acct_id, conn_id, "plaid-usd-acct", "Savings USD"),
    )
    db.commit()
    db.close()

    token = create_session(db_path, user_agent="pytest", user_id=user_id)
    client = TestClient(app, follow_redirects=False)
    client.cookies.set(SESSION_COOKIE, token)

    resp = client.get("/accounts")
    assert resp.status_code == 200
    assert "US$" in resp.text, "Expected US$ prefix on USD balance"


# ---------------------------------------------------------------------------
# Sync mock: bank_accounts.currency populated from Plaid
# ---------------------------------------------------------------------------


def test_sync_populates_bank_account_currency(db_path: Path, monkeypatch):
    """After a sync with mocked Plaid, bank_accounts.currency reflects iso_currency_code."""
    import server.paths as paths
    from server.db import get_db

    monkeypatch.setattr(paths, "DB_PATH", db_path)

    # Insert a bank connection
    conn_id = str(uuid.uuid4())
    db = get_db(db_path)
    db.execute(
        "INSERT INTO bank_connections (id, plaid_item_id, plaid_access_token_encrypted,"
        " institution_name, status, plaid_env)"
        " VALUES (?, ?, ?, ?, 'active', 'sandbox')",
        (conn_id, "item-test", "enc-token", "Mock Bank"),
    )
    db.execute(
        "INSERT INTO sync_cursors (connection_id, cursor) VALUES (?, NULL)",
        (conn_id,),
    )
    db.commit()
    db.close()

    plaid_account_id = "plaid-acct-usd"
    plaid_txn_id = "plaid-txn-001"

    mock_sync_result = {
        "added": [
            {
                "account_id": plaid_account_id,
                "transaction_id": plaid_txn_id,
                "date": "2024-01-15",
                "name": "Coffee Shop",
                "merchant_name": "Coffee Shop",
                "amount": 5.50,
                "pending": False,
            }
        ],
        "modified": [],
        "removed": [],
        "next_cursor": "cursor-v2",
        "accounts": [
            {
                "account_id": plaid_account_id,
                "name": "USD Chequing",
                "official_name": "USD Chequing Account",
                "type": "depository",
                "balances": {
                    "iso_currency_code": "USD",
                    "current": 1000.0,
                    "available": 950.0,
                },
            }
        ],
    }

    mock_provider = MagicMock()
    mock_provider.sync_transactions.return_value = mock_sync_result
    mock_provider.env = "sandbox"

    with patch("server.main.PlaidProvider", return_value=mock_provider):
        with patch("server.crypto.decrypt", return_value="fake-access-token"):
            from server.main import sync

            sync()

    db = get_db(db_path)
    row = db.execute(
        "SELECT currency FROM bank_accounts WHERE plaid_account_id = ?",
        (plaid_account_id,),
    ).fetchone()
    db.close()

    assert row is not None, "bank_accounts row not found after sync"
    assert row["currency"] == "USD", f"Expected USD, got {row['currency']}"


def test_sync_populates_transaction_currency(db_path: Path, monkeypatch):
    """After a sync with mocked Plaid, transactions.currency matches the account's currency."""
    import server.paths as paths
    from server.db import get_db

    monkeypatch.setattr(paths, "DB_PATH", db_path)

    conn_id = str(uuid.uuid4())
    db = get_db(db_path)
    db.execute(
        "INSERT INTO bank_connections (id, plaid_item_id, plaid_access_token_encrypted,"
        " institution_name, status, plaid_env)"
        " VALUES (?, ?, ?, ?, 'active', 'sandbox')",
        (conn_id, "item-test2", "enc-token2", "Mock Bank 2"),
    )
    db.execute(
        "INSERT INTO sync_cursors (connection_id, cursor) VALUES (?, NULL)",
        (conn_id,),
    )
    db.commit()
    db.close()

    plaid_account_id = "plaid-acct-gbp"
    plaid_txn_id = "plaid-txn-gbp-001"

    mock_sync_result = {
        "added": [
            {
                "account_id": plaid_account_id,
                "transaction_id": plaid_txn_id,
                "date": "2024-02-10",
                "name": "London Pub",
                "merchant_name": "London Pub",
                "amount": 12.50,
                "pending": False,
            }
        ],
        "modified": [],
        "removed": [],
        "next_cursor": "cursor-gbp-2",
        "accounts": [
            {
                "account_id": plaid_account_id,
                "name": "GBP Account",
                "official_name": None,
                "type": "depository",
                "balances": {
                    "iso_currency_code": "GBP",
                    "current": 500.0,
                    "available": 490.0,
                },
            }
        ],
    }

    mock_provider = MagicMock()
    mock_provider.sync_transactions.return_value = mock_sync_result
    mock_provider.env = "sandbox"

    with patch("server.main.PlaidProvider", return_value=mock_provider):
        with patch("server.crypto.decrypt", return_value="fake-access-token"):
            from server.main import sync

            sync()

    db = get_db(db_path)
    row = db.execute(
        "SELECT currency FROM transactions WHERE plaid_transaction_id = ?",
        (plaid_txn_id,),
    ).fetchone()
    db.close()

    assert row is not None, "transactions row not found after sync"
    assert row["currency"] == "GBP", f"Expected GBP, got {row['currency']}"
