#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent


def _parse_env_file(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        data[k] = v
    return data


def load_env() -> None:
    env_path = SKILL_ROOT / ".env"
    for k, v in _parse_env_file(env_path).items():
        os.environ.setdefault(k, v)


def env_path(name: str, default: Path) -> Path:
    v = os.environ.get(name)
    if v:
        return Path(v).expanduser().resolve()
    return default.expanduser().resolve()


def env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, str(default)))
    except Exception:
        return default


def env_str(name: str, default: str) -> str:
    return os.environ.get(name, default)


load_env()

OPENCLAW_WORKSPACE = env_path("OPENCLAW_WORKSPACE", Path.home() / ".openclaw" / "workspace")
KB_CONFIG_PATH = env_path("KB_CONFIG_PATH", OPENCLAW_WORKSPACE / "knowledge-bases" / "config" / "repos.json")
PROMPT_SHIELD_SCRIPT = env_path(
    "PROMPT_SHIELD_SCRIPT",
    OPENCLAW_WORKSPACE / "skills" / "prompt-shield-lite" / "scripts" / "detect-injection.sh",
)
KB_VENV_PYTHON = env_path("KB_VENV_PYTHON", OPENCLAW_WORKSPACE / ".venvs" / "duru-kb" / "bin" / "python")
USER_AGENT = env_str("KB_USER_AGENT", "Mozilla/5.0 (compatible; duru-obsidian-kb/0.5)")
MIN_CONTENT_LENGTH = env_int("KB_MIN_CONTENT_LENGTH", 700)
MAX_PREVIEW_LENGTH = env_int("KB_MAX_PREVIEW_LENGTH", 4000)
MAX_SEGMENTS = env_int("KB_MAX_SEGMENTS", 8)
