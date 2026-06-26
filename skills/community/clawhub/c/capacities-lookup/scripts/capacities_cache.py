from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


def _detect_workspace_root() -> Path:
    env_root = os.environ.get("CAPACITIES_WORKSPACE_ROOT", "").strip()
    if env_root:
        return Path(env_root).expanduser().resolve()

    candidates: list[Path] = []
    cwd = Path.cwd().resolve()
    candidates.extend([cwd, *cwd.parents])

    script_path = Path(__file__).resolve()
    candidates.extend(script_path.parents)

    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if (candidate / "AGENTS.md").exists():
            return candidate
        if (candidate / "config" / "capacities.json").exists():
            return candidate

    return Path(__file__).resolve().parents[3]


WORKSPACE_ROOT = _detect_workspace_root()
DATA_DIR = WORKSPACE_ROOT / "data" / "capacities"
STRUCTURES_PATH = DATA_DIR / "structures.json"
SPACES_PATH = DATA_DIR / "spaces.json"
LOOKUP_CACHE_PATH = DATA_DIR / "lookup-cache.json"
STATE_PATH = DATA_DIR / "state.json"


def ensure_data_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def read_json(path: Path, default: Any) -> Any:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def write_json_atomic(path: Path, data: Any) -> None:
    ensure_data_dirs()
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        json.dump(data, tmp, indent=2, sort_keys=True)
        tmp.write("\n")
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, path)


def load_structures_cache() -> dict[str, Any]:
    return read_json(STRUCTURES_PATH, {})


def save_structures_cache(data: dict[str, Any]) -> None:
    write_json_atomic(STRUCTURES_PATH, data)


def load_spaces_cache() -> dict[str, Any]:
    return read_json(SPACES_PATH, {})


def save_spaces_cache(data: dict[str, Any]) -> None:
    write_json_atomic(SPACES_PATH, data)


def load_lookup_cache() -> dict[str, Any]:
    return read_json(LOOKUP_CACHE_PATH, {})


def save_lookup_cache(data: dict[str, Any]) -> None:
    write_json_atomic(LOOKUP_CACHE_PATH, data)


def load_state() -> dict[str, Any]:
    return read_json(STATE_PATH, {})


def save_state(state: dict[str, Any]) -> None:
    write_json_atomic(STATE_PATH, state)
