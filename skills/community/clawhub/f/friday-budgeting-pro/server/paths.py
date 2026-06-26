"""
server/paths.py — Centralised path constants and permission helpers.

All on-disk artefacts for Friday Budgeting Pro live under ~/.friday-bp/.
This module owns:
  - Directory / file path constants
  - Atomic file creation with the correct mode (0600)
  - Directory creation with the correct mode (0700)
  - A startup audit that fixes any files whose permissions have drifted
"""

from __future__ import annotations

import logging
import os
import stat
from pathlib import Path

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Path constants
# ---------------------------------------------------------------------------

# FRIDAY_BP_APP_DIR env var lets tests (and CI) redirect all on-disk artefacts
# to a temporary directory without touching ~/.friday-bp/.
APP_DIR: Path = (
    Path(os.environ["FRIDAY_BP_APP_DIR"])
    if "FRIDAY_BP_APP_DIR" in os.environ
    else Path.home() / ".friday-bp"
)
DB_PATH: Path = APP_DIR / "data.db"
SYNC_LOCK_PATH: Path = APP_DIR / "sync.lock"
EXPORTS_DIR: Path = APP_DIR / "exports"

# ---------------------------------------------------------------------------
# Directory helpers
# ---------------------------------------------------------------------------

_DIR_MODE = 0o700
_FILE_MODE = 0o600


def ensure_app_dir() -> None:
    """Create ~/.friday-bp/ (and exports/) with mode 0700.

    Idempotent.  If the directory already exists but has the wrong permissions,
    the permissions are corrected and a warning is logged.
    """
    for directory in (APP_DIR, EXPORTS_DIR):
        if directory.exists():
            current = stat.S_IMODE(directory.stat().st_mode)
            if current != _DIR_MODE:
                logger.warning(
                    "Directory %s has permissions %o — expected %o; fixing.",
                    directory,
                    current,
                    _DIR_MODE,
                )
                os.chmod(directory, _DIR_MODE)
        else:
            directory.mkdir(mode=_DIR_MODE, parents=True)


# ---------------------------------------------------------------------------
# File helpers
# ---------------------------------------------------------------------------


def create_file(path: Path, mode: int = _FILE_MODE) -> None:
    """Create *path* with *mode*, atomically, if it does not already exist.

    If the file already exists:
      - its mode is audited; if wrong it is corrected and a warning is logged.
      - its contents are left untouched.

    The implementation uses O_CREAT | O_EXCL via os.open so that the mode is
    applied at creation time (avoids a race between open() and chmod()).
    """
    path = Path(path)
    if path.exists():
        current = stat.S_IMODE(path.stat().st_mode)
        if current != mode:
            logger.warning(
                "File %s has permissions %o — expected %o; fixing.",
                path,
                current,
                mode,
            )
            os.chmod(path, mode)
        return

    # Ensure parent directory exists before creating the file.
    path.parent.mkdir(mode=_DIR_MODE, parents=True, exist_ok=True)

    # Create atomically with the correct mode from the start.
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, mode)
    os.close(fd)


# ---------------------------------------------------------------------------
# Startup audit
# ---------------------------------------------------------------------------


def audit_permissions() -> None:
    """Scan APP_DIR and fix any files/dirs whose permissions have drifted.

    Called once at daemon startup.  Logs a warning for every artefact that
    needed to be corrected.
    """
    if not APP_DIR.exists():
        return

    # Audit the top-level app directory itself.
    _audit_dir(APP_DIR)

    for item in APP_DIR.rglob("*"):
        if item.is_dir():
            _audit_dir(item)
        elif item.is_file():
            _audit_file(item)


def _audit_dir(path: Path) -> None:
    current = stat.S_IMODE(path.stat().st_mode)
    if current != _DIR_MODE:
        logger.warning(
            "audit_permissions: directory %s has permissions %o — expected %o; fixing.",
            path,
            current,
            _DIR_MODE,
        )
        os.chmod(path, _DIR_MODE)


def _audit_file(path: Path) -> None:
    current = stat.S_IMODE(path.stat().st_mode)
    if current != _FILE_MODE:
        logger.warning(
            "audit_permissions: file %s has permissions %o — expected %o; fixing.",
            path,
            current,
            _FILE_MODE,
        )
        os.chmod(path, _FILE_MODE)
