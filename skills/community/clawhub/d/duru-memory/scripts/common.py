#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = SKILL_DIR / "config.yaml"
EXAMPLE_CONFIG_PATH = SKILL_DIR / "config.example.yaml"


def load_config(config_path: str | None = None) -> dict[str, Any]:
    if config_path:
        paths = [Path(config_path).resolve()]
    else:
        paths = [DEFAULT_CONFIG_PATH, EXAMPLE_CONFIG_PATH]
    for path in paths:
        if not path.exists():
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if isinstance(data, dict):
            return data
    return {}


def cfg_get(cfg: dict[str, Any], dotted: str, default: Any = None) -> Any:
    cur: Any = cfg
    for part in dotted.split('.'):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def env_or_cfg(env_name: str, cfg: dict[str, Any], dotted: str, default: Any = None) -> Any:
    return os.getenv(env_name, cfg_get(cfg, dotted, default))


def skill_dir() -> Path:
    return SKILL_DIR
