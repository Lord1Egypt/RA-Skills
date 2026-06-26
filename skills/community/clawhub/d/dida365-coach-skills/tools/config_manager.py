"""管理 Dida Coach 默认配置与用户覆盖配置。"""

from __future__ import annotations

import os
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


def _default_config_path() -> Path:
    override = os.environ.get("DIDA_COACH_DEFAULT_CONFIG_PATH")
    if override:
        return Path(override).expanduser()
    return Path(__file__).resolve().parent.parent / "config.yaml"


def _user_config_path() -> Path:
    override = os.environ.get("DIDA_COACH_USER_CONFIG_PATH")
    if override:
        return Path(override).expanduser()

    home = Path.home()
    candidates = [
        home / ".codex" / "skills" / "dida-coach" / "config.yaml",
        home / ".claude" / "skills" / "dida-coach" / "config.yaml",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def _read_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if isinstance(data, dict):
        return data
    raise ValueError(f"配置文件不是字典结构：{path}")


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> None:
    for key, value in override.items():
        if isinstance(base.get(key), dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


def load_config() -> Dict[str, Any]:
    """加载默认配置，并叠加用户自定义配置。"""

    config = deepcopy(_read_yaml(_default_config_path()))
    user_path = _user_config_path()
    if user_path.exists():
        user_config = _read_yaml(user_path)
        _deep_merge(config, user_config)
    return config


def get_personality_preset(config: Dict[str, Any]) -> str:
    """返回当前文风预设。"""

    return str(config.get("personality", {}).get("preset", "warm_encouraging"))


def get_work_method_config(
    config: Dict[str, Any],
    method_name: Optional[str] = None,
) -> Dict[str, Any]:
    """返回指定或默认工作法配置。"""

    methods = config.get("work_method", {}).get("methods", {})
    if not isinstance(methods, dict):
        return {}

    if method_name:
        candidate = methods.get(method_name)
        if isinstance(candidate, dict):
            return candidate

    default_method = str(config.get("work_method", {}).get("default", "flexible_pomodoro"))
    default_config = methods.get(default_method, {})
    return default_config if isinstance(default_config, dict) else {}


def get_reminder_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """返回提醒配置。"""

    reminders = config.get("reminders", {})
    return reminders if isinstance(reminders, dict) else {}


def save_user_config(updates: Dict[str, Any]) -> None:
    """将用户配置更新写入本地覆盖文件。"""

    config_path = _user_config_path()
    current: Dict[str, Any] = {}
    if config_path.exists():
        current = _read_yaml(config_path)

    _deep_merge(current, updates)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with config_path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(current, handle, allow_unicode=True, sort_keys=False)
