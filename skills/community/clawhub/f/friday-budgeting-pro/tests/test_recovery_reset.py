"""
tests/test_recovery_reset.py — Tests for the recovery-file password reset flow (#60).

Covers:
  - POST /forgot with valid username → recovery.txt created with mode 0600
  - POST /forgot with unknown username → same success page (no username leak)
  - POST /reset with valid token → password updated, recovery.txt deleted,
    sessions invalidated, redirect to /login?reset=1
  - POST /reset with expired token → rejected (mock time)
  - POST /reset with invalid token → rejected
  - POST /reset with password too short → rejected
"""

from __future__ import annotations

import stat
import time
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_path(tmp_path: Path, monkeypatch) -> Path:
    """Initialise a fresh SQLite DB in tmp_path and monkeypatch paths."""
    import server.paths as paths
    from server.db import init_db

    db = tmp_path / "test_recovery.db"
    init_db(db)

    monkeypatch.setattr(paths, "DB_PATH", db)
    # Redirect APP_DIR so recovery.txt doesn't touch the real ~/.friday-bp
    monkeypatch.setattr(paths, "APP_DIR", tmp_path)
    return db


@pytest.fixture()
def client(db_path: Path) -> TestClient:
    from ui.server import app

    return TestClient(app, follow_redirects=False)


