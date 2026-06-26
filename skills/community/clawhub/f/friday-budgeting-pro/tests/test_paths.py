"""
tests/test_paths.py — Unit tests for server/paths.py

All tests use pytest's tmp_path fixture + monkeypatch to redirect APP_DIR
so they never touch the real ~/.friday-bp/ directory.
"""

from __future__ import annotations

import logging
import os
import stat
from pathlib import Path

import server.paths as paths

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mode(p: Path) -> int:
    """Return the permission bits (lower 12) of *p*."""
    return stat.S_IMODE(p.stat().st_mode)


def _redirect_app_dir(monkeypatch, tmp_path: Path) -> Path:
    """Point server.paths.APP_DIR (and derived constants) at *tmp_path*."""
    fake_app_dir = tmp_path / ".friday-bp"
    monkeypatch.setattr(paths, "APP_DIR", fake_app_dir)
    monkeypatch.setattr(paths, "DB_PATH", fake_app_dir / "data.db")
    monkeypatch.setattr(paths, "SYNC_LOCK_PATH", fake_app_dir / "sync.lock")
    monkeypatch.setattr(paths, "EXPORTS_DIR", fake_app_dir / "exports")
    return fake_app_dir


# ---------------------------------------------------------------------------
# ensure_app_dir
# ---------------------------------------------------------------------------


def test_ensure_app_dir_creates_with_0700(monkeypatch, tmp_path):
    fake_app_dir = _redirect_app_dir(monkeypatch, tmp_path)

    paths.ensure_app_dir()

    assert fake_app_dir.is_dir(), "APP_DIR should be created"
    assert _mode(fake_app_dir) == 0o700, "APP_DIR should have mode 0700"

    exports = fake_app_dir / "exports"
    assert exports.is_dir(), "exports/ should be created"
    assert _mode(exports) == 0o700, "exports/ should have mode 0700"


def test_ensure_app_dir_fixes_wrong_mode(monkeypatch, tmp_path, caplog):
    fake_app_dir = _redirect_app_dir(monkeypatch, tmp_path)

    # Pre-create the directory, then force the wrong mode with chmod
    # (mkdir respects umask, so chmod is required to set an exact mode).
    fake_app_dir.mkdir(parents=True)
    os.chmod(fake_app_dir, 0o755)
    assert _mode(fake_app_dir) == 0o755

    with caplog.at_level(logging.WARNING, logger="server.paths"):
        paths.ensure_app_dir()

    assert _mode(fake_app_dir) == 0o700, "APP_DIR mode should be corrected to 0700"
    assert any(
        "fixing" in record.message for record in caplog.records
    ), "A warning should be logged when the mode is corrected"


def test_ensure_app_dir_idempotent(monkeypatch, tmp_path):
    _redirect_app_dir(monkeypatch, tmp_path)
    paths.ensure_app_dir()
    # Second call must not raise.
    paths.ensure_app_dir()


# ---------------------------------------------------------------------------
# create_file
# ---------------------------------------------------------------------------


def test_create_file_creates_with_0600(monkeypatch, tmp_path):
    fake_app_dir = _redirect_app_dir(monkeypatch, tmp_path)
    fake_app_dir.mkdir(mode=0o700, parents=True)

    target = fake_app_dir / "data.db"
    paths.create_file(target)

    assert target.exists(), "File should be created"
    assert _mode(target) == 0o600, "File should have mode 0600"


def test_create_file_fixes_wrong_mode(monkeypatch, tmp_path, caplog):
    fake_app_dir = _redirect_app_dir(monkeypatch, tmp_path)
    fake_app_dir.mkdir(mode=0o700, parents=True)

    target = fake_app_dir / "data.db"
    # Pre-create with wrong mode.
    target.touch()
    os.chmod(target, 0o644)
    assert _mode(target) == 0o644

    with caplog.at_level(logging.WARNING, logger="server.paths"):
        paths.create_file(target)

    assert _mode(target) == 0o600, "File mode should be corrected to 0600"
    assert any(
        "fixing" in record.message for record in caplog.records
    ), "A warning should be logged when the mode is corrected"


def test_create_file_does_not_overwrite_contents(monkeypatch, tmp_path):
    fake_app_dir = _redirect_app_dir(monkeypatch, tmp_path)
    fake_app_dir.mkdir(mode=0o700, parents=True)

    target = fake_app_dir / "data.db"
    target.write_text("existing content")
    os.chmod(target, 0o600)

    paths.create_file(target)

    assert (
        target.read_text() == "existing content"
    ), "create_file should not overwrite existing file contents"


# ---------------------------------------------------------------------------
# audit_permissions
# ---------------------------------------------------------------------------


def test_audit_permissions_fixes_file(monkeypatch, tmp_path, caplog):
    fake_app_dir = _redirect_app_dir(monkeypatch, tmp_path)
    fake_app_dir.mkdir(mode=0o700, parents=True)

    # Create a file with wrong permissions.
    bad_file = fake_app_dir / "data.db"
    bad_file.touch()
    os.chmod(bad_file, 0o644)
    assert _mode(bad_file) == 0o644

    with caplog.at_level(logging.WARNING, logger="server.paths"):
        paths.audit_permissions()

    assert _mode(bad_file) == 0o600, "audit_permissions should fix 0644 → 0600"
    assert any(
        "fixing" in record.message for record in caplog.records
    ), "A warning should be logged for the corrected file"


def test_audit_permissions_fixes_dir(monkeypatch, tmp_path, caplog):
    fake_app_dir = _redirect_app_dir(monkeypatch, tmp_path)

    # Pre-create the directory, then force the wrong mode with chmod
    # (mkdir respects umask, so chmod is required to set an exact mode).
    fake_app_dir.mkdir(parents=True)
    os.chmod(fake_app_dir, 0o755)
    assert _mode(fake_app_dir) == 0o755

    with caplog.at_level(logging.WARNING, logger="server.paths"):
        paths.audit_permissions()

    assert _mode(fake_app_dir) == 0o700, "audit_permissions should fix 0755 → 0700"
    assert any(
        "fixing" in record.message for record in caplog.records
    ), "A warning should be logged for the corrected directory"


def test_audit_permissions_no_op_when_correct(monkeypatch, tmp_path, caplog):
    fake_app_dir = _redirect_app_dir(monkeypatch, tmp_path)
    fake_app_dir.mkdir(mode=0o700, parents=True)

    good_file = fake_app_dir / "data.db"
    good_file.touch()
    os.chmod(good_file, 0o600)

    with caplog.at_level(logging.WARNING, logger="server.paths"):
        paths.audit_permissions()

    assert not caplog.records, "No warnings should be emitted when permissions are correct"


def test_audit_permissions_noop_when_dir_absent(monkeypatch, tmp_path):
    fake_app_dir = _redirect_app_dir(monkeypatch, tmp_path)
    assert not fake_app_dir.exists()

    # Should not raise.
    paths.audit_permissions()
