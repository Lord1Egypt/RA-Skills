"""
tests/test_ui_account_description.py — Tests for PATCH /profile/accounts/{id}/description

Covers:
  - Authenticated PATCH saves description, returns 200 + {"status": "ok"}
  - Unauthenticated PATCH returns 401
  - PATCH with unknown account_id returns 404
  - Empty string clears description (sets to NULL)
"""

from __future__ import annotations

import time
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import server.paths
from server.db import get_db, init_db

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_path(tmp_path: Path, monkeypatch) -> Path:
    """Initialise a fresh DB and monkeypatch server.paths.DB_PATH."""
    db = tmp_path / "test.db"
    init_db(db)
    monkeypatch.setattr(server.paths, "DB_PATH", db)
    monkeypatch.setattr("server.paths.APP_DIR", tmp_path)
    return db


@pytest.fixture()
def db_with_account(db_path: Path) -> tuple[Path, str, str]:
    """Return (db_path, conn_id, acct_id) after inserting a bank connection + account."""
    conn_id = str(uuid.uuid4())
    acct_id = str(uuid.uuid4())
    conn = get_db(db_path)
    conn.execute(
        "INSERT INTO bank_connections (id, plaid_item_id, plaid_access_token_encrypted, institution_name)"
        " VALUES (?, ?, ?, ?)",
        (conn_id, "item-test", "enc", "Test Bank"),
    )
    conn.execute(
        "INSERT INTO bank_accounts (id, connection_id, plaid_account_id, name, type)"
        " VALUES (?, ?, ?, ?, ?)",
        (acct_id, conn_id, "plaid-1", "Chequing", "depository"),
    )
    conn.execute("INSERT OR IGNORE INTO app_config (id) VALUES (1)")
    conn.commit()
    conn.close()
    return db_path, conn_id, acct_id


@pytest.fixture()
def client(db_path: Path) -> TestClient:
    from ui.server import app

    return TestClient(app, follow_redirects=False)


@pytest.fixture()
def authed_client(db_with_account) -> tuple[TestClient, Path, str]:
    """TestClient with a valid session cookie; returns (client, db_path, acct_id)."""
    db_path, conn_id, acct_id = db_with_account

    # Insert a session token directly
    token = "test-" + uuid.uuid4().hex
    now = int(time.time())
    conn = get_db(db_path)
    conn.execute(
        "INSERT INTO sessions (id, created_at, last_seen_at, expires_at) VALUES (?,?,?,?)",
        (token, now, now, now + 86400 * 3650),
    )
    conn.commit()
    conn.close()

    from ui.server import SESSION_COOKIE, app

    c = TestClient(app, follow_redirects=False)
    c.cookies.set(SESSION_COOKIE, token)
    return c, db_path, acct_id


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_patch_description_returns_200(authed_client):
    client, db_path, acct_id = authed_client
    resp = client.patch(
        f"/profile/accounts/{acct_id}/description",
        json={"description": "Day-to-day spending"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["account_id"] == acct_id


def test_patch_description_persists(authed_client):
    client, db_path, acct_id = authed_client
    client.patch(
        f"/profile/accounts/{acct_id}/description",
        json={"description": "Savings buffer"},
    )
    conn = get_db(db_path)
    row = conn.execute("SELECT description FROM bank_accounts WHERE id = ?", (acct_id,)).fetchone()
    conn.close()
    assert row["description"] == "Savings buffer"


def test_patch_description_not_authenticated(client):
    """Unauthenticated request to PATCH endpoint returns 401."""
    resp = client.patch(
        "/profile/accounts/some-id/description",
        json={"description": "X"},
    )
    assert resp.status_code == 401


def test_patch_description_unknown_account(authed_client):
    """Patching a non-existent account_id returns 404."""
    client, db_path, acct_id = authed_client
    resp = client.patch(
        "/profile/accounts/does-not-exist/description",
        json={"description": "Irrelevant"},
    )
    assert resp.status_code == 404


def test_patch_description_empty_string_clears(authed_client):
    """Sending empty string clears the description (sets to NULL)."""
    client, db_path, acct_id = authed_client

    # Set first
    client.patch(
        f"/profile/accounts/{acct_id}/description",
        json={"description": "Something"},
    )
    # Clear
    resp = client.patch(
        f"/profile/accounts/{acct_id}/description",
        json={"description": ""},
    )
    assert resp.status_code == 200

    conn = get_db(db_path)
    row = conn.execute("SELECT description FROM bank_accounts WHERE id = ?", (acct_id,)).fetchone()
    conn.close()
    assert row["description"] is None
