"""
tests/test_auth.py — Dedicated tests for ui.auth.

Covers:
  - argon2id hash/verify round trip
  - Wrong password -> verify_password returns False, no exception
  - create_session -> check_session round-trip
  - Logout deletes the session row
  - Sessions persist across DB close/reopen (no in-memory state)
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
    """Initialise a fresh SQLite DB and monkeypatch server.paths.DB_PATH."""
    import server.paths as paths
    from server.db import init_db

    db = tmp_path / "test_auth.db"
    init_db(db)

    monkeypatch.setattr(paths, "DB_PATH", db)
    monkeypatch.setattr(paths, "APP_DIR", tmp_path)
    return db


@pytest.fixture()
def client(db_path: Path) -> TestClient:
    from ui.server import app

    return TestClient(app, follow_redirects=False)


@pytest.fixture()
def setup_client(client: TestClient) -> TestClient:
    """Drive through setup wizard so a password is set."""
    _complete_setup(client)
    return client


def _complete_setup(client: TestClient, password: str = "correcthorsebattery") -> None:
    r = client.post("/setup/1", data={"password": password, "password_confirm": password})
    assert r.status_code == 200
    r = client.post("/setup/2", data={"notification_pref": "openclaw"})
    assert r.status_code == 200
    r = client.post("/setup/3", data={"action": "skip"})
    assert r.status_code == 302


# ---------------------------------------------------------------------------
# Unit tests -- password hashing
# ---------------------------------------------------------------------------


class TestPasswordHashing:
    def test_hash_verify_roundtrip(self):
        from ui.auth import hash_password, verify_password

        h = hash_password("mysecretpassword")
        assert verify_password("mysecretpassword", h) is True

    def test_wrong_password_returns_false(self):
        from ui.auth import hash_password, verify_password

        h = hash_password("correct")
        result = verify_password("wrong", h)
        assert result is False

    def test_wrong_password_no_exception(self):
        from ui.auth import hash_password, verify_password

        h = hash_password("correct")
        try:
            result = verify_password("definitely wrong", h)
            assert result is False
        except Exception as exc:
            pytest.fail(f"verify_password raised unexpectedly: {exc}")

    def test_empty_password_returns_false(self):
        from ui.auth import hash_password, verify_password

        h = hash_password("nonempty")
        assert verify_password("", h) is False

    def test_hash_uses_argon2id_format(self):
        from ui.auth import hash_password

        h = hash_password("test")
        assert h.startswith("$argon2id$"), f"Unexpected hash prefix: {h[:20]}"

    def test_two_hashes_differ(self):
        """argon2 uses a random salt -- two hashes of the same password differ."""
        from ui.auth import hash_password

        h1 = hash_password("same")
        h2 = hash_password("same")
        assert h1 != h2


# ---------------------------------------------------------------------------
# Unit tests -- session round-trip and logout
# ---------------------------------------------------------------------------


class TestSessionRoundTrip:
    def test_create_then_check_session(self, setup_client, db_path):
        """Login creates a session; accessing a protected page works."""
        r = setup_client.post("/login", data={"password": "correcthorsebattery"})
        assert r.status_code == 302
        r = setup_client.get("/profile")
        assert r.status_code == 200

    def test_wrong_password_rejected(self, setup_client):
        """Wrong password does not create a session."""
        r = setup_client.post("/login", data={"password": "wrongpassword"})
        assert r.status_code == 200  # login form re-rendered
        fresh = TestClient(setup_client.app, follow_redirects=False)
        r = fresh.get("/profile")
        assert r.status_code == 302
        assert r.headers["location"] == "/login"

    def test_logout_deletes_session(self, setup_client, db_path):
        """After logout, the session row is removed from the DB."""
        from server.db import get_db

        r = setup_client.post("/login", data={"password": "correcthorsebattery"})
        assert r.status_code == 302

        from ui.auth import SESSION_COOKIE

        token = setup_client.cookies.get(SESSION_COOKIE)
        assert token is not None

        conn = get_db(db_path)
        try:
            row = conn.execute("SELECT id FROM sessions WHERE id = ?", (token,)).fetchone()
            assert row is not None, "Session row should exist after login"
        finally:
            conn.close()

        r = setup_client.post("/logout")
        assert r.status_code in (200, 302)

        conn = get_db(db_path)
        try:
            row = conn.execute("SELECT id FROM sessions WHERE id = ?", (token,)).fetchone()
            assert row is None, "Session row should be deleted after logout"
        finally:
            conn.close()


# ---------------------------------------------------------------------------
# Unit tests -- session persistence across DB close/reopen
# ---------------------------------------------------------------------------


class TestSessionPersistence:
    def test_session_persists_across_db_close(self, db_path):
        """Sessions stored in SQLite survive a connection close/reopen."""
        import ui.auth as auth_module
        from server.db import get_db

        token = auth_module.create_session(db_path, user_agent="test-agent")
        assert len(token) == 64  # 32 bytes -> 64 hex chars

        conn = get_db(db_path)
        try:
            row = conn.execute("SELECT id FROM sessions WHERE id = ?", (token,)).fetchone()
            assert row is not None, "Session not found after DB close/reopen"
            assert row["id"] == token
        finally:
            conn.close()
