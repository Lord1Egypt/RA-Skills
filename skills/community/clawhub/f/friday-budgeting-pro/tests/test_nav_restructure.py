"""
tests/test_nav_restructure.py — Tests for issue #162: Nav restructure.

Covers:
  - GET /dashboard (authed) → 200, contains "Dashboard", "Sync Now", "Export to Excel"
  - GET /accounts (authed) → 200 (stub)
  - GET /settings (authed) → 200 (stub)
  - GET / (authed) → 302 to /dashboard
  - GET /ledgers (authed) → 200 (existing, unchanged)
  - After login POST, redirected to /dashboard
"""

from __future__ import annotations

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

    set_password_hash(db_path, hash_password("testpassword123"))
    token = create_session(db_path, user_agent="pytest")

    client = TestClient(app, follow_redirects=False)
    client.cookies.set(SESSION_COOKIE, token)
    return client


@pytest.fixture()
def unauthed_client(db_path: Path) -> TestClient:
    """TestClient without a session cookie but with a password set."""
    from ui.auth import hash_password, set_password_hash
    from ui.server import app

    set_password_hash(db_path, hash_password("testpassword123"))

    return TestClient(app, follow_redirects=False)


# ---------------------------------------------------------------------------
# Dashboard tests
# ---------------------------------------------------------------------------


class TestDashboard:
    def test_dashboard_requires_auth(self, unauthed_client):
        r = unauthed_client.get("/dashboard")
        assert r.status_code == 302
        assert "/login" in r.headers["location"]

    def test_dashboard_200_authed(self, authed_client):
        r = authed_client.get("/dashboard")
        assert r.status_code == 200

    def test_dashboard_contains_dashboard_heading(self, authed_client):
        r = authed_client.get("/dashboard")
        assert "Dashboard" in r.text

    def test_dashboard_contains_sync_now(self, authed_client):
        r = authed_client.get("/dashboard")
        assert "Sync Now" in r.text

    def test_dashboard_contains_export_excel(self, authed_client):
        r = authed_client.get("/dashboard")
        assert "Export to Excel" in r.text or "export/excel" in r.text

    def test_dashboard_has_nav(self, authed_client):
        r = authed_client.get("/dashboard")
        body = r.text
        assert "/accounts" in body
        assert "/ledgers" in body
        assert "/settings" in body
        assert "/logout" in body


# ---------------------------------------------------------------------------
# Accounts stub tests
# ---------------------------------------------------------------------------


class TestAccountsStub:
    def test_accounts_requires_auth(self, unauthed_client):
        r = unauthed_client.get("/accounts")
        assert r.status_code == 302
        assert "/login" in r.headers["location"]

    def test_accounts_200_authed(self, authed_client):
        r = authed_client.get("/accounts")
        assert r.status_code == 200

    def test_accounts_contains_accounts_text(self, authed_client):
        r = authed_client.get("/accounts")
        assert "Accounts" in r.text


# ---------------------------------------------------------------------------
# Settings stub tests
# ---------------------------------------------------------------------------


class TestSettingsStub:
    def test_settings_requires_auth(self, unauthed_client):
        r = unauthed_client.get("/settings")
        assert r.status_code == 302
        assert "/login" in r.headers["location"]

    def test_settings_200_authed(self, authed_client):
        r = authed_client.get("/settings")
        assert r.status_code == 200

    def test_settings_contains_settings_text(self, authed_client):
        r = authed_client.get("/settings")
        assert "Settings" in r.text


# ---------------------------------------------------------------------------
# Root redirect
# ---------------------------------------------------------------------------


class TestRootRedirect:
    def test_root_authed_redirects_to_dashboard(self, authed_client):
        r = authed_client.get("/")
        assert r.status_code == 302
        assert r.headers["location"].endswith("/dashboard")

    def test_root_unauthed_redirects_to_login(self, unauthed_client):
        r = unauthed_client.get("/")
        assert r.status_code == 302
        assert "/login" in r.headers["location"]


# ---------------------------------------------------------------------------
# Ledgers (existing route, unchanged)
# ---------------------------------------------------------------------------


class TestLedgersUnchanged:
    def test_ledgers_200_authed(self, authed_client):
        r = authed_client.get("/ledgers")
        assert r.status_code == 200

    def test_ledgers_has_nav(self, authed_client):
        r = authed_client.get("/ledgers")
        assert "/dashboard" in r.text
        assert "/accounts" in r.text
        assert "/settings" in r.text


# ---------------------------------------------------------------------------
# After login → redirected to /dashboard
# ---------------------------------------------------------------------------


class TestLoginRedirectsToDashboard:
    def test_login_post_redirects_to_dashboard(self, db_path):
        from ui.auth import create_user, hash_password, set_password_hash
        from ui.server import app

        set_password_hash(db_path, hash_password("mypassword1"))
        create_user(db_path, "testuser", "mypassword1")

        client = TestClient(app, follow_redirects=False)
        r = client.post("/login", data={"username": "testuser", "password": "mypassword1"})
        assert r.status_code == 302
        assert r.headers["location"].endswith("/dashboard")
