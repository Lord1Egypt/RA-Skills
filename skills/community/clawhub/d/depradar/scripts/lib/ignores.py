"""Acknowledgement/ignore system for /depradar.

Loads .depradar-ignore files (project-root and global) to suppress known,
evaluated breaking changes from the report output.

File format:
    # .depradar-ignore
    # Format: package[@version]  # optional reason comment
    chalk@5           # ESM-only, evaluated 2026-03-27 — only used in CLI output
    dotenv@17         # uses config() only, unchanged API
    stripe            # all versions suppressed (rare, use with care)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional, Set


_GLOBAL_IGNORE_FILE = Path.home() / ".config" / "depradar" / "ignore"
_PROJECT_IGNORE_FILE = ".depradar-ignore"


def load_ignores(project_root: str = "") -> Set[str]:
    """Load ignore entries from project and global ignore files.

    Returns a set of lowercase ignore keys like {'chalk@5', 'dotenv@17', 'stripe'}.
    """
    ignores: Set[str] = set()

    # Global file
    if _GLOBAL_IGNORE_FILE.exists():
        _parse_ignore_file(_GLOBAL_IGNORE_FILE, ignores)

    # Project file
    if project_root:
        project_file = Path(project_root) / _PROJECT_IGNORE_FILE
        if project_file.exists():
            _parse_ignore_file(project_file, ignores)

    return ignores


def is_ignored(package: str, version: str, ignores: Set[str]) -> bool:
    """Return True if package@version matches any ignore entry.

    Matching rules (checked in order):
    1. Exact: 'chalk@5.3.0' matches entry 'chalk@5.3.0'
    2. Major wildcard: 'chalk@5.3.0' matches entry 'chalk@5'
    3. Package wildcard: 'chalk@5.3.0' matches entry 'chalk'
    """
    if not ignores:
        return False
    pkg_lower = package.lower()
    ver_lower = version.lower()

    # 1. Exact match: chalk@5.3.0
    if f"{pkg_lower}@{ver_lower}" in ignores:
        return True

    # 2. Major version wildcard: chalk@5
    major = ver_lower.split(".")[0] if ver_lower else ""
    if major and f"{pkg_lower}@{major}" in ignores:
        return True

    # 3. Package-only wildcard: chalk
    if pkg_lower in ignores:
        return True

    return False


def _parse_ignore_file(path: Path, ignores: Set[str]) -> None:
    """Parse an ignore file and add entries to the ignores set."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return
    for line in text.splitlines():
        # Strip inline comment
        line = line.split("#")[0].strip()
        if not line:
            continue
        # Normalize: lowercase, strip version prefix 'v'
        entry = line.lower()
        # If 'pkg@vX.Y.Z', strip the 'v': 'pkg@X.Y.Z'
        entry = re.sub(r"@v(\d)", r"@\1", entry)
        ignores.add(entry)
