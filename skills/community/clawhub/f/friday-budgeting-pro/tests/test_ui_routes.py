"""
tests/test_ui_routes.py — Tests for the Friday Budgeting Pro UI (issue #14).

Uses fastapi.testclient.TestClient with a tmp_path DB so tests are fully
isolated.  server.paths.DB_PATH is monkeypatched so all route helpers use
the temp database.
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
    # Also patch APP_DIR so recovery.txt writes don't touch ~/.friday-bp
    monkeypatch.setattr(paths, "APP_DIR", tmp_path)

    # Reload ui.auth and ui.server so they pick up the monkeypatched paths.
    # We do this by patching the module-level attribute that routes read via
    # _paths.DB_PATH (since routes call _paths.DB_PATH at request time via
    # the _db_path() helper, the monkeypatch on paths.DB_PATH is sufficient).
    return db


@pytest.fixture()
def client(db_path: Path) -> TestClient:
    """TestClient backed by the patched app."""
    from ui.server import app

    return TestClient(app, follow_redirects=False)


@pytest.fixture()
def authed_client(db_path: Path) -> TestClient:
    """TestClient with a valid session cookie already set.

    Sets a password via the setup wizard, then logs in.
    """
    from ui.server import app

    client = TestClient(app, follow_redirects=False)
    _complete_setup(client)
    return _login(client)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _complete_setup(client: TestClient, password: str = "testpassword123") -> None:
    """Drive the setup wizard to completion."""
    # Step 1: password
    r = client.post(
        "/setup/1",
        data={
            "password": password,
            "password_confirm": password,
        },
    )
    assert r.status_code == 200, f"Setup step 1 failed: {r.status_code}"

    # Step 2: notification pref
    r = client.post("/setup/2", data={"notification_pref": "openclaw"})
    assert r.status_code == 200, f"Setup step 2 failed: {r.status_code}"

    # Step 3: bank link (skip) — terminal wizard step, redirects to /dashboard
    r = client.post("/setup/3", data={"action": "skip"})
    assert r.status_code == 302, f"Setup step 3 failed: {r.status_code}"
    assert r.headers["location"] == "/dashboard"


def _login(client: TestClient, password: str = "testpassword123") -> TestClient:
    """POST /login and return the same client (which now holds the session cookie)."""
    r = client.post("/login", data={"password": password})
    assert r.status_code == 302, f"Login failed: {r.status_code}"
    assert r.headers["location"] == "/dashboard"
    # TestClient stores Set-Cookie automatically.
    return client


# ---------------------------------------------------------------------------
# Tests — without a password set (fresh DB)
# ---------------------------------------------------------------------------


class TestNoPasswordSet:
    def test_healthz(self, client):
        r = client.get("/healthz")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}

    def test_root_redirects_to_setup(self, client):
        r = client.get("/")
        assert r.status_code == 302
        assert r.headers["location"] == "/setup"

    def test_setup_returns_200(self, client):
        r = client.get("/setup")
        assert r.status_code == 200
        assert b"Welcome" in r.content or b"setup" in r.content.lower()

    def test_login_redirects_to_setup_when_no_password(self, client):
        r = client.get("/login")
        assert r.status_code == 302
        assert r.headers["location"] == "/setup"


# ---------------------------------------------------------------------------
# Tests — after setup (password set)
# ---------------------------------------------------------------------------


class TestAfterSetup:
    @pytest.fixture(autouse=True)
    def _setup_done(self, client):
        """Complete setup before each test in this class."""
        _complete_setup(client)

    def test_login_page_is_200_after_setup(self, client):
        r = client.get("/login")
        assert r.status_code == 200
        assert b"Sign in" in r.content or b"login" in r.content.lower()

    def test_setup_returns_404_after_complete(self, client):
        r = client.get("/setup")
        assert r.status_code == 404

    def test_root_redirects_to_login_when_not_authed(self, client):
        # The wizard sets a session cookie at step 1 (per the wizard spec).
        # Clear cookies to test the not-authed path explicitly.
        client.cookies.clear()
        r = client.get("/")
        assert r.status_code == 302
        assert r.headers["location"] == "/login"

    def test_login_wrong_password_returns_200_with_error(self, client):
        r = client.post("/login", data={"password": "wrongpassword"})
        assert r.status_code == 200
        assert b"Incorrect" in r.content or b"error" in r.content.lower()

    def test_login_correct_password_redirects_to_profile_with_cookie(self, client):
        r = client.post("/login", data={"password": "testpassword123"})
        assert r.status_code == 302
        assert r.headers["location"] == "/dashboard"
        # TestClient stores the cookie; verify Set-Cookie was in response.
        assert "set-cookie" in r.headers

    def test_profile_without_cookie_redirects_to_login(self, client):
        # Make sure no session cookie is present.
        client.cookies.clear()
        r = client.get("/profile")
        assert r.status_code == 302
        assert r.headers["location"] == "/login"

    def test_profile_with_valid_cookie_returns_200(self, client):
        _login(client)
        r = client.get("/profile")
        assert r.status_code == 200
        assert b"Profile" in r.content

    def test_ledgers_with_valid_cookie_returns_200(self, client):
        _login(client)
        r = client.get("/ledgers")
        assert r.status_code == 200

    def test_logout_clears_cookie_and_redirects_to_login(self, client):
        _login(client)
        r = client.post("/logout")
        assert r.status_code == 302
        assert r.headers["location"] == "/login"
        # After logout, profile should redirect to login.
        r2 = client.get("/profile")
        assert r2.status_code == 302
        assert r2.headers["location"] == "/login"


# ---------------------------------------------------------------------------
# Tests — authenticated misc routes
# ---------------------------------------------------------------------------


class TestAuthenticatedRoutes:
    @pytest.fixture(autouse=True)
    def _authed(self, authed_client):
        self.client = authed_client

    def test_healthz_always_200(self):
        r = self.client.get("/healthz")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}

    def test_forgot_get_200(self):
        r = self.client.get("/forgot")
        assert r.status_code == 200

    def test_forgot_post_200(self):
        r = self.client.post("/forgot")
        assert r.status_code == 200

    def test_reset_get_200(self):
        r = self.client.get("/reset")
        assert r.status_code == 200

    def test_reset_post_placeholder(self):
        r = self.client.post(
            "/reset",
            data={
                "token": "abc",
                "password": "newpassword1",
                "password_confirm": "newpassword1",
            },
        )
        assert r.status_code == 200

    def test_link_get_200(self):
        r = self.client.get("/link")
        assert r.status_code == 200

    def test_link_get_with_token(self):
        r = self.client.get("/link?token=test-link-token")
        assert r.status_code == 200
        assert b"test-link-token" in r.content

    def test_profile_post_saves_settings(self):
        r = self.client.post("/profile", data={"notification_pref": "macos"})
        assert r.status_code == 200

    def test_ledgers_shows_personal_ledger(self):
        """The setup wizard created a 'Personal' ledger; it should appear."""
        r = self.client.get("/ledgers")
        assert r.status_code == 200
        assert b"Personal" in r.content

    def test_static_file_served(self):
        r = self.client.get("/static/style.css")
        assert r.status_code == 200
        assert "text/css" in r.headers.get("content-type", "")
