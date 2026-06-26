"""
tests/test_get_ui_url.py — Tests for the get_ui_url MCP tool.
"""

from __future__ import annotations

import pytest

from server.main import get_ui_url


class TestGetUiUrl:
    def test_no_args_returns_base_url(self, monkeypatch):
        """Calling get_ui_url() with no args returns the base URL on default port."""
        monkeypatch.delenv("FRIDAY_BP_UI_PORT", raising=False)
        result = get_ui_url()
        assert result == {"url": "http://127.0.0.1:6789"}

    def test_no_args_respects_env_port(self, monkeypatch):
        """FRIDAY_BP_UI_PORT env var is honoured."""
        monkeypatch.setenv("FRIDAY_BP_UI_PORT", "9000")
        result = get_ui_url()
        assert result == {"url": "http://127.0.0.1:9000"}

    def test_page_ledgers(self, monkeypatch):
        """page='ledgers' appends /ledgers to the URL."""
        monkeypatch.delenv("FRIDAY_BP_UI_PORT", raising=False)
        result = get_ui_url(page="ledgers")
        assert result == {"url": "http://127.0.0.1:6789/ledgers"}

    def test_page_accounts(self, monkeypatch):
        monkeypatch.delenv("FRIDAY_BP_UI_PORT", raising=False)
        assert get_ui_url(page="accounts") == {"url": "http://127.0.0.1:6789/accounts"}

    def test_page_profile(self, monkeypatch):
        monkeypatch.delenv("FRIDAY_BP_UI_PORT", raising=False)
        assert get_ui_url(page="profile") == {"url": "http://127.0.0.1:6789/profile"}

    def test_page_dashboard(self, monkeypatch):
        monkeypatch.delenv("FRIDAY_BP_UI_PORT", raising=False)
        assert get_ui_url(page="dashboard") == {"url": "http://127.0.0.1:6789/dashboard"}

    def test_invalid_page_raises(self, monkeypatch):
        """An invalid page argument raises ValueError."""
        monkeypatch.delenv("FRIDAY_BP_UI_PORT", raising=False)
        with pytest.raises(ValueError, match="page must be one of"):
            get_ui_url(page="settings")

    def test_invalid_port_env_falls_back_to_default(self, monkeypatch):
        """A non-integer FRIDAY_BP_UI_PORT silently falls back to 6789."""
        monkeypatch.setenv("FRIDAY_BP_UI_PORT", "not-a-number")
        result = get_ui_url()
        assert result == {"url": "http://127.0.0.1:6789"}
