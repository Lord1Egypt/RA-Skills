"""
tests/test_openclaw_cron.py — Focused unit tests for the OpenClaw cron
registration helper in server.main.

These tests operate at the helper level (_register_openclaw_cron / the
_OPENCLAW_HOME module override) and do NOT touch the database, so no tmp_db
fixture is needed.
"""

from __future__ import annotations

import json
from pathlib import Path

import server.main as _main
from server.main import _register_openclaw_cron

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _set_openclaw_home(monkeypatch, path: Path | None) -> None:
    """Redirect server.main._OPENCLAW_HOME to *path* for the duration of the test."""
    monkeypatch.setattr(_main, "_OPENCLAW_HOME", path)


# ---------------------------------------------------------------------------
# Happy-path: ~/.openclaw/ exists
# ---------------------------------------------------------------------------


def test_cron_file_created_when_openclaw_exists(monkeypatch, tmp_path):
    """_register_openclaw_cron() returns True and writes the cron JSON file."""
    oc_dir = tmp_path / ".openclaw"
    oc_dir.mkdir()
    _set_openclaw_home(monkeypatch, oc_dir)

    result = _register_openclaw_cron()

    assert result is True
    cron_file = oc_dir / "cron" / "friday-budgeting-pro-sync.json"
    assert cron_file.exists(), f"Cron file should exist at {cron_file}"


def test_cron_file_has_correct_schedule(monkeypatch, tmp_path):
    """The written cron file must contain the expected schedule expression."""
    oc_dir = tmp_path / ".openclaw"
    oc_dir.mkdir()
    _set_openclaw_home(monkeypatch, oc_dir)

    _register_openclaw_cron()

    cron_file = oc_dir / "cron" / "friday-budgeting-pro-sync.json"
    spec = json.loads(cron_file.read_text())

    assert spec["schedule"]["kind"] == "cron"
    assert spec["schedule"]["expr"] == "0 6 * * *"


def test_cron_file_has_tz(monkeypatch, tmp_path):
    """The cron spec must include a non-empty 'tz' field."""
    oc_dir = tmp_path / ".openclaw"
    oc_dir.mkdir()
    _set_openclaw_home(monkeypatch, oc_dir)

    _register_openclaw_cron()

    cron_file = oc_dir / "cron" / "friday-budgeting-pro-sync.json"
    spec = json.loads(cron_file.read_text())

    assert "tz" in spec["schedule"]
    assert spec["schedule"]["tz"]  # non-empty string


def test_cron_file_has_correct_name_and_payload(monkeypatch, tmp_path):
    """The cron spec must have the canonical name and agentTurn payload."""
    oc_dir = tmp_path / ".openclaw"
    oc_dir.mkdir()
    _set_openclaw_home(monkeypatch, oc_dir)

    _register_openclaw_cron()

    cron_file = oc_dir / "cron" / "friday-budgeting-pro-sync.json"
    spec = json.loads(cron_file.read_text())

    assert spec["name"] == "friday-budgeting-pro-sync"
    assert spec["sessionTarget"] == "isolated"
    assert spec["payload"]["kind"] == "agentTurn"
    assert "sync" in spec["payload"]["message"].lower()
    assert spec["payload"]["timeoutSeconds"] == 900
    assert spec["delivery"]["mode"] == "none"


# ---------------------------------------------------------------------------
# Absent ~/.openclaw/ — no error, returns False
# ---------------------------------------------------------------------------


def test_returns_false_when_openclaw_absent(monkeypatch, tmp_path):
    """_register_openclaw_cron() must return False (not raise) when ~/.openclaw/ is missing."""
    absent_dir = tmp_path / "not-here"
    # Deliberately do NOT create absent_dir
    _set_openclaw_home(monkeypatch, absent_dir)

    result = _register_openclaw_cron()

    assert result is False


def test_no_file_written_when_openclaw_absent(monkeypatch, tmp_path):
    """No cron file should be written when ~/.openclaw/ does not exist."""
    absent_dir = tmp_path / "not-here"
    _set_openclaw_home(monkeypatch, absent_dir)

    _register_openclaw_cron()

    # The directory itself should not have been created
    assert not absent_dir.exists()


def test_warning_logged_when_openclaw_absent(monkeypatch, tmp_path, caplog):
    """A WARNING must be logged when ~/.openclaw/ is absent."""
    import logging

    absent_dir = tmp_path / "not-here"
    _set_openclaw_home(monkeypatch, absent_dir)

    with caplog.at_level(logging.WARNING, logger="server.main"):
        _register_openclaw_cron()

    assert any(
        "cron" in msg.lower() or "openclaw" in msg.lower() for msg in caplog.messages
    ), "Expected a warning mentioning cron or openclaw"


# ---------------------------------------------------------------------------
# Idempotency — running twice overwrites cleanly
# ---------------------------------------------------------------------------


def test_overwrite_on_second_call(monkeypatch, tmp_path):
    """Calling _register_openclaw_cron() twice produces exactly one cron file."""
    oc_dir = tmp_path / ".openclaw"
    oc_dir.mkdir()
    _set_openclaw_home(monkeypatch, oc_dir)

    r1 = _register_openclaw_cron()
    r2 = _register_openclaw_cron()

    assert r1 is True
    assert r2 is True

    cron_dir = oc_dir / "cron"
    files = list(cron_dir.iterdir())
    assert len(files) == 1, f"Expected 1 file, got {[f.name for f in files]}"


def test_second_call_produces_valid_json(monkeypatch, tmp_path):
    """The cron file written on the second call must still be valid JSON."""
    oc_dir = tmp_path / ".openclaw"
    oc_dir.mkdir()
    _set_openclaw_home(monkeypatch, oc_dir)

    _register_openclaw_cron()
    _register_openclaw_cron()

    cron_file = oc_dir / "cron" / "friday-budgeting-pro-sync.json"
    spec = json.loads(cron_file.read_text())  # raises if invalid
    assert spec["name"] == "friday-budgeting-pro-sync"


# ---------------------------------------------------------------------------
# cron/ sub-directory is created if absent
# ---------------------------------------------------------------------------


def test_cron_dir_auto_created(monkeypatch, tmp_path):
    """The cron/ subdirectory must be created if it doesn't already exist."""
    oc_dir = tmp_path / ".openclaw"
    oc_dir.mkdir()
    # Do NOT pre-create cron/
    _set_openclaw_home(monkeypatch, oc_dir)

    _register_openclaw_cron()

    assert (oc_dir / "cron").is_dir()
