#!/usr/bin/env python3
"""
Shared path resolution for AiriLab runtime data.
"""

import os
from pathlib import Path


def get_airilab_home() -> Path:
    """
    Resolve runtime home directory.

    Priority:
    1) AIRILAB_HOME env var
    2) ~/.openclaw/skills/airilab
    """
    override = os.getenv("AIRILAB_HOME", "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return (Path.home() / ".openclaw" / "skills" / "airilab").resolve()


def get_config_dir() -> Path:
    return get_airilab_home() / "config"


def get_scheduler_dir() -> Path:
    return get_airilab_home() / "scheduler"


def ensure_runtime_dirs() -> None:
    get_config_dir().mkdir(parents=True, exist_ok=True)
    get_scheduler_dir().mkdir(parents=True, exist_ok=True)

