"""
tests/test_transfer_detection.py — Tests for server/transfer_detect.py.

Covers:
- detect_internal_transfers: basic match (same amount, different accounts, within 3 days)
- detect_internal_transfers: amount tolerance within $0.01 → still detected
- detect_internal_transfers: more than 3 days apart → NOT detected
- detect_internal_transfers: same account → NOT detected
- detect_internal_transfers: different users → NOT detected
- is_investment_account: returns True for Wealthsimple, False for RBC Royal Bank
- get_transfer_hint: returns proper hint dict for a matching tx, None otherwise
"""

from __future__ import annotations

import sqlite3
import uuid
from pathlib import Path

import pytest

from server.db import get_db, init_db
from server.transfer_detect import (
    detect_internal_transfers,
    get_transfer_hint,
    is_investment_account,
)

# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def tmp_db(tmp_path: Path):
    """Return a fresh initialised DB path."""
    db_file = tmp_path / "test.db"
    init_db(db_file)
    return db_file


def _new_id() -> str:
    return str(uuid.uuid4())


def _seed_user(conn: sqlite3.Connection) -> str:
    """Insert a user and return their id."""
    import time

    user_id = _new_id()
    conn.execute(
        "INSERT INTO users (id, username, password_hash, created_at) VALUES (?, ?, ?, ?)",
        (user_id, f"user_{user_id[:8]}", "hash", int(time.time())),
    )
    conn.commit()
    return user_id


def _seed_connection(conn: sqlite3.Connection, user_id: str, institution_name: str = "RBC") -> str:
    """Insert a bank_connection and return its id."""

    conn_id = _new_id()
    conn.execute(
        "INSERT INTO bank_connections "
        "(id, plaid_access_token_encrypted, institution_name, user_id, plaid_env) "
        "VALUES (?, ?, ?, ?, ?)",
        (conn_id, "enc_token", institution_name, user_id, "sandbox"),
    )
    conn.commit()
    return conn_id


def _seed_account(conn: sqlite3.Connection, connection_id: str) -> str:
    """Insert a bank_account and return its id."""
    acct_id = _new_id()
    conn.execute(
        "INSERT INTO bank_accounts (id, connection_id, plaid_account_id, name, type) "
        "VALUES (?, ?, ?, ?, ?)",
        (acct_id, connection_id, _new_id(), "Chequing", "depository"),
    )
    conn.commit()
    return acct_id


def _seed_transaction(
    conn: sqlite3.Connection,
    bank_account_id: str,
    amount: float,
    date: str,
    pending: int = 0,
) -> str:
    """Insert a transaction and return its id."""
    tx_id = _new_id()
    conn.execute(
        "INSERT INTO transactions "
        "(id, bank_account_id, plaid_transaction_id, date, merchant, amount, pending) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (tx_id, bank_account_id, _new_id(), date, "Transfer", amount, pending),
    )
    conn.commit()
    return tx_id


# ---------------------------------------------------------------------------
# detect_internal_transfers tests
# ---------------------------------------------------------------------------


def test_basic_transfer_detected(tmp_db: Path):
    """Outflow $500 on 2026-05-20, inflow -$500 on 2026-05-21 → detected."""
    conn = get_db(tmp_db)
    user_id = _seed_user(conn)
    conn_id = _seed_connection(conn, user_id)
    acct_a = _seed_account(conn, conn_id)
    acct_b = _seed_account(conn, conn_id)

    tx_out = _seed_transaction(conn, acct_a, 500.0, "2026-05-20")
    tx_in = _seed_transaction(conn, acct_b, -500.0, "2026-05-21")

    pairs = detect_internal_transfers(conn, user_id, lookback_days=365)
    conn.close()

    assert len(pairs) == 1
    p = pairs[0]
    assert p["outflow_tx_id"] == tx_out
    assert p["inflow_tx_id"] == tx_in
    assert p["amount"] == 500.0
    assert p["days_apart"] == 1
    assert p["account_a"] == acct_a
    assert p["account_b"] == acct_b


def test_amount_tolerance_within_penny(tmp_db: Path):
    """Amounts within $0.01 of each other should still be detected."""
    conn = get_db(tmp_db)
    user_id = _seed_user(conn)
    conn_id = _seed_connection(conn, user_id)
    acct_a = _seed_account(conn, conn_id)
    acct_b = _seed_account(conn, conn_id)

    tx_out = _seed_transaction(conn, acct_a, 500.00, "2026-05-20")
    tx_in = _seed_transaction(conn, acct_b, -500.005, "2026-05-20")

    pairs = detect_internal_transfers(conn, user_id, lookback_days=365)
    conn.close()

    assert len(pairs) == 1
    assert pairs[0]["outflow_tx_id"] == tx_out
    assert pairs[0]["inflow_tx_id"] == tx_in


def test_more_than_3_days_apart_not_detected(tmp_db: Path):
    """4 days apart should NOT be detected."""
    conn = get_db(tmp_db)
    user_id = _seed_user(conn)
    conn_id = _seed_connection(conn, user_id)
    acct_a = _seed_account(conn, conn_id)
    acct_b = _seed_account(conn, conn_id)

    _seed_transaction(conn, acct_a, 500.0, "2026-05-20")
    _seed_transaction(conn, acct_b, -500.0, "2026-05-24")  # 4 days later

    pairs = detect_internal_transfers(conn, user_id, lookback_days=365)
    conn.close()

    assert pairs == []


