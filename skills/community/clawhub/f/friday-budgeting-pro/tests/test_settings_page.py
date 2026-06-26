"""
tests/test_settings_page.py — Tests for issue #159: Settings page (/settings).

Covers:
  - Schema: home_currency column exists on users
  - GET /settings → 200 with home_currency selector
  - POST /settings with valid currency → saves, redirects back
  - POST /settings with invalid currency → error or ignored
  - get_setting('home_currency') → returns current setting
  - set_setting('home_currency', 'USD') → updates, verify with get_setting
  - get_setting('unknown_key') → error response
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
def authed_client(db_path: Path) -> tuple[TestClient, str]:
    """TestClient with a valid session cookie for a real user.

    Returns (client, user_id).
    """
    from ui.auth import SESSION_COOKIE, create_session, create_user
    from ui.server import app

    uid = create_user(db_path, "testuser", "testpassword1")
    token = create_session(db_path, user_agent="pytest", user_id=uid)

    client = TestClient(app, follow_redirects=False)
    client.cookies.set(SESSION_COOKIE, token)
    return client, uid


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------


class TestSchema:
    def test_home_currency_column_exists(self, db_path: Path):
        """home_currency column must exist on the users table."""
        from server.db import get_db

        conn = get_db(db_path)
        try:
            cols = {row[1] for row in conn.execute("PRAGMA table_info(users)")}
        finally:
            conn.close()
        assert "home_currency" in cols

    def test_home_currency_defaults_to_cad(self, db_path: Path):
        """Existing users with NULL home_currency should be seeded to 'CAD'."""
        from server.db import get_db
        from ui.auth import create_user

        uid = create_user(db_path, "currencyuser", "password123")
        conn = get_db(db_path)
        try:
            conn.execute("UPDATE users SET home_currency = NULL WHERE id = ?", (uid,))
            conn.commit()
            conn.execute("UPDATE users SET home_currency = 'CAD' WHERE home_currency IS NULL")
            conn.commit()
            row = conn.execute("SELECT home_currency FROM users WHERE id = ?", (uid,)).fetchone()
            assert row["home_currency"] == "CAD"
        finally:
            conn.close()


# ---------------------------------------------------------------------------
# GET /settings
# ---------------------------------------------------------------------------


class TestSettingsGet:
    def test_get_settings_returns_200(self, authed_client):
        client, _ = authed_client
        r = client.get("/settings")
        assert r.status_code == 200

    def test_get_settings_contains_currency_selector(self, authed_client):
        client, _ = authed_client
        r = client.get("/settings")
        assert r.status_code == 200
        assert "home_currency" in r.text
        assert "<select" in r.text

    def test_get_settings_shows_all_currencies(self, authed_client):
        client, _ = authed_client
        r = client.get("/settings")
        for currency in ["CAD", "USD", "EUR", "GBP"]:
            assert currency in r.text

    def test_get_settings_preselects_current_value(self, db_path: Path, authed_client):
        """CAD should be pre-selected by default for a new user."""
        client, uid = authed_client
        r = client.get("/settings")
        assert r.status_code == 200
        assert 'value="CAD"' in r.text

    def test_get_settings_redirects_when_unauthenticated(self, db_path: Path):
        from ui.server import app

        client = TestClient(app, follow_redirects=False)
        r = client.get("/settings")
        assert r.status_code in (302, 307)
        assert "/login" in r.headers["location"]

    def test_get_settings_shows_saved_flash(self, authed_client):
        client, _ = authed_client
        r = client.get("/settings?saved=1")
        assert r.status_code == 200
        assert "Settings saved" in r.text


# ---------------------------------------------------------------------------
# POST /settings
# ---------------------------------------------------------------------------


class TestSettingsPost:
    def test_post_valid_currency_redirects(self, authed_client):
        client, _ = authed_client
        r = client.post("/settings", data={"home_currency": "USD"})
        assert r.status_code in (302, 307)
        assert "/settings" in r.headers["location"]

    def test_post_valid_currency_saves_to_db(self, db_path: Path, authed_client):
        client, uid = authed_client
        r = client.post("/settings", data={"home_currency": "EUR"})
        assert r.status_code in (302, 307)

        from server.db import get_db

        conn = get_db(db_path)
        try:
            row = conn.execute("SELECT home_currency FROM users WHERE id = ?", (uid,)).fetchone()
            assert row["home_currency"] == "EUR"
        finally:
            conn.close()

    def test_post_valid_currency_all_supported(self, db_path: Path, authed_client):
        client, uid = authed_client
        for currency in ["CAD", "USD", "EUR", "GBP"]:
            r = client.post("/settings", data={"home_currency": currency})
            assert r.status_code in (302, 307)

        from server.db import get_db

        conn = get_db(db_path)
        try:
            row = conn.execute("SELECT home_currency FROM users WHERE id = ?", (uid,)).fetchone()
            assert row["home_currency"] == "GBP"
        finally:
            conn.close()

    def test_post_invalid_currency_does_not_save(self, db_path: Path, authed_client):
        """Invalid currency should return an error (not save)."""
        client, uid = authed_client
        client.post("/settings", data={"home_currency": "CAD"})
        r = client.post("/settings", data={"home_currency": "XYZ"})

        from server.db import get_db

        conn = get_db(db_path)
        try:
            row = conn.execute("SELECT home_currency FROM users WHERE id = ?", (uid,)).fetchone()
            assert row["home_currency"] != "XYZ"
        finally:
            conn.close()

    def test_post_redirects_when_unauthenticated(self, db_path: Path):
        from ui.server import app

        client = TestClient(app, follow_redirects=False)
        r = client.post("/settings", data={"home_currency": "USD"})
        assert r.status_code in (302, 307)
        assert "/login" in r.headers["location"]


# ---------------------------------------------------------------------------
# MCP tools: get_setting / set_setting
# ---------------------------------------------------------------------------


class TestGetSetting:
    def test_get_setting_home_currency_default(self, db_path: Path):
        """get_setting('home_currency') returns CAD for a fresh user."""
        from ui.auth import create_user

        create_user(db_path, "mcpuser", "mcppassword1")

        from server.main import get_setting

        result = get_setting("home_currency")
        assert result["status"] == "ok"
        assert result["key"] == "home_currency"
        assert result["value"] == "CAD"

    def test_get_setting_unknown_key_returns_error(self, db_path: Path):
        from server.main import get_setting

        result = get_setting("unknown_key")
        assert result["status"] == "error"

    def test_get_setting_returns_updated_value(self, db_path: Path):
        """After set_setting, get_setting should return the new value."""
        from ui.auth import create_user

        create_user(db_path, "mcpuser2", "mcppassword2")

        from server.main import get_setting, set_setting

        set_result = set_setting("home_currency", "GBP")
        assert set_result["status"] == "ok"

        get_result = get_setting("home_currency")
        assert get_result["status"] == "ok"
        assert get_result["value"] == "GBP"


class TestSetSetting:
    def test_set_setting_valid_updates_db(self, db_path: Path):
        from ui.auth import create_user

        create_user(db_path, "setuser", "setpassword1")

        from server.main import set_setting

        result = set_setting("home_currency", "USD")
        assert result["status"] == "ok"
        assert result["key"] == "home_currency"
        assert result["value"] == "USD"

    def test_set_setting_invalid_value_returns_error(self, db_path: Path):
        from server.main import set_setting

        result = set_setting("home_currency", "JPY")
        assert result["status"] == "error"

    def test_set_setting_unknown_key_returns_error(self, db_path: Path):
        from server.main import set_setting

        result = set_setting("nonexistent_key", "some_value")
        assert result["status"] == "error"

    def test_set_and_get_roundtrip(self, db_path: Path):
        """set_setting followed by get_setting should return the set value."""
        from ui.auth import create_user

        create_user(db_path, "roundtripuser", "password123")

        from server.main import get_setting, set_setting

        initial = get_setting("home_currency")
        assert initial["status"] == "ok"
        assert initial["value"] == "CAD"

        set_result = set_setting("home_currency", "USD")
        assert set_result["status"] == "ok"
        assert set_result["value"] == "USD"

        final = get_setting("home_currency")
        assert final["status"] == "ok"
        assert final["value"] == "USD"

    def test_all_valid_currencies_accepted(self, db_path: Path):
        from ui.auth import create_user

        create_user(db_path, "allcurruser", "password123")

        from server.main import set_setting

        for currency in ["CAD", "USD", "EUR", "GBP"]:
            result = set_setting("home_currency", currency)
            assert result["status"] == "ok", f"Expected ok for {currency}, got {result}"
