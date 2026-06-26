"""Runtime path resolution for Founder Signal."""

from __future__ import annotations

import os
from pathlib import Path

_RUNTIME_DIRS = (
    "profiles",
    "runs",
    "logs",
    "state",
    "config-imports",
)


def default_data_dir() -> Path:
    configured = os.environ.get("FOUNDER_SIGNAL_HOME")
    if configured:
        return Path(configured).expanduser().resolve()
    return Path("~/.founder-signal").expanduser().resolve()


def resolve_root_dir(value: str | None) -> Path:
    if value:
        return Path(value).expanduser().resolve()
    return default_data_dir()


def ensure_runtime_dirs(root_dir: Path) -> None:
    for dirname in _RUNTIME_DIRS:
        (root_dir / dirname).mkdir(parents=True, exist_ok=True)