@pytest.fixture()
def setup_user(db_path: Path, client: TestClient) -> dict:
    """Create a user via the setup wizard and return user info."""
    r = client.post(
        "/setup/1",
        data={
            "username": "testuser",
            "password": "hunter2abc",
            "password_confirm": "hunter2abc",
        },
    )
    assert r.status_code == 200, f"Setup step 1 failed: {r.status_code}"
    r = client.post("/setup/2", data={"notification_pref": "openclaw"})
    assert r.status_code == 200
    r = client.post("/setup/3", data={"action": "skip"})
    assert r.status_code == 302
    return {"username": "testuser", "password": "hunter2abc"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _clear_tokens() -> None:
    """Clear the in-memory recovery token store between tests."""
    import ui.server as srv

    srv._recovery_tokens.clear()


# ---------------------------------------------------------------------------
# POST /forgot
# ---------------------------------------------------------------------------


class TestForgotPost:
    def test_recovery_txt_created(self, db_path, client, setup_user, tmp_path):
        """POST /forgot with a valid username writes recovery.txt with 0600 perms."""
        _clear_tokens()
        r = client.post("/forgot", data={"username": "testuser"})
        assert r.status_code == 200
        assert b"recovery.txt" in r.content

        recovery_path = tmp_path / "recovery.txt"
        assert recovery_path.exists(), "recovery.txt was not created"

        # Token content should be non-empty hex
        token = recovery_path.read_text().strip()
        assert len(token) == 64, f"Expected 64-char hex token, got: {len(token)}"

        # Check file permissions: 0600
        file_mode = stat.S_IMODE(recovery_path.stat().st_mode)
        assert file_mode == 0o600, f"Expected 0600, got {oct(file_mode)}"

    def test_recovery_txt_perms_exact(self, db_path, client, setup_user, tmp_path):
        """recovery.txt must have exactly 0600 — not 0644, not 0400."""
        _clear_tokens()
        client.post("/forgot", data={"username": "testuser"})
        recovery_path = tmp_path / "recovery.txt"
        assert recovery_path.exists()
        file_mode = stat.S_IMODE(recovery_path.stat().st_mode)
        assert file_mode == 0o600

    def test_unknown_username_same_success_page(self, db_path, client, setup_user, tmp_path):
        """POST /forgot with an unknown username returns the same success page (no enumeration)."""
        _clear_tokens()
        r = client.post("/forgot", data={"username": "no_such_user"})
        assert r.status_code == 200
        # Page renders without error — same sent=True appearance expected
        # recovery.txt should NOT be created
        recovery_path = tmp_path / "recovery.txt"
        assert not recovery_path.exists(), "recovery.txt should not be created for unknown user"

    def test_token_stored_in_memory(self, db_path, client, setup_user, tmp_path):
        """A token should be stored in the in-memory dict after POST /forgot."""
        import ui.server as srv

        _clear_tokens()
        client.post("/forgot", data={"username": "testuser"})
        recovery_path = tmp_path / "recovery.txt"
        token = recovery_path.read_text().strip()
        assert token in srv._recovery_tokens


# ---------------------------------------------------------------------------
# POST /reset — valid token
# ---------------------------------------------------------------------------


class TestResetPostValid:
    def test_password_updated(self, db_path, client, setup_user, tmp_path):
        """POST /reset with a valid token updates the user's password."""
        from ui.auth import get_user_by_username, verify_password

        _clear_tokens()

        client.post("/forgot", data={"username": "testuser"})
        recovery_path = tmp_path / "recovery.txt"
        token = recovery_path.read_text().strip()

        r = client.post("/reset", data={"token": token, "new_password": "newpass12345"})
        assert r.status_code == 302
        assert r.headers["location"] == "/login?reset=1"

        # Verify new password works
        user = get_user_by_username(db_path, "testuser")
        assert user is not None
        assert verify_password("newpass12345", user["password_hash"])

    def test_recovery_txt_deleted(self, db_path, client, setup_user, tmp_path):
        """POST /reset with valid token deletes recovery.txt."""
        _clear_tokens()
        client.post("/forgot", data={"username": "testuser"})
        recovery_path = tmp_path / "recovery.txt"
        token = recovery_path.read_text().strip()

        client.post("/reset", data={"token": token, "new_password": "newpass12345"})
        assert not recovery_path.exists(), "recovery.txt should be deleted after reset"

    def test_sessions_invalidated(self, db_path, client, setup_user, tmp_path):
        """POST /reset with valid token deletes all sessions for that user."""
        from server.db import get_db

        _clear_tokens()

        # Log in first to create a session
        login_r = client.post("/login", data={"username": "testuser", "password": "hunter2abc"})
        assert login_r.status_code == 302

        # Confirm there's a session in the DB
        conn = get_db(db_path)
        try:
            count_before = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        finally:
            conn.close()
        assert count_before > 0

        # Now reset the password
        client.post("/forgot", data={"username": "testuser"})
        recovery_path = tmp_path / "recovery.txt"
        token = recovery_path.read_text().strip()
        client.post("/reset", data={"token": token, "new_password": "newpass12345"})

        # Sessions for testuser should be gone
        conn = get_db(db_path)
        try:
            count_after = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        finally:
            conn.close()
        assert count_after == 0, "Sessions should be invalidated after password reset"

    def test_token_removed_from_store(self, db_path, client, setup_user, tmp_path):
        """Token should be removed from memory after successful reset."""
        import ui.server as srv

        _clear_tokens()

        client.post("/forgot", data={"username": "testuser"})
        recovery_path = tmp_path / "recovery.txt"
        token = recovery_path.read_text().strip()

        client.post("/reset", data={"token": token, "new_password": "newpass12345"})
        assert token not in srv._recovery_tokens


# ---------------------------------------------------------------------------
# POST /reset — expired token
# ---------------------------------------------------------------------------


class TestResetPostExpired:
    def test_expired_token_rejected(self, db_path, client, setup_user, tmp_path):
        """POST /reset with an expired token is rejected."""

        _clear_tokens()

        client.post("/forgot", data={"username": "testuser"})
        recovery_path = tmp_path / "recovery.txt"
        token = recovery_path.read_text().strip()

        # Wind time forward past the 10-minute TTL
        future_time = time.time() + 601
        with patch("time.time", return_value=future_time):
            r = client.post("/reset", data={"token": token, "new_password": "newpass12345"})

        assert r.status_code == 200
        assert b"expired" in r.content.lower()

    def test_expired_token_not_accepted_for_password_change(
        self, db_path, client, setup_user, tmp_path
    ):
        """Expired token must not change the password."""
        from ui.auth import get_user_by_username, verify_password

        _clear_tokens()

        client.post("/forgot", data={"username": "testuser"})
        recovery_path = tmp_path / "recovery.txt"
        token = recovery_path.read_text().strip()

        future_time = time.time() + 601
        with patch("time.time", return_value=future_time):
            client.post("/reset", data={"token": token, "new_password": "newpass12345"})

        # Original password should still work
        user = get_user_by_username(db_path, "testuser")
        assert verify_password("hunter2abc", user["password_hash"])


# ---------------------------------------------------------------------------
# POST /reset — invalid token
# ---------------------------------------------------------------------------


class TestResetPostInvalid:
    def test_invalid_token_rejected(self, db_path, client, setup_user, tmp_path):
        """POST /reset with a random/invalid token is rejected."""
        _clear_tokens()
        r = client.post(
            "/reset",
            data={
                "token": "aabbccddeeff" * 5 + "aabb",  # 64 hex chars, not in store
                "new_password": "newpass12345",
            },
        )
        assert r.status_code == 200
        assert b"invalid" in r.content.lower() or b"expired" in r.content.lower()

    def test_empty_token_rejected(self, db_path, client, setup_user, tmp_path):
        """POST /reset with an empty token is rejected."""
        _clear_tokens()
        r = client.post("/reset", data={"token": "", "new_password": "newpass12345"})
        assert r.status_code == 200
        assert b"invalid" in r.content.lower() or b"expired" in r.content.lower()


# ---------------------------------------------------------------------------
# POST /reset — short password
# ---------------------------------------------------------------------------


class TestResetPostShortPassword:
    def test_short_password_rejected(self, db_path, client, setup_user, tmp_path):
        """POST /reset rejects passwords shorter than 8 characters."""
        _clear_tokens()
        client.post("/forgot", data={"username": "testuser"})
        recovery_path = tmp_path / "recovery.txt"
        token = recovery_path.read_text().strip()

        r = client.post("/reset", data={"token": token, "new_password": "short"})
        assert r.status_code == 200
        assert b"8" in r.content  # error message mentions 8 characters
