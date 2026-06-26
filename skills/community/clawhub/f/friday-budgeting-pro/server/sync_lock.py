"""
server/sync_lock.py — Single-flight sync lock primitive.

Uses a POSIX advisory exclusive lock (fcntl.flock) on SYNC_LOCK_PATH so that
only one sync operation can run at a time.  The lock file is never deleted —
deletion causes races with concurrent openers; the flock is the gate.

Unix only (fcntl).  No Windows fallback.

Public API
----------
acquire_sync_lock(timeout: float = 0.0) -> SyncLock | None
    Non-blocking acquire.  Returns a SyncLock on success, None on contention.
    When timeout > 0 the call retries with short sleeps until the lock is
    acquired or the timeout elapses.

sync_lock(timeout: float = 0.0) — @contextmanager
    Yields a SyncLock or raises LockBusy on contention.

class SyncLock
    Context manager.  Holds the open file descriptor and releases the flock
    on __exit__ / close().  Does NOT delete the lock file.

class LockBusy(Exception)
    Raised by sync_lock() when the lock cannot be acquired.
"""

from __future__ import annotations

import fcntl
import os
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

import server.paths as _paths

__all__ = [
    "SyncLock",
    "LockBusy",
    "acquire_sync_lock",
    "sync_lock",
]

_RETRY_INTERVAL = 0.05  # seconds between retries when timeout > 0


class LockBusy(Exception):
    """Raised when the sync lock cannot be acquired due to contention."""


class SyncLock:
    """Holds an exclusive flock on the sync lock file.

    Acquire via :func:`acquire_sync_lock` or the :func:`sync_lock` context
    manager rather than constructing directly.
    """

    def __init__(self, fd: int) -> None:
        self._fd: int | None = fd

    # ------------------------------------------------------------------
    # Context-manager protocol
    # ------------------------------------------------------------------

    def __enter__(self) -> "SyncLock":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Explicit release
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Release the flock and close the file descriptor.

        Idempotent — safe to call more than once.
        """
        if self._fd is not None:
            try:
                fcntl.flock(self._fd, fcntl.LOCK_UN)
            finally:
                os.close(self._fd)
                self._fd = None


def _open_lock_file() -> int:
    """Return an open file descriptor for SYNC_LOCK_PATH (mode 0600).

    Creates the file via server.paths.create_file if it does not exist,
    then opens it read-only for locking (we only need the fd, not the data).
    """
    lock_path: Path = _paths.SYNC_LOCK_PATH
    _paths.create_file(lock_path)
    return os.open(lock_path, os.O_RDONLY)


def acquire_sync_lock(timeout: float = 0.0) -> SyncLock | None:
    """Try to acquire the exclusive sync lock.

    Parameters
    ----------
    timeout:
        * ``0.0`` (default) — single non-blocking attempt.
        * ``> 0`` — keep retrying until *timeout* seconds have elapsed.

    Returns
    -------
    SyncLock
        On success.
    None
        On contention (lock is held by another process/descriptor).
    """
    deadline: float | None = (time.monotonic() + timeout) if timeout > 0 else None

    while True:
        fd = _open_lock_file()
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return SyncLock(fd)
        except BlockingIOError:
            os.close(fd)
            if deadline is None or time.monotonic() >= deadline:
                return None
            time.sleep(_RETRY_INTERVAL)


@contextmanager
def sync_lock(timeout: float = 0.0) -> Generator[SyncLock, None, None]:
    """Context manager that yields a :class:`SyncLock` or raises :class:`LockBusy`.

    Parameters
    ----------
    timeout:
        Passed through to :func:`acquire_sync_lock`.

    Raises
    ------
    LockBusy
        When the lock cannot be acquired within *timeout* seconds.
    """
    lock = acquire_sync_lock(timeout=timeout)
    if lock is None:
        raise LockBusy("sync lock is held by another process")
    try:
        yield lock
    finally:
        lock.close()
