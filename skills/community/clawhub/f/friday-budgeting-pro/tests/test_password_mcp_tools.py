"""
tests/test_password_mcp_tools.py — Tests for set_ui_password / reset_ui_password MCP tools.

Covers:
  - set_ui_password with valid old + new (both >= 8 chars) → ok, password verifies
  - set_ui_password with wrong old_password → error
  - set_ui_password without old_password when one exists → error
  - set_ui_password with too-short new password → error
  - set_ui_password with no active user → error
  - reset_ui_password → recovery.txt created with 0600 perms, recovery_url contains token
  - reset_ui_password with no active user → error
"""

from __future__ import annotations

import stat
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_path(tmp_path: Path, monkeypatch) -> Path:
    """Initialise a fresh SQLite DB in tmp_path and monkeypatch server.paths."""
    import server.paths as paths
    from server.db import init_db

    db = tmp_path / "test_pw_mcp.db"
    init_db(db)

    monkeypatch.setattr(paths, "DB_PATH", db)
    monkeypatch.setattr(paths, "APP_DIR", tmp_path)

    # Also patch server.main's reference to server.paths so the tools see the
    # monkeypatched values via server.paths.DB_PATH / server.paths.APP_DIR.
    return db


@pytest.fixture()
def user(db_path: Path) -> dict:
    """Create a user in the test DB and return {user_id, username, password}."""
    from ui.auth import create_session, create_user

    user_id = create_user(db_path, "testuser", "password123")
    # Create an active session so get_active_user_id() can find this user.
    create_session(db_path, user_agent="pytest", user_id=user_id)
    return {"user_id": user_id, "username": "testuser", "password": "password123"}


def _clear_tokens() -> None:
    """Clear the shared in-memory recovery token store between tests."""
    from ui.auth import _recovery_tokens

    _recovery_tokens.clear()


# ---------------------------------------------------------------------------
# set_ui_password
# ---------------------------------------------------------------------------


class TestSetUiPassword:
    def test_success_updates_password(self, db_path, user):
        """Valid old + new password → status ok, new password verifies."""
        from server.main import set_ui_password
        from ui.auth import get_user_by_id, verify_password

        result = set_ui_password("newpass99", old_password="password123")
        assert result == {"status": "ok"}, f"Unexpected result: {result}"

        updated = get_user_by_id(db_path, user["user_id"])
        assert verify_password("newpass99", updated["password_hash"])

    def test_wrong_old_password(self, db_path, user):
        """Wrong old_password → error."""
        from server.main import set_ui_password

        result = set_ui_password("newpass99", old_password="wrongpassword")
        assert result["status"] == "error"
        assert "old password" in result["message"].lower()

    def test_missing_old_password(self, db_path, user):
        """old_password omitted when user has a password → error."""
        from server.main import set_ui_password

        result = set_ui_password("newpass99")
        assert result["status"] == "error"
        assert "old password" in result["message"].lower()

    def test_too_short_new_password(self, db_path, user):
        """new_password shorter than 8 chars → error before any DB access."""
        from server.main import set_ui_password

        result = set_ui_password("short", old_password="password123")
        assert result["status"] == "error"
        assert "short" in result["message"].lower() or "8" in result["message"]

    def test_no_active_user(self, db_path, monkeypatch):
        """No active session / user → error."""
        import ui.auth as _auth
        from server.main import set_ui_password

        monkeypatch.setattr(_auth, "get_active_user_id", lambda _: None)

        # Also patch server.main's imported reference
        import server.main as _main

        monkeypatch.setattr(_main, "get_active_user_id", lambda _: None)

        result = set_ui_password("newpass99", old_password="password123")
        assert result["status"] == "error"
        assert "logged in" in result["message"].lower()


# ---------------------------------------------------------------------------
# reset_ui_password
# ---------------------------------------------------------------------------


class TestResetUiPassword:
    def test_recovery_txt_created(self, db_path, user, tmp_path):
        """reset_ui_password creates recovery.txt with mode 0600."""
        _clear_tokens()
        from server.main import reset_ui_password

        result = reset_ui_password()
        assert result["status"] == "ok", f"Unexpected: {result}"
        assert "recovery_url" in result

        recovery_path = tmp_path / "recovery.txt"
        assert recovery_path.exists(), "recovery.txt was not created"

        mode = stat.S_IMODE(recovery_path.stat().st_mode)
        assert mode == 0o600, f"Expected 0600, got {oct(mode)}"

    def test_recovery_url_contains_token(self, db_path, user, tmp_path):
        """The recovery_url must contain the written token."""
        _clear_tokens()
        from server.main import reset_ui_password

        result = reset_ui_password()
        recovery_path = tmp_path / "recovery.txt"
        token = recovery_path.read_text().strip()

        assert len(token) == 64, f"Token should be 64 hex chars, got {len(token)}"
        assert token in result["recovery_url"]

    def test_token_stored_in_memory(self, db_path, user, tmp_path):
        """Token is stored in the shared _recovery_tokens dict."""
        _clear_tokens()
        from server.main import reset_ui_password
        from ui.auth import _recovery_tokens

        reset_ui_password()
        recovery_path = tmp_path / "recovery.txt"
        token = recovery_path.read_text().strip()
        assert token in _recovery_tokens

    def test_recovery_url_default_port(self, db_path, user, monkeypatch):
        """recovery_url uses port 6789 when FRIDAY_BP_UI_PORT is not set."""
        _clear_tokens()
        import os

        from server.main import reset_ui_password

        monkeypatch.delitem(os.environ, "FRIDAY_BP_UI_PORT", raising=False)
        result = reset_ui_password()
        assert "127.0.0.1:6789" in result["recovery_url"]

    def test_no_active_user(self, db_path, monkeypatch):
        """No active session / user → error."""
        _clear_tokens()
        import server.main as _main

        monkeypatch.setattr(_main, "get_active_user_id", lambda _: None)

        result = _main.reset_ui_password()
        assert result["status"] == "error"
        assert "logged in" in result["message"].lower()
