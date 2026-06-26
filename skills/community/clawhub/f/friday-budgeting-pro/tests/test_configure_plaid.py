"""
tests/test_configure_plaid.py — Tests for the configure_plaid MCP tool.
"""

from __future__ import annotations

import logging
import os
import stat

import pytest

import server.main as main_module
from server.main import configure_plaid

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def patch_project_root(tmp_path, monkeypatch):
    """Redirect all .env writes to tmp_path so tests never touch the real repo."""
    monkeypatch.setattr(main_module, "project_root", tmp_path)
    yield tmp_path


@pytest.fixture(autouse=True)
def clean_environ():
    """Remove Plaid env vars before/after each test to avoid cross-test pollution."""
    keys = ("PLAID_CLIENT_ID", "PLAID_SECRET", "PLAID_ENV")
    saved = {k: os.environ.pop(k, None) for k in keys}
    yield
    for k, v in saved.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestConfigurePlaid:
    def test_writes_env_file_and_returns_ok(self, tmp_path):
        result = configure_plaid("abc", "xyz", "sandbox")

        assert result == {"ok": True, "env": "sandbox"}
        env_file = tmp_path / ".env"
        assert env_file.exists()
        content = env_file.read_text()
        assert "PLAID_CLIENT_ID=abc" in content
        assert "PLAID_SECRET=xyz" in content
        assert "PLAID_ENV=sandbox" in content

    def test_env_file_mode_is_0o600(self, tmp_path):
        configure_plaid("abc", "xyz", "sandbox")
        env_file = tmp_path / ".env"
        mode = stat.S_IMODE(env_file.stat().st_mode)
        assert mode == 0o600

    def test_invalid_env_raises_value_error(self):
        with pytest.raises(ValueError, match="env must be one of"):
            configure_plaid("abc", "xyz", "staging")

    def test_empty_client_id_raises_value_error(self):
        with pytest.raises(ValueError, match="client_id must be non-empty"):
            configure_plaid("", "xyz", "sandbox")

    def test_empty_secret_raises_value_error(self):
        with pytest.raises(ValueError, match="secret must be non-empty"):
            configure_plaid("abc", "", "sandbox")

    def test_os_environ_updated_after_call(self):
        configure_plaid("myid", "mysecret", "production")
        assert os.environ["PLAID_CLIENT_ID"] == "myid"
        assert os.environ["PLAID_SECRET"] == "mysecret"
        assert os.environ["PLAID_ENV"] == "production"

    def test_calling_twice_replaces_file(self, tmp_path):
        configure_plaid("first_id", "first_secret", "sandbox")
        configure_plaid("second_id", "second_secret", "production")

        env_file = tmp_path / ".env"
        content = env_file.read_text()

        # Only the second call's values should be present.
        assert "second_id" in content
        assert "second_secret" in content
        assert "production" in content
        assert "first_id" not in content
        assert "first_secret" not in content
        # Sanity: file is not just appended lines.
        assert content.count("PLAID_CLIENT_ID") == 1

    def test_secret_never_appears_in_stdout_stderr(self, tmp_path, capsys, caplog):
        secret = "super_secret_12345"
        with caplog.at_level(logging.DEBUG):
            configure_plaid("myid", secret, "sandbox")

        captured = capsys.readouterr()
        assert secret not in captured.out
        assert secret not in captured.err
        assert secret not in caplog.text

    def test_default_env_is_production(self, tmp_path):
        result = configure_plaid("myid", "mysecret")
        assert result["env"] == "production"
        content = (tmp_path / ".env").read_text()
        assert "PLAID_ENV=production" in content

    def test_development_env_accepted(self, tmp_path):
        result = configure_plaid("myid", "mysecret", "development")
        assert result == {"ok": True, "env": "development"}
