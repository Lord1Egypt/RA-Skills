"""
tests/test_timezone.py — Tests for issue #161: Timezone management.

Covers:
  - Schema: users.timezone column exists and defaults to 'America/Toronto'
  - GET /settings shows timezone selector
  - POST /settings saves new timezone
  - set_setting('timezone', ...) → updates
  - get_setting('timezone') → returns current setting
  - Profile page HTML has data-utc attributes (not pre-formatted dates)
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
    """TestClient with a valid session cookie for a real user."""
    from ui.auth import SESSION_COOKIE, create_session, create_user
    from ui.server import app

    uid = create_user(db_path, "tzuser", "testpassword1")
    token = create_session(db_path, user_agent="pytest", user_id=uid)

    client = TestClient(app, follow_redirects=False)
    client.cookies.set(SESSION_COOKIE, token)
    return client, uid


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------


class TestSchema:
    def test_timezone_column_exists(self, db_path: Path):
        """timezone column must exist on the users table."""
        from server.db import get_db

        conn = get_db(db_path)
        try:
            cols = {row[1] for row in conn.execute("PRAGMA table_info(users)")}
        finally:
            conn.close()
        assert "timezone" in cols

    def test_timezone_defaults_to_toronto(self, db_path: Path):
        """New users should have timezone seeded to 'America/Toronto'."""
        from server.db import get_db
        from ui.auth import create_user

        uid = create_user(db_path, "tzdefaultuser", "password123")
        conn = get_db(db_path)
        try:
            row = conn.execute("SELECT timezone FROM users WHERE id = ?", (uid,)).fetchone()
        finally:
            conn.close()
        assert row["timezone"] == "America/Toronto"


# ---------------------------------------------------------------------------
# GET /settings
# ---------------------------------------------------------------------------


class TestSettingsGet:
    def test_get_settings_contains_timezone_selector(self, authed_client):
        client, _ = authed_client
        resp = client.get("/settings")
        assert resp.status_code == 200
        assert "timezone" in resp.text.lower()

    def test_get_settings_shows_iana_options(self, authed_client):
        client, _ = authed_client
        resp = client.get("/settings")
        assert "America/Toronto" in resp.text
        assert "UTC" in resp.text

    def test_get_settings_preselects_current_timezone(self, db_path: Path, authed_client):
        """If user has UTC as timezone, it should be pre-selected."""
        from server.db import get_db

        client, uid = authed_client
        conn = get_db(db_path)
        try:
            conn.execute("UPDATE users SET timezone = 'UTC' WHERE id = ?", (uid,))
            conn.commit()
        finally:
            conn.close()

        resp = client.get("/settings")
        assert resp.status_code == 200
        # The UTC option should appear selected
        assert 'value="UTC"' in resp.text


# ---------------------------------------------------------------------------
# POST /settings
# ---------------------------------------------------------------------------


class TestSettingsPost:
    def test_post_settings_saves_timezone(self, db_path: Path, authed_client):
        """Posting a valid timezone saves it to the DB."""
        from server.db import get_db

        client, uid = authed_client
        resp = client.post(
            "/settings",
            data={"home_currency": "CAD", "timezone": "America/Los_Angeles"},
        )
        # Should redirect to /settings?saved=1
        assert resp.status_code in (302, 303)

        conn = get_db(db_path)
        try:
            row = conn.execute("SELECT timezone FROM users WHERE id = ?", (uid,)).fetchone()
        finally:
            conn.close()
        assert row["timezone"] == "America/Los_Angeles"

    def test_post_settings_without_timezone_keeps_existing(self, db_path: Path, authed_client):
        """Posting without a timezone field keeps the existing timezone."""
        from server.db import get_db

        client, uid = authed_client
        # Set a known timezone first
        conn = get_db(db_path)
        try:
            conn.execute("UPDATE users SET timezone = 'Europe/Berlin' WHERE id = ?", (uid,))
            conn.commit()
        finally:
            conn.close()

        resp = client.post(
            "/settings",
            data={"home_currency": "CAD"},  # no timezone field
        )
        assert resp.status_code in (302, 303)

        conn = get_db(db_path)
        try:
            row = conn.execute("SELECT timezone FROM users WHERE id = ?", (uid,)).fetchone()
        finally:
            conn.close()
        assert row["timezone"] == "Europe/Berlin"


# ---------------------------------------------------------------------------
# MCP tools: get_setting / set_setting
# ---------------------------------------------------------------------------


class TestMcpTimezoneTools:
    def test_get_setting_timezone_default(self, db_path: Path):
        """get_setting('timezone') returns America/Toronto for a fresh user."""
        from ui.auth import create_user

        create_user(db_path, "mcp_tz_user", "password123")

        from server.main import get_setting

        result = get_setting("timezone")
        assert result["status"] == "ok"
        assert result["key"] == "timezone"
        assert result["value"] == "America/Toronto"

    def test_set_setting_timezone(self, db_path: Path):
        """set_setting('timezone', 'Asia/Tokyo') updates and get_setting reflects it."""
        from ui.auth import create_user

        create_user(db_path, "mcp_tz_user2", "password123")

        from server.main import get_setting, set_setting

        result = set_setting("timezone", "Asia/Tokyo")
        assert result["status"] == "ok"
        assert result["value"] == "Asia/Tokyo"

        check = get_setting("timezone")
        assert check["value"] == "Asia/Tokyo"

    def test_set_setting_empty_timezone_rejected(self, db_path: Path):
        """set_setting('timezone', '') should return an error."""
        from ui.auth import create_user

        create_user(db_path, "mcp_tz_user3", "password123")

        from server.main import set_setting

        result = set_setting("timezone", "")
        assert result["status"] == "error"


# ---------------------------------------------------------------------------
# Profile page: data-utc rendering
# ---------------------------------------------------------------------------


FAKE_TS = 1779649905


def _render_profile_html_tz(monkeypatch, connections):
    """Return rendered HTML for /profile with fake auth + connections."""
    import ui.server as srv

    monkeypatch.setattr(srv, "_is_authenticated", lambda req: True)
    monkeypatch.setattr(srv, "_current_user_id", lambda req: "user-1")
    monkeypatch.setattr(srv, "_get_notification_pref", lambda: "openclaw")
    monkeypatch.setattr(srv, "_get_connections", lambda uid=None: connections)
    monkeypatch.setattr(srv, "_get_accounts", lambda uid=None: [])

    client = TestClient(srv.app, raise_server_exceptions=True)
    resp = client.get("/profile", follow_redirects=False)
    assert resp.status_code == 200
    return resp.text


class TestProfileDataUtc:
    def test_profile_has_data_utc_attribute(self, monkeypatch):
        """Profile page must include data-utc attribute for JS rendering."""
        connections = [
            {
                "id": "conn-1",
                "institution_name": "Test Bank",
                "status": "active",
                "last_synced_at": FAKE_TS,
            }
        ]
        html = _render_profile_html_tz(monkeypatch, connections)
        assert (
            f'data-utc="{FAKE_TS}"' in html
        ), f'data-utc attribute not found in profile HTML (expected data-utc="{FAKE_TS}")'

    def test_profile_has_datetime_local_class(self, monkeypatch):
        """Profile must use .datetime-local class for JS to target."""
        connections = [
            {
                "id": "conn-1",
                "institution_name": "Test Bank",
                "status": "active",
                "last_synced_at": FAKE_TS,
            }
        ]
        html = _render_profile_html_tz(monkeypatch, connections)
        assert "datetime-local" in html

    def test_profile_no_server_formatted_date_in_synced_cell(self, monkeypatch):
        """Profile page must NOT contain a pre-formatted date in the last_synced cell.

        The JS snippet in base.html does the formatting; server should only emit
        the raw integer as data-utc.
        """
        connections = [
            {
                "id": "conn-1",
                "institution_name": "Test Bank",
                "status": "active",
                "last_synced_at": FAKE_TS,
            }
        ]
        html = _render_profile_html_tz(monkeypatch, connections)
        # Server-side formatted strings like "May 24, 2026" must NOT appear
        # (only the raw int in data-utc= is expected)
        assert "May 24, 2026" not in html

    def test_profile_zero_ts_shows_never(self, monkeypatch):
        """When last_synced_at is 0 the template should show 'Never'."""
        connections = [
            {
                "id": "conn-2",
                "institution_name": "Empty Bank",
                "status": "active",
                "last_synced_at": 0,
            }
        ]
        html = _render_profile_html_tz(monkeypatch, connections)
        assert "Never" in html

    def test_base_html_has_datetime_js(self, monkeypatch):
        """base.html must include the JS snippet for datetime-local conversion."""
        connections = [
            {
                "id": "conn-1",
                "institution_name": "Test Bank",
                "status": "active",
                "last_synced_at": FAKE_TS,
            }
        ]
        html = _render_profile_html_tz(monkeypatch, connections)
        assert "datetime-local" in html
        assert "toLocaleString" in html
