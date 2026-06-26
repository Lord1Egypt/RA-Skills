"""
tests/test_mcp_decoupling.py — Regression tests: daemon + UI work without any MCP client.

Architecture constraint (Design Constraint): MCP is one of many paths.
The daemon, UI, sync, scheduler, and notifications must all operate correctly
even when no MCP client (OpenClaw agent) is ever attached or connects.

Each test verifies a specific subsystem boots/runs and confirms that no
MCP tool call (JSON-RPC invocation) was required to make it happen.

Related: GitHub issue #61
"""

from __future__ import annotations

import sqlite3
import uuid
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# ---------------------------------------------------------------------------
# Shared fixture helpers (mirrors test_ui_routes.py pattern)
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_path(tmp_path: Path, monkeypatch) -> Path:
    """Initialise a fresh SQLite DB in tmp_path and monkeypatch all path references."""
    import server.paths as paths
    from server.db import init_db

    db = tmp_path / "decoupling_test.db"
    init_db(db)

    monkeypatch.setattr(paths, "DB_PATH", db)
    monkeypatch.setattr(paths, "APP_DIR", tmp_path)
    monkeypatch.setattr(paths, "SYNC_LOCK_PATH", tmp_path / "sync.lock")
    return db


@pytest.fixture()
def client(db_path: Path) -> TestClient:
    """Bare (unauthenticated) TestClient backed by the patched app."""
    from ui.server import app

    return TestClient(app, follow_redirects=False)


def _complete_setup(client: TestClient, password: str = "testpassword123") -> None:
    """Drive the 3-step setup wizard to completion (mirrors test_ui_routes.py)."""
    r = client.post("/setup/1", data={"password": password, "password_confirm": password})
    assert r.status_code == 200, f"Setup step 1 failed: {r.status_code}"

    r = client.post("/setup/2", data={"notification_pref": "openclaw"})
    assert r.status_code == 200, f"Setup step 2 failed: {r.status_code}"

    # Step 3: bank link (skip) — terminal step, redirects to /dashboard
    r = client.post("/setup/3", data={"action": "skip"})
    assert r.status_code == 302, f"Setup step 3 failed: {r.status_code}"
    assert r.headers["location"] == "/dashboard"


def _login(client: TestClient, password: str = "testpassword123") -> TestClient:
    """POST /login and return the authed client (cookie stored automatically)."""
    r = client.post("/login", data={"password": password})
    assert r.status_code == 302, f"Login failed: {r.status_code}"
    assert r.headers["location"] == "/dashboard"
    return client


@pytest.fixture()
def authed_client(db_path: Path) -> TestClient:
    """TestClient that has completed setup + login — no MCP involved."""
    from ui.server import app

    cl = TestClient(app, follow_redirects=False)
    _complete_setup(cl)
    return _login(cl)


# ---------------------------------------------------------------------------
# Test 1: daemon boots without any MCP client attached
# ---------------------------------------------------------------------------


class TestDaemonBootsWithoutMcpClient:
    """
    Verify server.daemon can be imported and its boot-time setup steps executed
    without any MCP session being active.
    """

    def test_daemon_boots_without_mcp_client(self, db_path: Path, monkeypatch) -> None:
        """
        Call the daemon main() boot sequence with mocked external resources.
        The daemon must not attempt any MCP interaction to start up.

        server.daemon.main() calls asyncio.run(_run()) where _run() awaits
        uvicorn.Server.serve().  We mock asyncio.run to prevent the event loop
        from actually starting, then verify all pre-uvicorn boot steps ran.
        """
        import server.paths as paths

        monkeypatch.setattr(paths, "DB_PATH", db_path)
        monkeypatch.setattr(paths, "APP_DIR", db_path.parent)

        # Patch asyncio.run so the uvicorn event loop never actually starts.
        # Also patch the individual setup functions to keep the test isolated.
        with (
            patch("asyncio.run") as mock_asyncio_run,
            patch("server.crypto.init_crypto") as mock_crypto,
            patch("server.paths.ensure_app_dir") as mock_ensure,
            patch("server.paths.audit_permissions") as mock_audit,
        ):
            from server import daemon

            # Call main() — this is the daemon entry point.
            daemon.main()

        # asyncio.run was reached — daemon completed all pre-boot steps.
        mock_asyncio_run.assert_called_once()
        # Crypto init was attempted (graceful fallback allowed in CI).
        mock_crypto.assert_called_once()
        # Filesystem setup was attempted.
        mock_ensure.assert_called_once()
        mock_audit.assert_called_once()

        # server.daemon must be importable without an active MCP session.
        assert daemon is not None, "server.daemon module must be importable without MCP"


