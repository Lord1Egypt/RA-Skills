"""
tests/test_proactive_reauth.py — Tests for get_connections_needing_attention (#35).

Covers:
  - needs_reauth connection → returned with correct message
  - pending_expiration connection → returned with expiry message
  - active/healthy connection → NOT returned
  - last_alerted_at is updated after call
  - last_alerted_at within 24h → throttled (connection not returned again)
  - no active user → returns empty list
"""

from __future__ import annotations

import time
import uuid

import pytest

import server.paths
from server.db import get_db, init_db

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_path(tmp_path, monkeypatch):
    """Fresh temp DB with server.paths.DB_PATH monkeypatched."""
    path = tmp_path / "test.db"
    init_db(path)
    monkeypatch.setattr(server.paths, "DB_PATH", path)
    return path


@pytest.fixture()
def db_path_with_user(db_path):
    """db_path that has a user inserted.

    get_active_user_id() falls back to the first user in the DB when no
    session exists, so we only need to insert a user row here.
    """
    conn = get_db(db_path)
    user_id = str(uuid.uuid4())
    now = int(time.time())
    conn.execute(
        "INSERT INTO users (id, username, password_hash, created_at) VALUES (?, ?, ?, ?)",
        (user_id, "testuser", "fakehash", now),
    )
    conn.commit()
    conn.close()
    return db_path, user_id


