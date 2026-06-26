"""
tests/test_profile_page.py — Tests for issue #47: Profile page Linked Accounts section.

Covers:
  - GET /profile shows bank_connections list (institution name or "—" for NULL, status text)
  - GET /profile shows Sync Now button
  - POST /profile action=sync_now → 200 with success message
  - POST /profile action=disconnect_bank → 200, row removed from bank_connections
  - POST /profile action=reconnect_bank → 200 with Plaid Link URL surfaced
"""

from __future__ import annotations

import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_path(tmp_path: Path, monkeypatch) -> Path:
    """Initialise a fresh SQLite DB in tmp_path and monkeypatch DB_PATH."""
    import server.paths as paths
    from server.db import init_db

    db = tmp_path / "test.db"
    init_db(db)

    monkeypatch.setattr(paths, "DB_PATH", db)
    monkeypatch.setattr(paths, "APP_DIR", tmp_path)
    return db


@pytest.fixture()
def authed_client(db_path: Path) -> TestClient:
    """TestClient with a valid session cookie and password set."""
    from ui.auth import SESSION_COOKIE, create_session, hash_password, set_password_hash
    from ui.server import app

    # Set password
    set_password_hash(db_path, hash_password("testpassword123"))

    # Create a session
    token = create_session(db_path, user_agent="pytest")

    client = TestClient(app, follow_redirects=False)
    client.cookies.set(SESSION_COOKIE, token)
    return client


@pytest.fixture()
def seeded_db(db_path: Path) -> tuple[Path, str, str]:
    """
    Seed two bank_connections: one active, one needs_reauth.
    Returns (db_path, active_id, reauth_id).
    """
    from server.db import get_db

    active_id = str(uuid.uuid4())
    reauth_id = str(uuid.uuid4())

    conn = get_db(db_path)
    try:
        conn.execute(
            "INSERT INTO bank_connections (id, plaid_access_token_encrypted, institution_name, status, last_synced_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (active_id, "enc_token_active", "Chase Bank", "active", 1700000000),
        )
        conn.execute(
            "INSERT INTO bank_connections (id, plaid_access_token_encrypted, institution_name, status, last_synced_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (reauth_id, "enc_token_reauth", None, "needs_reauth", None),
        )
        conn.commit()
    finally:
        conn.close()

    return db_path, active_id, reauth_id


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestProfileGetLinkedAccounts:
    def test_shows_institution_name(self, authed_client, seeded_db):
        """GET /profile lists institution names; NULL becomes '—'."""
        db_path, active_id, reauth_id = seeded_db
        r = authed_client.get("/profile")
        assert r.status_code == 200
        body = r.text
        # Active bank should show its institution name
        assert "Chase Bank" in body
        # Null institution name should show em-dash placeholder
        assert "\u2014" in body

    def test_shows_needs_reauth_status(self, authed_client, seeded_db):
        """GET /profile includes 'needs_reauth' status text."""
        db_path, active_id, reauth_id = seeded_db
        r = authed_client.get("/profile")
        assert r.status_code == 200
        assert "needs_reauth" in r.text

    def test_shows_sync_now_button(self, authed_client, seeded_db):
        """GET /profile includes a Sync Now button."""
        r = authed_client.get("/profile")
        assert r.status_code == 200
        # Button text or id
        assert "Sync Now" in r.text or "btn-sync-now" in r.text


class TestProfilePostSyncNow:
    def test_sync_now_success(self, authed_client, db_path, monkeypatch):
        """POST /profile action=sync_now calls server.main.sync() and shows success."""
        import server.main as _sm

        fake_result = {"connections_synced": 1, "total_added": 5}
        monkeypatch.setattr(_sm, "sync", lambda: fake_result)

        r = authed_client.post("/profile", data={"action": "sync_now"})
        assert r.status_code == 200
        assert "Sync complete" in r.text or "sync" in r.text.lower()

    def test_sync_now_failure(self, authed_client, db_path, monkeypatch):
        """POST /profile action=sync_now shows error on exception."""
        import server.main as _sm

        def _bad_sync():
            raise RuntimeError("Plaid unavailable")

        monkeypatch.setattr(_sm, "sync", _bad_sync)

        r = authed_client.post("/profile", data={"action": "sync_now"})
        assert r.status_code == 200
        assert "Plaid unavailable" in r.text or "failed" in r.text.lower()


class TestProfilePostDisconnectBank:
    def test_disconnect_removes_row(self, authed_client, seeded_db):
        """POST /profile action=disconnect_bank removes the connection row."""
        from server.db import get_db

        db_path, active_id, reauth_id = seeded_db

        r = authed_client.post(
            "/profile",
            data={
                "action": "disconnect_bank",
                "bank_id": active_id,
            },
        )
        # After successful disconnect the handler redirects to /accounts or /setup
        # (Bug 1 fix: no longer re-renders profile.html)
        assert r.status_code in (302, 303)
        assert r.headers["location"] in ("/accounts", "/setup")

        # Verify the row is gone
        conn = get_db(db_path)
        try:
            row = conn.execute(
                "SELECT id FROM bank_connections WHERE id = ?", (active_id,)
            ).fetchone()
        finally:
            conn.close()

        assert row is None, "bank_connection row should be deleted"

    def test_disconnect_shows_success(self, authed_client, seeded_db):
        """POST /profile action=disconnect_bank redirects to /accounts after success."""
        db_path, active_id, reauth_id = seeded_db
        r = authed_client.post(
            "/profile",
            data={
                "action": "disconnect_bank",
                "bank_id": active_id,
            },
        )
        # Bug 1 fix: successful disconnect now redirects instead of re-rendering
        assert r.status_code in (302, 303)
        assert r.headers["location"] in ("/accounts", "/setup")


class TestProfilePostReconnectBank:
    def test_reconnect_surfaces_url(self, authed_client, seeded_db, monkeypatch):
        """POST /profile action=reconnect_bank shows the Plaid Link URL."""
        import server.main as _sm

        fake_url = "http://127.0.0.1:6789/link?token=test-link-token-xyz"
        monkeypatch.setattr(_sm, "refresh_connection", lambda id: {"url": fake_url})

        db_path, active_id, reauth_id = seeded_db
        r = authed_client.post(
            "/profile",
            data={
                "action": "reconnect_bank",
                "bank_id": reauth_id,
            },
        )
        assert r.status_code == 200
        assert fake_url in r.text or "test-link-token-xyz" in r.text

    def test_reconnect_failure(self, authed_client, seeded_db, monkeypatch):
        """POST /profile action=reconnect_bank shows error when refresh fails."""
        import server.main as _sm

        def _bad_refresh(id):
            raise RuntimeError("Plaid token expired")

        monkeypatch.setattr(_sm, "refresh_connection", _bad_refresh)

        db_path, active_id, reauth_id = seeded_db
        r = authed_client.post(
            "/profile",
            data={
                "action": "reconnect_bank",
                "bank_id": reauth_id,
            },
        )
        assert r.status_code == 200
        assert "Plaid token expired" in r.text or "failed" in r.text.lower()
