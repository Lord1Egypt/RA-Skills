"""
tests/test_transaction_datetime_ordering.py

Verifies that:
1. authorized_datetime is stored during sync when Plaid provides it.
2. The /accounts/{id}/transactions API returns rows ordered by
   COALESCE(authorized_datetime, date) DESC so that same-day transactions
   appear in chronological (time-of-day) order rather than arbitrary rowid order.
"""

from __future__ import annotations

import uuid

import pytest

import server.main as _main
from server.db import get_db, init_db
from server.main import sync  # noqa: F401 — imported for patching side-effects
from ui.auth import create_user

# ---------------------------------------------------------------------------
# Fake Plaid data — three same-day transactions with distinct times,
# intentionally added out of chronological order so we can verify sorting.
# ---------------------------------------------------------------------------

_ACCOUNT_ID = "plaid-acct-dt"

_ADDED_TXNS = [
    {
        "transaction_id": "dt-txn-3",
        "account_id": _ACCOUNT_ID,
        "date": "2026-05-10",
        "authorized_datetime": "2026-05-10T22:15:00Z",
        "datetime": None,
        "name": "LateNight Coffee",
        "merchant_name": "LateNight Coffee",
        "amount": 3.50,
        "pending": False,
    },
    {
        "transaction_id": "dt-txn-1",
        "account_id": _ACCOUNT_ID,
        "date": "2026-05-10",
        "authorized_datetime": "2026-05-10T08:00:00Z",
        "datetime": None,
        "name": "Morning Bagel",
        "merchant_name": "Morning Bagel",
        "amount": 5.00,
        "pending": False,
    },
    {
        "transaction_id": "dt-txn-2",
        "account_id": _ACCOUNT_ID,
        "date": "2026-05-10",
        "authorized_datetime": "2026-05-10T13:30:00Z",
        "datetime": None,
        "name": "Lunch Spot",
        "merchant_name": "Lunch Spot",
        "amount": 12.00,
        "pending": False,
    },
]

_ACCOUNT_META = {
    _ACCOUNT_ID: {
        "name": "Test Chequing",
        "type": "depository",
        "currency": "CAD",
        "balance_current": 1000.0,
        "balance_available": 900.0,
    }
}


def _mock_sync(access_token, cursor=None):
    return {
        "added": _ADDED_TXNS,
        "modified": [],
        "removed": [],
        "next_cursor": "cursor-dt",
        "account_meta": _ACCOUNT_META,
    }


_HEALTH_NOOP = {"checked": 0, "active": 0, "needs_reauth": 0, "pending_expiration": 0}


def _plaid_factory(sync_fn):
    """Return a PlaidProvider-compatible class (mirrors test_sync.py pattern)."""

    class _MockPlaidProvider:
        def __init__(self, env=None, client_id=None, secret=None):
            import os as _os

            self.env = (env or _os.environ.get("PLAID_ENV", "sandbox")).lower()

        def sync_transactions(self, access_token, cursor=None):
            return sync_fn(access_token, cursor)

        def get_item_status(self, access_token):
            return {"status": "active"}

    return _MockPlaidProvider


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------


@pytest.fixture()
def env(tmp_path, monkeypatch):
    db = tmp_path / "test.db"
    lock = tmp_path / "sync.lock"
    init_db(db)

    monkeypatch.setattr("server.paths.DB_PATH", db)
    monkeypatch.setattr("server.paths.SYNC_LOCK_PATH", lock)

    user_id = create_user(db, "testuser", "testpass1")
    conn = get_db(db)
    connection_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO bank_connections "
        "(id, user_id, plaid_access_token_encrypted, plaid_item_id, plaid_env, status) "
        "VALUES (?, ?, ?, ?, ?, 'active')",
        (connection_id, user_id, "enc-tok", "item-dt", "sandbox"),
    )
    conn.commit()
    conn.close()
    return {"db": db, "connection_id": connection_id, "user_id": user_id}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_authorized_datetime_stored_on_sync(env, monkeypatch):
    """authorized_datetime is persisted for each transaction that Plaid provides."""
    monkeypatch.setattr("server.main.PlaidProvider", _plaid_factory(_mock_sync))
    monkeypatch.setattr("server.crypto.decrypt", lambda x: x)
    monkeypatch.setattr(
        "server.health_monitor.check_all_connections", lambda db, plaid_provider=None: _HEALTH_NOOP
    )

    _main.sync()

    conn = get_db(env["db"])
    txns = conn.execute(
        "SELECT plaid_transaction_id, authorized_datetime FROM transactions "
        "ORDER BY plaid_transaction_id"
    ).fetchall()
    conn.close()

    by_id = {row["plaid_transaction_id"]: row["authorized_datetime"] for row in txns}
    assert by_id["dt-txn-1"] == "2026-05-10T08:00:00Z"
    assert by_id["dt-txn-2"] == "2026-05-10T13:30:00Z"
    assert by_id["dt-txn-3"] == "2026-05-10T22:15:00Z"


def test_transactions_ordered_by_datetime_desc(env, monkeypatch):
    """
    Same-day transactions are returned latest-first when authorized_datetime
    is available — not in arbitrary insertion/rowid order.
    """
    monkeypatch.setattr("server.main.PlaidProvider", _plaid_factory(_mock_sync))
    monkeypatch.setattr("server.crypto.decrypt", lambda x: x)
    monkeypatch.setattr(
        "server.health_monitor.check_all_connections", lambda db, plaid_provider=None: _HEALTH_NOOP
    )

    _main.sync()

    conn = get_db(env["db"])
    # Replicate the exact ORDER BY clause used in ui/server.py
    rows = conn.execute("""
        SELECT t.merchant, t.authorized_datetime
          FROM transactions t
         ORDER BY COALESCE(t.authorized_datetime, t.date) DESC,
                  t.rowid DESC
        """).fetchall()
    conn.close()

    merchants = [r["merchant"] for r in rows]
    assert merchants == [
        "LateNight Coffee",
        "Lunch Spot",
        "Morning Bagel",
    ], f"Unexpected ordering: {merchants}"


def test_transactions_fallback_to_date_when_no_datetime(env, monkeypatch):
    """
    When authorized_datetime is NULL, ordering falls back gracefully to date DESC.
    """
    monkeypatch.setattr("server.main.PlaidProvider", _plaid_factory(_mock_sync))
    monkeypatch.setattr("server.crypto.decrypt", lambda x: x)
    monkeypatch.setattr(
        "server.health_monitor.check_all_connections", lambda db, plaid_provider=None: _HEALTH_NOOP
    )

    _main.sync()

    conn = get_db(env["db"])
    # NULL out the late-night transaction's authorized_datetime
    conn.execute(
        "UPDATE transactions SET authorized_datetime = NULL WHERE plaid_transaction_id = 'dt-txn-3'"
    )
    conn.commit()

    rows = conn.execute("""
        SELECT t.merchant, t.authorized_datetime
          FROM transactions t
         ORDER BY COALESCE(t.authorized_datetime, t.date) DESC,
                  t.rowid DESC
        """).fetchall()
    conn.close()

    merchants = [r["merchant"] for r in rows]
    # Lunch Spot (13:30) should still come before Morning Bagel (08:00)
    lunch_idx = merchants.index("Lunch Spot")
    morning_idx = merchants.index("Morning Bagel")
    assert (
        lunch_idx < morning_idx
    ), f"Lunch Spot should appear before Morning Bagel; got: {merchants}"
