from __future__ import annotations

import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        os.environ.setdefault(key.strip(), value.strip())


def load_local_env() -> None:
    candidates = [
        Path.cwd() / '.env.local',
        Path.cwd() / '.env',
        ROOT_DIR / '.env.local',
        ROOT_DIR / '.env',
    ]
    for item in candidates:
        _load_env_file(item)


def get_required(key: str) -> str:
    load_local_env()
    value = os.environ.get(key, '').strip()
    if not value:
        raise RuntimeError(f'缺少配置：{key}')
    return value


def get_optional(key: str, default: str) -> str:
    load_local_env()
    return os.environ.get(key, default).strip() or default
