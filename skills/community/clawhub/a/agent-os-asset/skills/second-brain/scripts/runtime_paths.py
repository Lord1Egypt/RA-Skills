#!/usr/bin/env python3
"""Resolve portable Second Brain data and runtime paths."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Mapping
from urllib.parse import urlparse


@dataclass(frozen=True)
class RuntimePaths:
    """Resolved user data and runtime state locations."""

    vault: Path
    report_vault: Path
    state_dir: Path
    index_dir: Path
    report_index: Path
    asset_registry: Path
    log_path: Path
    lock_path: Path


def _configured_path(
    values: Mapping[str, str],
    name: str,
    fallback: Path,
) -> Path:
    raw = values.get(name, "").strip()
    return Path(raw).expanduser() if raw else fallback


def resolve_paths(
    *,
    environ: Mapping[str, str] | None = None,
    home: Path | None = None,
) -> RuntimePaths:
    """Resolve paths without depending on the installed Skill location."""

    values = os.environ if environ is None else environ
    user_home = (home or Path.home()).expanduser()
    xdg_state = values.get("XDG_STATE_HOME", "").strip()
    portable_state = Path(xdg_state).expanduser() if xdg_state else user_home / ".local" / "state"
    state_dir = _configured_path(
        values,
        "SECOND_BRAIN_STATE_DIR",
        portable_state / "second-brain",
    )
    index_dir = _configured_path(values, "SECOND_BRAIN_INDEX_DIR", state_dir / "index")
    return RuntimePaths(
        vault=_configured_path(
            values,
            "SECOND_BRAIN_VAULT",
            user_home / "Documents" / "SecondBrain",
        ),
        report_vault=_configured_path(
            values,
            "SECOND_BRAIN_REPORT_VAULT",
            user_home / "Documents" / "SecondBrainReports",
        ),
        state_dir=state_dir,
        index_dir=index_dir,
        report_index=_configured_path(
            values,
            "SECOND_BRAIN_REPORT_INDEX",
            state_dir / "report-index" / "documents.jsonl",
        ),
        asset_registry=_configured_path(
            values,
            "SECOND_BRAIN_ASSET_REGISTRY",
            state_dir / "asset-index-registry.json",
        ),
        log_path=_configured_path(
            values,
            "SECOND_BRAIN_LOG",
            state_dir / "logs" / "routine-update.log",
        ),
        lock_path=_configured_path(
            values,
            "SECOND_BRAIN_LOCK",
            state_dir / "locks" / "routine-update.lock",
        ),
    )


def is_https_url(value: str) -> bool:
    """Return whether value is an absolute HTTPS URL."""

    parsed = urlparse(value.strip())
    return parsed.scheme.lower() == "https" and bool(parsed.netloc)


DEFAULT_PATHS = resolve_paths()
