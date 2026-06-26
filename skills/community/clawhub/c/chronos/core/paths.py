"""Runtime path and command helpers for Chronos."""
from __future__ import annotations

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

_DEFAULT_WORKSPACE = Path.home() / ".openclaw" / "workspace"


def _explicit_workspace_candidates() -> list[Path]:
    candidates: list[Path] = []
    for env_name in ("CHRONOS_WORKSPACE", "OPENCLAW_WORKSPACE"):
        raw_value = os.getenv(env_name)
        if raw_value:
            candidates.append(Path(raw_value).expanduser())
    return candidates


def _workspace_candidates() -> list[Path]:
    candidates = _explicit_workspace_candidates()
    candidates.extend([_DEFAULT_WORKSPACE, PROJECT_ROOT])
    return candidates


def resolve_workspace() -> Path:
    """Return the best workspace root for the current runtime."""
    explicit_candidates = _explicit_workspace_candidates()
    if explicit_candidates:
        for candidate in explicit_candidates:
            if candidate.exists():
                return candidate
        return explicit_candidates[0]

    for candidate in _workspace_candidates():
        if (candidate / "todo.db").exists():
            return candidate

    for candidate in _workspace_candidates():
        if candidate.exists():
            return candidate

    return PROJECT_ROOT


WORKSPACE = resolve_workspace()
TODO_DB = Path(os.getenv("CHRONOS_DB_PATH", str(WORKSPACE / "todo.db"))).expanduser()
PYTHON_BIN = os.getenv("CHRONOS_PYTHON_BIN") or sys.executable or "python"
OPENCLAW_BIN = os.getenv("OPENCLAW_BIN", "openclaw")


def get_prediction_logger_path() -> Path | None:
    """Return the prediction logger script path when available."""
    configured = os.getenv("CHRONOS_PREDICTION_LOGGER")
    if configured:
        path = Path(configured).expanduser()
        return path if path.exists() else None

    default_path = WORKSPACE / "scripts" / "prediction_logger.py"
    return default_path if default_path.exists() else None
