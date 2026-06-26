"""
tests/test_rules_ui.py — Tests for issue #172: Rules list UI in Settings page.

Covers:
  - GET /settings (authed) → 200 with rules table present
  - HTML contains rule names from seeded default rules
  - Disabled rule shows 'disabled' in HTML
  - Default rule shows 'default' badge text
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

    uid = create_user(db_path, "testuser", "testpassword1")
    token = create_session(db_path, user_agent="pytest", user_id=uid)

    client = TestClient(app, follow_redirects=False)
    client.cookies.set(SESSION_COOKIE, token)
    return client, uid


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestRulesUI:
    def test_get_settings_returns_200(self, authed_client):
        """GET /settings (authed) returns 200."""
        client, _ = authed_client
        r = client.get("/settings")
        assert r.status_code == 200

    def test_get_settings_has_rules_table(self, authed_client):
        """GET /settings includes the Classification Rules section and a table."""
        client, _ = authed_client
        r = client.get("/settings")
        assert r.status_code == 200
        assert "Classification Rules" in r.text
        assert "<table" in r.text

    def test_get_settings_shows_pending_skip(self, authed_client):
        """Default rule 'Pending skip' appears in the settings page."""
        client, _ = authed_client
        r = client.get("/settings")
        assert r.status_code == 200
        assert "Pending skip" in r.text

    def test_get_settings_shows_internal_transfer(self, authed_client):
        """Default rule 'Internal transfer' appears in the settings page."""
        client, _ = authed_client
        r = client.get("/settings")
        assert r.status_code == 200
        assert "Internal transfer" in r.text

    def test_get_settings_enabled_rule_shows_enabled(self, authed_client):
        """Enabled rules are shown with 'enabled' status text."""
        client, _ = authed_client
        r = client.get("/settings")
        assert r.status_code == 200
        assert "enabled" in r.text

    def test_disabled_rule_shows_disabled(self, db_path: Path, authed_client):
        """A disabled rule shows 'disabled' in the settings page."""
        from server.main import disable_rule, list_rules

        # Disable the first rule
        rules = list_rules().get("rules", [])
        assert rules, "Expected seeded default rules"
        first_rule_id = rules[0]["id"]
        disable_rule(first_rule_id)

        client, _ = authed_client
        r = client.get("/settings")
        assert r.status_code == 200
        assert "disabled" in r.text

    def test_default_rule_shows_default_badge(self, authed_client):
        """Default rules are labelled with 'default' badge text."""
        client, _ = authed_client
        r = client.get("/settings")
        assert r.status_code == 200
        assert "default" in r.text

    def test_rules_shown_in_priority_order(self, authed_client):
        """Priority numbers appear in the rendered HTML in ascending order."""
        client, _ = authed_client
        r = client.get("/settings")
        assert r.status_code == 200
        # Priority 1 (Pending skip) should appear before priority 50 (Bank fees)
        idx_1 = r.text.find(">1<")
        idx_50 = r.text.find(">50<")
        assert idx_1 != -1, "Priority 1 not found"
        assert idx_50 != -1, "Priority 50 not found"
        assert idx_1 < idx_50, "Priority 1 should appear before priority 50"

    def test_no_edit_controls_present(self, authed_client):
        """Rules table must not contain edit buttons or input controls."""
        client, _ = authed_client
        r = client.get("/settings")
        assert r.status_code == 200
        # Check that no edit/delete buttons are in the rules section
        # (The form for currency/timezone settings is fine)
        # We look for buttons labelled Edit/Delete near rule content
        assert "Edit rule" not in r.text
        assert "Delete rule" not in r.text