def test_same_account_not_detected(tmp_db: Path):
    """Outflow and inflow on the same account should NOT be detected as a transfer."""
    conn = get_db(tmp_db)
    user_id = _seed_user(conn)
    conn_id = _seed_connection(conn, user_id)
    acct_a = _seed_account(conn, conn_id)

    _seed_transaction(conn, acct_a, 500.0, "2026-05-20")
    _seed_transaction(conn, acct_a, -500.0, "2026-05-21")

    pairs = detect_internal_transfers(conn, user_id, lookback_days=365)
    conn.close()

    assert pairs == []


def test_different_users_not_detected(tmp_db: Path):
    """Transactions from different users should NOT be matched."""
    conn = get_db(tmp_db)

    user_a = _seed_user(conn)
    conn_a = _seed_connection(conn, user_a)
    acct_a = _seed_account(conn, conn_a)

    user_b = _seed_user(conn)
    conn_b = _seed_connection(conn, user_b)
    acct_b = _seed_account(conn, conn_b)

    _seed_transaction(conn, acct_a, 500.0, "2026-05-20")
    _seed_transaction(conn, acct_b, -500.0, "2026-05-21")

    # Query from user_a's perspective: should find no match with user_b's account.
    pairs = detect_internal_transfers(conn, user_a, lookback_days=365)
    conn.close()

    assert pairs == []


# ---------------------------------------------------------------------------
# is_investment_account tests
# ---------------------------------------------------------------------------


def test_is_investment_wealthsimple():
    assert is_investment_account({"institution_name": "Wealthsimple"}) is True


def test_is_investment_wealthsimple_lower():
    assert is_investment_account({"institution_name": "wealthsimple trade"}) is True


def test_is_investment_questrade():
    assert is_investment_account({"institution_name": "Questrade Inc."}) is True


def test_is_investment_robinhood():
    assert is_investment_account({"institution_name": "Robinhood Markets"}) is True


def test_is_investment_vanguard():
    assert is_investment_account({"institution_name": "Vanguard"}) is True


def test_is_investment_fidelity():
    assert is_investment_account({"institution_name": "Fidelity Investments"}) is True


def test_is_investment_schwab():
    assert is_investment_account({"institution_name": "Charles Schwab"}) is True


def test_not_investment_rbc():
    assert is_investment_account({"institution_name": "RBC Royal Bank"}) is False


def test_not_investment_td():
    assert is_investment_account({"institution_name": "TD Canada Trust"}) is False


def test_not_investment_none():
    assert is_investment_account({"institution_name": None}) is False


def test_not_investment_empty():
    assert is_investment_account({"institution_name": ""}) is False


# ---------------------------------------------------------------------------
# get_transfer_hint tests
# ---------------------------------------------------------------------------


def test_get_transfer_hint_match(tmp_db: Path):
    """get_transfer_hint returns a hint dict for a transaction that is part of a pair."""
    conn = get_db(tmp_db)
    user_id = _seed_user(conn)
    conn_id = _seed_connection(conn, user_id)
    acct_a = _seed_account(conn, conn_id)
    acct_b = _seed_account(conn, conn_id)

    tx_out = _seed_transaction(conn, acct_a, 500.0, "2026-05-20")
    _seed_transaction(conn, acct_b, -500.0, "2026-05-21")
    conn.close()

    hint = get_transfer_hint(tx_out, str(tmp_db))
    assert hint is not None
    assert hint["is_possible_transfer"] is True
    assert hint["matched_account"] == acct_b
    assert hint["matched_amount"] == 500.0


def test_get_transfer_hint_inflow_match(tmp_db: Path):
    """get_transfer_hint also works when queried from the inflow side."""
    conn = get_db(tmp_db)
    user_id = _seed_user(conn)
    conn_id = _seed_connection(conn, user_id)
    acct_a = _seed_account(conn, conn_id)
    acct_b = _seed_account(conn, conn_id)

    _seed_transaction(conn, acct_a, 500.0, "2026-05-20")
    tx_in = _seed_transaction(conn, acct_b, -500.0, "2026-05-21")
    conn.close()

    hint = get_transfer_hint(tx_in, str(tmp_db))
    assert hint is not None
    assert hint["is_possible_transfer"] is True
    assert hint["matched_account"] == acct_a
    assert hint["matched_amount"] == 500.0


def test_get_transfer_hint_no_match(tmp_db: Path):
    """get_transfer_hint returns None when no pair is detected."""
    conn = get_db(tmp_db)
    user_id = _seed_user(conn)
    conn_id = _seed_connection(conn, user_id)
    acct_a = _seed_account(conn, conn_id)

    tx_id = _seed_transaction(conn, acct_a, 500.0, "2026-05-20")
    conn.close()

    hint = get_transfer_hint(tx_id, str(tmp_db))
    assert hint is None


def test_get_transfer_hint_unknown_tx(tmp_db: Path):
    """get_transfer_hint returns None for an unknown transaction id."""
    hint = get_transfer_hint("nonexistent-tx-id", str(tmp_db))
    assert hint is None
