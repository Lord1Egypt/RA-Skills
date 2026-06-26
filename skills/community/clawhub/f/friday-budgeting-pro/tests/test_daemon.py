"""
tests/test_daemon.py — Tests for server.daemon and ui.server (issue #52).

Coverage:
  - server.daemon imports without error
  - ui.server.app is a FastAPI instance
  - GET /healthz → 200, body {"status": "ok"}
  - daemon.main() respects FRIDAY_BP_UI_PORT env var (uvicorn.Server.serve is
    stubbed to a coroutine that records host/port and exits immediately — no
    real server is started)
  - 0.0.0.0 / public binds are NOT used (complements test_no_public_bind.py)
"""

from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient

# ---------------------------------------------------------------------------
# Import sanity checks
# ---------------------------------------------------------------------------


def test_daemon_module_imports():
    """server.daemon must be importable without side-effects."""
    import server.daemon  # noqa: F401


def test_ui_server_module_imports():
    """ui.server must be importable and expose a FastAPI `app`."""
    from fastapi import FastAPI

    from ui.server import app

    assert isinstance(app, FastAPI)


# ---------------------------------------------------------------------------
# /healthz endpoint
# ---------------------------------------------------------------------------


def test_healthz_returns_200_ok():
    """GET /healthz → HTTP 200, body {"status": "ok"}."""
    from ui.server import app

    client = TestClient(app)
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# FRIDAY_BP_UI_PORT env-var respected by daemon.main()
# ---------------------------------------------------------------------------


def test_main_respects_friday_bp_ui_port(monkeypatch, tmp_path):
    """daemon.main() must pass FRIDAY_BP_UI_PORT to uvicorn.Config."""

    captured: dict[str, Any] = {}

    # Stub out heavy I/O calls that main() makes before starting uvicorn.
    monkeypatch.setattr("server.paths.ensure_app_dir", lambda: None)
    monkeypatch.setattr("server.paths.audit_permissions", lambda: None)
    monkeypatch.setattr("server.db.init_db", lambda path: None)

    # init_crypto may raise in CI (no Keychain) — daemon already handles that,
    # but we stub it to keep the test hermetic.
    monkeypatch.setattr("server.crypto.init_crypto", lambda: None)

    # Stub uvicorn.Server.serve: record host/port then return immediately.
    async def fake_serve(self):  # noqa: ANN001
        captured["host"] = self.config.host
        captured["port"] = self.config.port

    monkeypatch.setattr("uvicorn.Server.serve", fake_serve)

    test_port = 19999
    monkeypatch.setenv("FRIDAY_BP_UI_PORT", str(test_port))

    import server.daemon as daemon

    daemon.main()

    assert (
        captured.get("port") == test_port
    ), f"Expected uvicorn to bind on port {test_port}, got {captured.get('port')}"


# ---------------------------------------------------------------------------
# 127.0.0.1 — no public binds in daemon or ui code
# ---------------------------------------------------------------------------


def test_daemon_binds_localhost_only(monkeypatch):
    """The host passed to uvicorn.Config must be 127.0.0.1, never 0.0.0.0."""

    captured: dict[str, Any] = {}

    monkeypatch.setattr("server.paths.ensure_app_dir", lambda: None)
    monkeypatch.setattr("server.paths.audit_permissions", lambda: None)
    monkeypatch.setattr("server.db.init_db", lambda path: None)
    monkeypatch.setattr("server.crypto.init_crypto", lambda: None)

    async def fake_serve(self):  # noqa: ANN001
        captured["host"] = self.config.host

    monkeypatch.setattr("uvicorn.Server.serve", fake_serve)

    # Remove any port override so we use the default path.
    monkeypatch.delenv("FRIDAY_BP_UI_PORT", raising=False)

    import server.daemon as daemon

    daemon.main()

    assert (
        captured.get("host") == "127.0.0.1"
    ), f"Daemon must bind to 127.0.0.1 only, got {captured.get('host')!r}"
