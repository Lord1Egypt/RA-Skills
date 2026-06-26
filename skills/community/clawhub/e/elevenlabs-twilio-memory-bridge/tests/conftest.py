"""Shared fixtures for ClawHub review remediation tests.

Provides app instances with various ADMIN_API_KEY configurations
and isolated data directories for filesystem-backed persistence.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

import app as app_module
import memory as memory_module


@pytest.fixture()
def tmp_data_dir(tmp_path, monkeypatch):
    """Redirect DATA_DIR to a temporary directory so tests don't pollute the real filesystem."""
    monkeypatch.setattr(memory_module, "DATA_DIR", tmp_path)
    return tmp_path


@pytest.fixture()
def configured_app(tmp_data_dir, monkeypatch):  # noqa: ARG001
    """Return a TestClient whose app has ADMIN_API_KEY set to a known value.

    The key is ``"test-secret-key"`` — tests that need a specific key should
    use the ``configured_client_factory`` fixture instead.
    """
    monkeypatch.setattr(app_module, "ADMIN_API_KEY", "test-secret-key")
    return TestClient(app_module.app, raise_server_exceptions=False)


@pytest.fixture()
def unconfigured_app(tmp_data_dir, monkeypatch):  # noqa: ARG001
    """Return a TestClient whose app has ADMIN_API_KEY empty (unconfigured)."""
    monkeypatch.setattr(app_module, "ADMIN_API_KEY", "")
    return TestClient(app_module.app, raise_server_exceptions=False)


@pytest.fixture()
def configured_client_factory(tmp_data_dir, monkeypatch):  # noqa: ARG001
    """Factory fixture: returns a (client, key) tuple for a given ADMIN_API_KEY value."""

    def _make(api_key: str):
        monkeypatch.setattr(app_module, "ADMIN_API_KEY", api_key)
        client = TestClient(app_module.app, raise_server_exceptions=False)
        return client, api_key

    return _make
