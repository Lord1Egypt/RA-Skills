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


PROVIDER_NAMES = (
    "deepseek", "tongyi", "zhipu", "kimi", "hunyuan",
    "doubao", "minimax", "lingyi", "baichuan", "stepfun",
)


def normalize_api_keys(value: Any) -> List[str]:
    """v2.1.0: normalize a key field to a non-empty list without warnings.

    Accepts:
      - single string  -> [string]                 (legacy config, zero migration)
      - list of strings -> [k for k in list if k]  (new Key pool)
      - empty / None    -> []
    """
    if isinstance(value, str):
        return [value] if value.strip() else []
    if isinstance(value, (list, tuple)):
        return [str(k) for k in value if k and str(k).strip()]
    return []


def get_provider_keys(config: Dict[str, Any], provider: str) -> List[str]:
    """Return all keys for a provider from config.

    Supports both ``api_key`` and the short alias ``key``; both may be a
    single value (legacy) or an array (Key pool). No warnings for old config.
    """
    pcfg = config.get(provider, {}) or {}
    if not isinstance(pcfg, dict):
        return []
    raw = pcfg.get("api_key", pcfg.get("key"))
    return normalize_api_keys(raw)


def get_member(config: Dict[str, Any]) -> str:
    """v2.1.0: optional member tag for multi-tenant usage attribution."""
    member = config.get("member")
    if not member and isinstance(config.get("_meta"), dict):
        member = config["_meta"].get("member")
    return str(member) if member else "default"


def migrate_config_for_pool(config: Dict[str, Any]) -> Dict[str, Any]:
    """v2.1.0: produce a pool-aware view of config without mutating / warning.

    For each provider, ensures ``api_key`` is set to the FIRST key so existing
    adapters (which expect a string) keep working; stores the full list under
    a private ``_keys`` field consumed by KeyPoolManager. Legacy single-value
    configs are unchanged in behavior.
    """
    view = dict(config)
    for provider in PROVIDER_NAMES:
        pcfg = view.get(provider)
        if not isinstance(pcfg, dict):
            continue
        keys = get_provider_keys(config, provider)
        if not keys:
            continue
        new_pcfg = dict(pcfg)
        new_pcfg["api_key"] = keys[0]
        new_pcfg["_keys"] = keys
        view[provider] = new_pcfg
    return view


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