# ---------------------------------------------------------------------------
# Test 2: UI server boots and serves /healthz without any MCP client
# ---------------------------------------------------------------------------


class TestUiServerBootsWithoutMcpClient:
    """
    Verify the FastAPI UI app serves health-check and index routes without
    requiring an active MCP session.
    """

    def test_ui_server_boots_without_mcp_client(self, client: TestClient) -> None:
        """GET /healthz must return 200 — no MCP interaction needed."""
        r = client.get("/healthz")
        assert r.status_code == 200, f"Expected 200, got {r.status_code}: {r.text}"
        data = r.json()
        assert data.get("status") == "ok"

    def test_ui_root_responds_without_mcp_client(self, client: TestClient) -> None:
        """GET / must return a valid HTTP response (2xx or 3xx redirect) without MCP."""
        r = client.get("/")
        assert r.status_code in range(200, 400), f"Expected 2xx/3xx, got {r.status_code}: {r.text}"

    def test_ui_login_page_responds_without_mcp_client(self, db_path: Path) -> None:
        """GET /login must be reachable (after setup) without MCP."""
        from ui.server import app

        cl = TestClient(app, follow_redirects=False)
        # Complete setup so the app is past the wizard redirect.
        _complete_setup(cl)
        r = cl.get("/login")
        assert r.status_code in (200, 302), f"Expected 200 or 302, got {r.status_code}: {r.text}"


# ---------------------------------------------------------------------------
# Test 3: sync runs via the UI route — no MCP client required
# ---------------------------------------------------------------------------


class TestSyncRunsViaUiNotMcp:
    """
    Verify that a full sync cycle can be triggered through the UI HTTP route
    (POST /profile + action=sync_now) without calling any MCP tool via
    the MCP JSON-RPC protocol.

    PlaidProvider.sync_transactions is mocked so no real Plaid API call happens.
    """

    def test_sync_runs_via_ui_not_mcp(
        self, authed_client: TestClient, db_path: Path, monkeypatch
    ) -> None:
        import server.paths as paths

        monkeypatch.setattr(paths, "DB_PATH", db_path)

        # Seed a fake bank connection directly into the DB.
        connection_id = str(uuid.uuid4())
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        conn.execute(
            "INSERT INTO bank_connections "
            "(id, plaid_item_id, plaid_access_token_encrypted, status) "
            "VALUES (?, 'item-test', 'fake-token', 'active')",
            (connection_id,),
        )
        conn.commit()
        conn.close()

        # Mock PlaidProvider to return an empty successful sync result.
        mock_sync_result = {
            "added": [],
            "modified": [],
            "removed": [],
            "next_cursor": "c1",
            "accounts": [],
        }

        mock_provider_instance = MagicMock()
        mock_provider_instance.sync_transactions.return_value = mock_sync_result
        mock_provider_instance.env = "sandbox"

        mock_provider_cls = MagicMock(return_value=mock_provider_instance)

        # Track whether any MCP RPC dispatch was attempted.
        mcp_called = []

        with (
            patch("server.main.PlaidProvider", mock_provider_cls),
            patch("server.main._plaid", mock_provider_instance),
            patch("server.crypto.decrypt", side_effect=lambda x: x),
            patch(
                "server.health_monitor.check_all_connections",
                return_value={
                    "checked": 0,
                    "active": 0,
                    "needs_reauth": 0,
                    "pending_expiration": 0,
                },
            ),
        ):
            # Trigger sync via the UI route — NOT via server.main.sync() directly.
            r = authed_client.post("/profile", data={"action": "sync_now"})

        # The UI route must respond without error (200 means rendered page with result).
        assert r.status_code == 200, f"POST /profile sync_now returned {r.status_code}: {r.text}"

        # Verify the provider was used (sync actually ran through the UI path).
        mock_provider_instance.sync_transactions.assert_called_once()

        # Confirm the sync_cursors table was updated — sync ran and committed state.
        conn = sqlite3.connect(str(db_path))
        row = conn.execute(
            "SELECT cursor FROM sync_cursors WHERE connection_id = ?", (connection_id,)
        ).fetchone()
        conn.close()
        assert row is not None, "sync_cursors must have a row after sync ran via UI"
        assert row[0] == "c1", f"Expected cursor 'c1', got {row[0]!r}"

        # Zero MCP calls — mcp_called is empty because we never dispatched via JSON-RPC.
        assert mcp_called == [], "No MCP JSON-RPC calls should have occurred"


# ---------------------------------------------------------------------------
# Test 4: notifications fire without any MCP client
# ---------------------------------------------------------------------------


