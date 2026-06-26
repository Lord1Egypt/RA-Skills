# FILE_META
# INPUT:  scope_id + PipelineOptions
# OUTPUT: HarnessBundle (zip bytes + scrub report) or ScopeInfo list
# POS:    skill lib adapters/hermes — harness packaging stage
# MISSION: Bundle ~/.hermes/ non-DB files into a scope='user' harness zip.

"""Hermes harness packaging.

Scope model (per docs/adapter-design.md §6.2): Hermes ships all user
state under a single ``~/.hermes/`` tree. That makes it a natural
``scope_type='user'`` adapter with a fixed ``scope_id='default'``.

What goes into the harness zip:
  - Every regular file under ``~/.hermes/``
    EXCEPT ``state.db`` + the WAL/SHM sidecars (SQLite internals, not
    user-authored config; also often larger than the 50MB bundle cap).
  - PII scrub is enabled for text-ish content (config / prompts / skills).
    Binary files are auto-detected and stored verbatim.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .. import ScopeInfo
from ._db import DEFAULT_STATE_DB

try:
    from lib.harness import HarnessBundle, HarnessFile, build_bundle
except ImportError:
    from ...harness import HarnessBundle, HarnessFile, build_bundle  # type: ignore

# Files we must not include (SQLite internals — large, binary, mutable).
EXCLUDE_NAMES = {"state.db", "state.db-wal", "state.db-shm"}


def _hermes_root(opts: Any = None) -> Path:
    """Resolve ~/.hermes/ (or env override).

    Shares the override semantics with _db.resolve_db_path so tests that
    point at a fake state.db can also exercise harness packaging.
    """
    env_db = os.environ.get("HERMES_STATE_DB")
    if env_db:
        return Path(env_db).expanduser().parent
    return Path(DEFAULT_STATE_DB).expanduser().parent


def list_scopes(opts: Any = None) -> list[ScopeInfo]:
    """There is at most one Hermes scope per machine: the user's ~/.hermes/."""
    root = _hermes_root(opts)
    if not root.is_dir():
        return []
    return [
        ScopeInfo(
            scope_type="user",
            scope_id="default",
            display_name=str(root),
        )
    ]


def build_harness(scope_id: str, opts: Any = None) -> HarnessBundle:
    """Pack ~/.hermes/ into a HarnessBundle.

    ``scope_id`` is validated against the fixed "default" value; any other
    value is a caller bug and raises ValueError.
    """
    if scope_id != "default":
        raise ValueError(
            f"hermes harness only supports scope_id='default', got {scope_id!r}"
        )

    root = _hermes_root(opts)
    if not root.is_dir():
        return build_bundle([])  # empty bundle; caller decides whether to upload

    manifest: list[HarnessFile] = []
    for dirpath, _dirs, filenames in os.walk(root):
        for fname in filenames:
            if fname in EXCLUDE_NAMES:
                continue
            full = Path(dirpath) / fname
            rel = full.relative_to(root).as_posix()
            manifest.append(HarnessFile(src=full, arc=rel, scrub=True))

    return build_bundle(manifest)


__all__ = ["list_scopes", "build_harness"]
