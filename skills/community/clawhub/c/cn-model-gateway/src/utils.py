"""Utility functions."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict


def load_config(config_path: str) -> Dict[str, Any]:
    """Load and validate config.json."""
    p = Path(config_path)
    if not p.exists():
        raise FileNotFoundError(
            f"配置文件不存在: {config_path}\n"
            f"请复制 config.json.example 为 config.json 并填写 api_key。"
        )
    with open(p, "r", encoding="utf-8") as f:
        config = json.load(f)
    if not isinstance(config, dict):
        raise ValueError("config.json 格式错误：根节点必须是对象。")
    return config


def get_default_config_path() -> str:
    """Return default config path (next to the script or in user home)."""
    # First check current directory
    local = Path("config.json")
    if local.exists():
        return str(local.resolve())
    # Then check user home
    home_config = Path.home() / ".cn-model-gateway" / "config.json"
    if home_config.exists():
        return str(home_config)
    # Default to local
    return str(local.resolve())


def mask_api_key(key: str) -> str:
    """Mask API key for display: show first 4 and last 4 chars."""
    if len(key) <= 8:
        return "****"
    return key[:4] + "*" * (len(key) - 8) + key[-4:]


def format_size(size_bytes: int) -> str:
    """Format bytes to human-readable size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"