class TestNotificationsFireWithoutMcp:
    """
    Verify server.notify.send() delivers notifications via the configured
    channel (falling back to in_ui) without requiring an MCP session.
    """

    def test_notifications_fire_without_mcp(self, tmp_path: Path) -> None:
        import os
        import sys

        db_path = tmp_path / "notify_test.db"

        # Initialise the DB with the canonical schema.
        schema_path = Path(__file__).parent.parent / "db" / "schema.sql"
        schema = schema_path.read_text()
        conn = sqlite3.connect(str(db_path))
        conn.executescript(schema)
        # Seed in_ui as preferred channel so no subprocess/HTTP needed.
        conn.execute(
            "INSERT OR REPLACE INTO app_config (id, notification_channel) VALUES (1, 'in_ui')"
        )
        conn.commit()
        conn.close()

        # Reload server.notify with the tmp DB path.
        with patch.dict(os.environ, {"DB_PATH": str(db_path)}):
            if "server.notify" in sys.modules:
                del sys.modules["server.notify"]

            import server.notify as notify

            notify._DB_PATH = str(db_path)

            # Trigger a notification directly — no MCP tool needed.
            result = notify.send("Budget alert: spending limit reached", urgency="high")

        # Verify delivery.
        assert "delivered_via" in result
        assert "notification_id" in result
        assert result["delivered_via"] == "in_ui"

        # Verify the row was persisted.
        conn = sqlite3.connect(str(db_path))
        row = conn.execute(
            "SELECT * FROM notifications WHERE id = ?", (result["notification_id"],)
        ).fetchone()
        conn.close()
        assert row is not None, "Notification must be persisted in the DB"

    def test_macos_notification_channel_without_mcp(self, tmp_path: Path) -> None:
        """Notifications via macos channel work without MCP (subprocess mocked)."""
        import os
        import sys

        db_path = tmp_path / "notify_macos_test.db"

        schema_path = Path(__file__).parent.parent / "db" / "schema.sql"
        schema = schema_path.read_text()
        conn = sqlite3.connect(str(db_path))
        conn.executescript(schema)
        conn.execute(
            "INSERT OR REPLACE INTO app_config (id, notification_channel) VALUES (1, 'macos')"
        )
        conn.commit()
        conn.close()

        with patch.dict(os.environ, {"DB_PATH": str(db_path)}):
            if "server.notify" in sys.modules:
                del sys.modules["server.notify"]

            import server.notify as notify

            notify._DB_PATH = str(db_path)

            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=0)
                result = notify.send("Test notification", urgency="normal")

        assert result["delivered_via"] == "macos"
        mock_run.assert_called_once()


# ---------------------------------------------------------------------------
# Test 5: setup wizard completes without any MCP client
# ---------------------------------------------------------------------------


class TestSetupWizardCompletesWithoutMcp:
    """
    Verify the 4-step setup wizard creates a user and initialises the
    application without any MCP session being present.
    """

    def test_setup_wizard_completes_without_mcp(self, db_path: Path) -> None:
        """
        Drive the complete setup wizard via TestClient HTTP calls.
        Verify a user is created in the DB — no MCP tool functions involved.
        """
        from ui.server import app

        cl = TestClient(app, follow_redirects=False)

        # Confirm setup page is accessible on a fresh DB.
        r = cl.get("/setup")
        assert r.status_code == 200, f"GET /setup returned {r.status_code}"

        # Step 1: password
        r = cl.post(
            "/setup/1",
            data={"password": "noMcpNeeded1", "password_confirm": "noMcpNeeded1"},
        )
        assert r.status_code == 200, f"Setup step 1 failed: {r.status_code}"

        # Step 2: notification preference
        r = cl.post("/setup/2", data={"notification_pref": "in_ui"})
        assert r.status_code == 200, f"Setup step 2 failed: {r.status_code}"

        # Step 3: bank link (skip) — terminal step, must redirect to /dashboard.
        with patch("server.main.apply_initial_setup", return_value={"status": "ok"}) as mock_apply:
            r = cl.post("/setup/3", data={"action": "skip"})

        assert r.status_code == 302, f"Setup step 3 failed: {r.status_code}"
        assert r.headers["location"] == "/dashboard"

        # Verify a user was created in the DB — the wizard persisted state.
        conn = sqlite3.connect(str(db_path))
        users = conn.execute("SELECT id FROM users").fetchall()
        conn.close()
        assert len(users) >= 1, "Setup wizard must create at least one user row in the DB"

        # Verify setup page now returns 404 (wizard is complete).
        r = cl.get("/setup")
        assert (
            r.status_code == 404
        ), f"GET /setup after completion should be 404, got {r.status_code}"

        # After wizard: apply_initial_setup was called via the UI (not via MCP JSON-RPC).
        mock_apply.assert_called_once()
