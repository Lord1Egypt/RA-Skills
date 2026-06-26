"""
tests/test_notify.py — Unit tests for server/notify.py

All external side-effects (HTTP calls, osascript subprocess) are mocked so
the test suite runs without a live OpenClaw instance or macOS notification
permissions.
"""

import os
import sqlite3
import sys
import uuid
from pathlib import Path
from unittest.mock import MagicMock, patch
from urllib.error import URLError

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _init_db(db_path: str) -> None:
    """Run the canonical schema against a fresh SQLite file."""
    schema_path = Path(__file__).parent.parent / "db" / "schema.sql"
    schema = schema_path.read_text()
    conn = sqlite3.connect(db_path)
    conn.executescript(schema)
    conn.commit()
    conn.close()


def _seed_config(db_path: str, channel: str) -> None:
    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT OR REPLACE INTO app_config (id, notification_channel) VALUES (1, ?)",
        (channel,),
    )
    conn.commit()
    conn.close()


def _count_notifications(db_path: str) -> int:
    conn = sqlite3.connect(db_path)
    count = conn.execute("SELECT COUNT(*) FROM notifications").fetchone()[0]
    conn.close()
    return count


def _get_notification(db_path: str) -> dict:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM notifications LIMIT 1").fetchone()
    conn.close()
    return dict(row) if row else {}


# ---------------------------------------------------------------------------
# Fixture: isolated DB + patched module
# ---------------------------------------------------------------------------


@pytest.fixture
def notify_module(tmp_path):
    """
    Load (or reload) server.notify with DB_PATH pointed at a fresh tmp DB.
    Yields the module so tests can call notify.send() directly.
    """
    db_path = str(tmp_path / "friday.db")
    _init_db(db_path)

    # Patch the env var so notify._DB_PATH resolves to our tmp DB.
    with patch.dict(os.environ, {"DB_PATH": db_path}):
        # Force a clean reload so module-level _DB_PATH picks up the env var.
        if "server.notify" in sys.modules:
            del sys.modules["server.notify"]
        if "notify" in sys.modules:
            del sys.modules["notify"]

        # Add repo root to path so `import server.notify` works.
        repo_root = str(Path(__file__).parent.parent)
        if repo_root not in sys.path:
            sys.path.insert(0, repo_root)

        import server.notify as notify_mod

        # Re-bind _DB_PATH since it may have been set at import time before patch.
        notify_mod._DB_PATH = db_path
        yield notify_mod, db_path


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------


class TestOpenClawPreferred:
    """Preferred channel = openclaw_chat"""

    def test_openclaw_reachable(self, notify_module):
        mod, db_path = notify_module
        _seed_config(db_path, "openclaw_chat")

        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_resp) as mock_url:
            result = mod.send("Test message", urgency="normal")

        assert result["delivered_via"] == "openclaw_chat"
        assert "notification_id" in result
        assert _count_notifications(db_path) == 1
        row = _get_notification(db_path)
        assert row["delivered_via"] == "openclaw_chat"
        assert row["message"] == "Test message"
        assert row["urgency"] == "normal"
        assert row["read"] == 0

    def test_openclaw_fails_fallback_to_macos(self, notify_module):
        mod, db_path = notify_module
        _seed_config(db_path, "openclaw_chat")

        mock_proc = MagicMock()
        mock_proc.returncode = 0

        with patch("urllib.request.urlopen", side_effect=URLError("refused")):
            with patch("subprocess.run", return_value=mock_proc):
                result = mod.send("Test fallback", urgency="high")

        assert result["delivered_via"] == "macos"
        assert _count_notifications(db_path) == 1
        assert _get_notification(db_path)["delivered_via"] == "macos"

    def test_openclaw_and_macos_fail_fallback_to_in_ui(self, notify_module):
        mod, db_path = notify_module
        _seed_config(db_path, "openclaw_chat")

        mock_proc = MagicMock()
        mock_proc.returncode = 1  # osascript returns non-zero

        with patch("urllib.request.urlopen", side_effect=URLError("refused")):
            with patch("subprocess.run", return_value=mock_proc):
                result = mod.send("All channels fail")

        assert result["delivered_via"] == "in_ui"
        assert _count_notifications(db_path) == 1
        assert _get_notification(db_path)["delivered_via"] == "in_ui"


class TestMacOSPreferred:
    """Preferred channel = macos"""

    def test_macos_reachable(self, notify_module):
        mod, db_path = notify_module
        _seed_config(db_path, "macos")

        mock_proc = MagicMock()
        mock_proc.returncode = 0

        with patch("subprocess.run", return_value=mock_proc):
            result = mod.send("macOS test")

        assert result["delivered_via"] == "macos"
        assert _count_notifications(db_path) == 1

    def test_macos_fails_fallback_to_in_ui(self, notify_module):
        mod, db_path = notify_module
        _seed_config(db_path, "macos")

        mock_proc = MagicMock()
        mock_proc.returncode = 1

        with patch("subprocess.run", return_value=mock_proc):
            result = mod.send("macOS failure")

        assert result["delivered_via"] == "in_ui"
        assert _count_notifications(db_path) == 1
        assert _get_notification(db_path)["delivered_via"] == "in_ui"


class TestInUIPreferred:
    """Preferred channel = in_ui"""

    def test_in_ui_never_tries_other_channels(self, notify_module):
        mod, db_path = notify_module
        _seed_config(db_path, "in_ui")

        with patch("urllib.request.urlopen") as mock_url, patch("subprocess.run") as mock_proc:
            result = mod.send("UI only")

            mock_url.assert_not_called()
            mock_proc.assert_not_called()

        assert result["delivered_via"] == "in_ui"
        assert _count_notifications(db_path) == 1
        assert _get_notification(db_path)["delivered_via"] == "in_ui"


class TestRowPersistence:
    """All delivery paths must write a notifications row."""

    @pytest.mark.parametrize(
        "channel,url_side_effect,proc_returncode,expected_via",
        [
            # openclaw_chat success
            ("openclaw_chat", None, 0, "openclaw_chat"),
            # openclaw_chat fails → macos success
            ("openclaw_chat", URLError("x"), 0, "macos"),
            # openclaw_chat fails → macos fails → in_ui
            ("openclaw_chat", URLError("x"), 1, "in_ui"),
            # macos success
            ("macos", None, 0, "macos"),
            # macos fails → in_ui
            ("macos", None, 1, "in_ui"),
            # in_ui direct
            ("in_ui", None, 0, "in_ui"),
        ],
    )
    def test_row_always_inserted(
        self,
        notify_module,
        channel,
        url_side_effect,
        proc_returncode,
        expected_via,
    ):
        mod, db_path = notify_module
        _seed_config(db_path, channel)

        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)

        mock_proc = MagicMock()
        mock_proc.returncode = proc_returncode

        url_effect = url_side_effect if url_side_effect else mock_resp

        with patch(
            "urllib.request.urlopen",
            side_effect=url_side_effect if url_side_effect else None,
            return_value=mock_resp if not url_side_effect else None,
        ):
            with patch("subprocess.run", return_value=mock_proc):
                result = mod.send("Persistence check", urgency="normal")

        assert (
            _count_notifications(db_path) == 1
        ), f"Expected 1 notification row for channel={channel}, got 0"
        row = _get_notification(db_path)
        assert row["delivered_via"] == expected_via
        assert uuid.UUID(result["notification_id"])  # valid UUID4
