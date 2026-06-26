"""
tests/test_health_monitor.py — Tests for server.health_monitor.check_all_connections().

Covers:
  - No error → status stays/becomes 'active', last_synced_at updated
  - ITEM_LOGIN_REQUIRED → status becomes 'needs_reauth'
  - PENDING_EXPIRATION → status becomes 'pending_expiration'
  - Return shape includes correct counts
  - ITEM_LOCKED → status becomes 'needs_reauth' (same re-auth bucket)
  - Unknown error code → status unchanged (warning logged)
"""

from __future__ import annotations

import uuid

import pytest

from server.db import get_db, init_db
from server.health_monitor import check_all_connections

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _insert_connection(conn, connection_id: str, status: str = "active") -> None:
    conn.execute(
        "INSERT INTO bank_connections "
        "(id, plaid_item_id, plaid_access_token_encrypted, status) "
        "VALUES (?, ?, ?, ?)",
        (connection_id, f"item-{connection_id[:8]}", f"tok-{connection_id[:8]}", status),
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_env(tmp_path, monkeypatch):
    """Patch paths and init a tmp DB with three bank_connections."""
    db = tmp_path / "data.db"
    monkeypatch.setattr("server.paths.DB_PATH", db)
    init_db(db)

    conn_active_id = str(uuid.uuid4())  # should stay active (no error)
    conn_reauth_id = str(uuid.uuid4())  # ITEM_LOGIN_REQUIRED → needs_reauth
    conn_pending_id = str(uuid.uuid4())  # PENDING_EXPIRATION → pending_expiration

    conn = get_db(db)
    _insert_connection(conn, conn_active_id, "active")
    _insert_connection(conn, conn_reauth_id, "active")
    _insert_connection(conn, conn_pending_id, "active")
    conn.commit()
    conn.close()

    return {
        "db": db,
        "conn_active_id": conn_active_id,
        "conn_reauth_id": conn_reauth_id,
        "conn_pending_id": conn_pending_id,
    }


# ---------------------------------------------------------------------------
# Mock PlaidProvider
# ---------------------------------------------------------------------------


class _MockPlaid:
    """Returns different item statuses keyed by access_token prefix."""

    def __init__(self, token_responses: dict):
        # token_responses: {token_prefix: return_dict}
        self._responses = token_responses

    def get_item_status(self, access_token: str) -> dict:
        for prefix, resp in self._responses.items():
            if access_token.startswith(prefix):
                return resp
        return {}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_no_error_sets_active(db_env, monkeypatch):
    """Connection with no Plaid error → status='active', last_synced_at updated."""
    monkeypatch.setattr("server.crypto.decrypt", lambda x: x)

    env = db_env
    token = f"tok-{env['conn_active_id'][:8]}"

    plaid = _MockPlaid({token: {"error_code": None, "item_id": "item-abc"}})

    db = get_db(env["db"])
    try:
        # Only test the single active connection
        db.execute(
            "DELETE FROM bank_connections WHERE id != ?",
            (env["conn_active_id"],),
        )
        db.commit()

        result = check_all_connections(db, plaid_provider=plaid)
    finally:
        db.close()

    assert result["checked"] == 1
    assert result["active"] == 1
    assert result["needs_reauth"] == 0
    assert result["pending_expiration"] == 0

    # Verify DB update
    db2 = get_db(env["db"])
    row = db2.execute(
        "SELECT status, last_synced_at FROM bank_connections WHERE id=?",
        (env["conn_active_id"],),
    ).fetchone()
    db2.close()

    assert row["status"] == "active"
    assert row["last_synced_at"] is not None


def test_item_login_required_sets_needs_reauth(db_env, monkeypatch):
    """ITEM_LOGIN_REQUIRED → status='needs_reauth'."""
    monkeypatch.setattr("server.crypto.decrypt", lambda x: x)

    env = db_env
    token = f"tok-{env['conn_reauth_id'][:8]}"

    plaid = _MockPlaid({token: {"error_code": "ITEM_LOGIN_REQUIRED"}})

    db = get_db(env["db"])
    try:
        db.execute(
            "DELETE FROM bank_connections WHERE id != ?",
            (env["conn_reauth_id"],),
        )
        db.commit()

        result = check_all_connections(db, plaid_provider=plaid)
    finally:
        db.close()

    assert result["checked"] == 1
    assert result["needs_reauth"] == 1
    assert result["active"] == 0

    db2 = get_db(env["db"])
    row = db2.execute(
        "SELECT status FROM bank_connections WHERE id=?",
        (env["conn_reauth_id"],),
    ).fetchone()
    db2.close()

    assert row["status"] == "needs_reauth"


def test_pending_expiration_sets_status(db_env, monkeypatch):
    """PENDING_EXPIRATION → status='pending_expiration'."""
    monkeypatch.setattr("server.crypto.decrypt", lambda x: x)

    env = db_env
    token = f"tok-{env['conn_pending_id'][:8]}"

    plaid = _MockPlaid({token: {"error_code": "PENDING_EXPIRATION"}})

    db = get_db(env["db"])
    try:
        db.execute(
            "DELETE FROM bank_connections WHERE id != ?",
            (env["conn_pending_id"],),
        )
        db.commit()

        result = check_all_connections(db, plaid_provider=plaid)
    finally:
        db.close()

    assert result["checked"] == 1
    assert result["pending_expiration"] == 1
    assert result["needs_reauth"] == 0

    db2 = get_db(env["db"])
    row = db2.execute(
        "SELECT status FROM bank_connections WHERE id=?",
        (env["conn_pending_id"],),
    ).fetchone()
    db2.close()

    assert row["status"] == "pending_expiration"


def test_all_three_connections_counts(db_env, monkeypatch):
    """Three connections with three different outcomes — verify full result shape."""
    monkeypatch.setattr("server.crypto.decrypt", lambda x: x)

    env = db_env
    tok_active = f"tok-{env['conn_active_id'][:8]}"
    tok_reauth = f"tok-{env['conn_reauth_id'][:8]}"
    tok_pending = f"tok-{env['conn_pending_id'][:8]}"

    plaid = _MockPlaid(
        {
            tok_active: {"error_code": None},
            tok_reauth: {"error_code": "ITEM_LOGIN_REQUIRED"},
            tok_pending: {"error_code": "PENDING_EXPIRATION"},
        }
    )

    db = get_db(env["db"])
    try:
        result = check_all_connections(db, plaid_provider=plaid)
    finally:
        db.close()

    assert result["checked"] == 3
    assert result["active"] == 1
    assert result["needs_reauth"] == 1
    assert result["pending_expiration"] == 1


def test_item_locked_sets_needs_reauth(db_env, monkeypatch):
    """ITEM_LOCKED is also a re-auth scenario → status='needs_reauth'."""
    monkeypatch.setattr("server.crypto.decrypt", lambda x: x)

    env = db_env
    token = f"tok-{env['conn_active_id'][:8]}"

    plaid = _MockPlaid({token: {"error_code": "ITEM_LOCKED"}})

    db = get_db(env["db"])
    try:
        db.execute(
            "DELETE FROM bank_connections WHERE id != ?",
            (env["conn_active_id"],),
        )
        db.commit()

        result = check_all_connections(db, plaid_provider=plaid)
    finally:
        db.close()

    assert result["needs_reauth"] == 1

    db2 = get_db(env["db"])
    row = db2.execute(
        "SELECT status FROM bank_connections WHERE id=?",
        (env["conn_active_id"],),
    ).fetchone()
    db2.close()

    assert row["status"] == "needs_reauth"


def test_unknown_error_code_leaves_status_unchanged(db_env, monkeypatch):
    """Unknown Plaid error code → status unchanged, warning logged."""
    monkeypatch.setattr("server.crypto.decrypt", lambda x: x)

    env = db_env
    token = f"tok-{env['conn_active_id'][:8]}"

    plaid = _MockPlaid({token: {"error_code": "SOME_WEIRD_ERROR"}})

    db = get_db(env["db"])
    try:
        db.execute(
            "DELETE FROM bank_connections WHERE id != ?",
            (env["conn_active_id"],),
        )
        db.commit()

        result = check_all_connections(db, plaid_provider=plaid)
    finally:
        db.close()

    # Counted as checked but not as active/reauth/pending
    assert result["checked"] == 1
    assert result["active"] == 0
    assert result["needs_reauth"] == 0
    assert result["pending_expiration"] == 0

    # Status must not change
    db2 = get_db(env["db"])
    row = db2.execute(
        "SELECT status FROM bank_connections WHERE id=?",
        (env["conn_active_id"],),
    ).fetchone()
    db2.close()

    assert row["status"] == "active"


def test_no_active_connections_returns_zero_counts(db_env, monkeypatch):
    """No active connections → all zero counts, plaid never called."""
    monkeypatch.setattr("server.crypto.decrypt", lambda x: x)

    env = db_env

    class _NeverCalledPlaid:
        def get_item_status(self, access_token):
            raise AssertionError("should not be called")

    db = get_db(env["db"])
    try:
        # Set all connections to non-active
        db.execute("UPDATE bank_connections SET status='needs_reauth'")
        db.commit()

        result = check_all_connections(db, plaid_provider=_NeverCalledPlaid())
    finally:
        db.close()

    assert result == {"checked": 0, "active": 0, "needs_reauth": 0, "pending_expiration": 0}
