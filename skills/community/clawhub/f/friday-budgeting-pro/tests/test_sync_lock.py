"""
tests/test_sync_lock.py — Tests for server.sync_lock
"""

from __future__ import annotations

import fcntl
import os
import stat
from pathlib import Path

import pytest

import server.paths as paths
from server.sync_lock import (
    LockBusy,
    SyncLock,
    acquire_sync_lock,
    sync_lock,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@pytest.fixture()
def lock_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Redirect SYNC_LOCK_PATH to a temp file for isolation."""
    p = tmp_path / "sync.lock"
    monkeypatch.setattr(paths, "SYNC_LOCK_PATH", p)
    return p


# ---------------------------------------------------------------------------
# Basic acquire / release
# ---------------------------------------------------------------------------


def test_first_acquire_succeeds(lock_path: Path) -> None:
    lock = acquire_sync_lock()
    assert lock is not None
    lock.close()


def test_second_acquire_while_held_returns_none(lock_path: Path) -> None:
    lock1 = acquire_sync_lock()
    assert lock1 is not None
    try:
        lock2 = acquire_sync_lock()
        assert lock2 is None
    finally:
        lock1.close()


def test_acquire_after_release_succeeds(lock_path: Path) -> None:
    lock1 = acquire_sync_lock()
    assert lock1 is not None
    lock1.close()

    lock2 = acquire_sync_lock()
    assert lock2 is not None
    lock2.close()


# ---------------------------------------------------------------------------
# File permissions
# ---------------------------------------------------------------------------


def test_lock_file_mode_is_0600(lock_path: Path) -> None:
    lock = acquire_sync_lock()
    assert lock is not None
    try:
        mode = stat.S_IMODE(lock_path.stat().st_mode)
        assert mode == 0o600
    finally:
        lock.close()


# ---------------------------------------------------------------------------
# Context manager
# ---------------------------------------------------------------------------


def test_context_manager_releases_on_normal_exit(lock_path: Path) -> None:
    with sync_lock() as lk:
        assert isinstance(lk, SyncLock)

    # Should be releasable now
    lock2 = acquire_sync_lock()
    assert lock2 is not None
    lock2.close()


def test_context_manager_releases_on_exception(lock_path: Path) -> None:
    try:
        with sync_lock():
            raise RuntimeError("boom")
    except RuntimeError:
        pass

    lock2 = acquire_sync_lock()
    assert lock2 is not None
    lock2.close()


def test_sync_lock_raises_lock_busy_on_contention(lock_path: Path) -> None:
    lock1 = acquire_sync_lock()
    assert lock1 is not None
    try:
        with pytest.raises(LockBusy):
            with sync_lock():
                pass
    finally:
        lock1.close()


# ---------------------------------------------------------------------------
# Low-level contention: two raw fds on the same file
# ---------------------------------------------------------------------------


def test_raw_contention_raises_blocking_io_error(lock_path: Path) -> None:
    """Open the same file with two fds; second flock should raise BlockingIOError."""
    # Ensure file exists with correct mode
    paths.create_file(lock_path)

    fd1 = os.open(lock_path, os.O_RDONLY)
    fd2 = os.open(lock_path, os.O_RDONLY)
    try:
        fcntl.flock(fd1, fcntl.LOCK_EX | fcntl.LOCK_NB)
        with pytest.raises(BlockingIOError):
            fcntl.flock(fd2, fcntl.LOCK_EX | fcntl.LOCK_NB)
    finally:
        try:
            fcntl.flock(fd1, fcntl.LOCK_UN)
        except Exception:
            pass
        os.close(fd1)
        os.close(fd2)


# ---------------------------------------------------------------------------
# SyncLock.close() is idempotent
# ---------------------------------------------------------------------------


def test_close_is_idempotent(lock_path: Path) -> None:
    lock = acquire_sync_lock()
    assert lock is not None
    lock.close()
    lock.close()  # Should not raise