def _insert_connection(db_path, user_id, status, institution_name="Test Bank", last_synced_at=1):
    """Helper: insert a bank_connections row and return its id."""
    conn = get_db(db_path)
    cid = str(uuid.uuid4())
    conn.execute(
        """
        INSERT INTO bank_connections
            (id, plaid_item_id, plaid_access_token_encrypted, status,
             user_id, institution_name, last_synced_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (cid, f"item-{cid}", f"enc:tok-{cid}", status, user_id, institution_name, last_synced_at),
    )
    conn.commit()
    conn.close()
    return cid


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_needs_reauth_returned_with_correct_message(db_path_with_user):
    db_path, user_id = db_path_with_user
    cid = _insert_connection(db_path, user_id, "needs_reauth", "BMO Bank of Montreal")

    from server.main import get_connections_needing_attention

    result = get_connections_needing_attention()

    assert isinstance(result, dict)
    assert "connections" in result
    connections = result["connections"]
    assert len(connections) == 1

    c = connections[0]
    assert c["connection_id"] == cid
    assert c["institution_name"] == "BMO Bank of Montreal"
    assert c["status"] == "needs_reauth"
    assert "re-authorization" in c["suggested_message"]
    assert "BMO Bank of Montreal" in c["suggested_message"]
    assert "reconnect BMO Bank of Montreal" in c["suggested_message"]


def test_pending_expiration_returned_with_expiry_message(db_path_with_user):
    db_path, user_id = db_path_with_user
    cid = _insert_connection(db_path, user_id, "pending_expiration", "TD Bank")

    from server.main import get_connections_needing_attention

    result = get_connections_needing_attention()

    connections = result["connections"]
    assert len(connections) == 1
    c = connections[0]
    assert c["connection_id"] == cid
    assert c["status"] == "pending_expiration"
    assert "expires" in c["suggested_message"]
    assert "TD Bank" in c["suggested_message"]
    assert "reconnect TD Bank" in c["suggested_message"]


def test_active_connection_not_returned(db_path_with_user):
    db_path, user_id = db_path_with_user
    # Healthy active connection — should NOT appear.
    _insert_connection(db_path, user_id, "active", "RBC Royal Bank")

    from server.main import get_connections_needing_attention

    result = get_connections_needing_attention()
    assert result["connections"] == []


def test_never_synced_connection_returned(db_path_with_user):
    db_path, user_id = db_path_with_user
    # last_synced_at=None → never synced → needs attention
    conn = get_db(db_path)
    cid = str(uuid.uuid4())
    conn.execute(
        """
        INSERT INTO bank_connections
            (id, plaid_item_id, plaid_access_token_encrypted, status,
             user_id, institution_name, last_synced_at)
        VALUES (?, ?, ?, 'active', ?, ?, NULL)
        """,
        (cid, f"item-{cid}", f"enc:tok-{cid}", user_id, "Scotiabank"),
    )
    conn.commit()
    conn.close()

    from server.main import get_connections_needing_attention

    result = get_connections_needing_attention()
    assert len(result["connections"]) == 1
    c = result["connections"][0]
    assert c["connection_id"] == cid
    assert "re-authorization" in c["suggested_message"]


def test_last_alerted_at_updated_after_call(db_path_with_user):
    db_path, user_id = db_path_with_user
    cid = _insert_connection(db_path, user_id, "needs_reauth")

    before = int(time.time())
    from server.main import get_connections_needing_attention

    get_connections_needing_attention()
    after = int(time.time())

    conn = get_db(db_path)
    row = conn.execute(
        "SELECT last_alerted_at FROM bank_connections WHERE id = ?", (cid,)
    ).fetchone()
    conn.close()

    assert row["last_alerted_at"] is not None
    assert before <= row["last_alerted_at"] <= after


def test_throttle_within_24h(db_path_with_user):
    """Connection alerted recently should NOT appear in a second call."""
    db_path, user_id = db_path_with_user
    cid = _insert_connection(db_path, user_id, "needs_reauth")

    # Pre-set last_alerted_at to 1 hour ago (within 24h window).
    one_hour_ago = int(time.time()) - 3600
    conn = get_db(db_path)
    conn.execute(
        "UPDATE bank_connections SET last_alerted_at = ? WHERE id = ?",
        (one_hour_ago, cid),
    )
    conn.commit()
    conn.close()

    from server.main import get_connections_needing_attention

    result = get_connections_needing_attention()
    assert result["connections"] == []


def test_not_throttled_after_24h(db_path_with_user):
    """Connection alerted >24h ago should appear again."""
    db_path, user_id = db_path_with_user
    cid = _insert_connection(db_path, user_id, "needs_reauth")

    # Pre-set last_alerted_at to 25 hours ago (outside cooldown).
    twenty_five_hours_ago = int(time.time()) - 25 * 3600
    conn = get_db(db_path)
    conn.execute(
        "UPDATE bank_connections SET last_alerted_at = ? WHERE id = ?",
        (twenty_five_hours_ago, cid),
    )
    conn.commit()
    conn.close()

    from server.main import get_connections_needing_attention

    result = get_connections_needing_attention()
    assert len(result["connections"]) == 1


def test_no_active_user_returns_empty(db_path):
    """When there is no active session/user, return empty list gracefully."""
    from server.main import get_connections_needing_attention

    result = get_connections_needing_attention()
    assert result == {"connections": []}


def test_only_current_user_connections_returned(db_path_with_user):
    """Connections belonging to a different user are not returned."""
    db_path, user_id = db_path_with_user

    # Create a second user with a needs_reauth connection (no session).
    other_user_id = str(uuid.uuid4())
    conn = get_db(db_path)
    now = int(time.time())
    conn.execute(
        "INSERT INTO users (id, username, password_hash, created_at) VALUES (?, ?, ?, ?)",
        (other_user_id, "otheruser", "fakehash2", now),
    )
    other_cid = str(uuid.uuid4())
    conn.execute(
        """
        INSERT INTO bank_connections
            (id, plaid_item_id, plaid_access_token_encrypted, status,
             user_id, institution_name, last_synced_at)
        VALUES (?, ?, ?, 'needs_reauth', ?, ?, 1)
        """,
        (other_cid, f"item-{other_cid}", f"enc:tok-{other_cid}", other_user_id, "Other Bank"),
    )
    conn.commit()
    conn.close()

    from server.main import get_connections_needing_attention

    result = get_connections_needing_attention()
    returned_ids = [c["connection_id"] for c in result["connections"]]
    assert other_cid not in returned_ids
