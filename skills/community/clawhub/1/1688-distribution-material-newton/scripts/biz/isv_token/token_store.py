#!/usr/bin/env python3
"""ISV Token 本地存储管理"""

import json
import os
from pathlib import Path
from typing import Optional


TOKEN_FILE = Path.home() / ".isv_tokens.json"


def load_tokens() -> dict:
    """从本地文件加载所有 ISV token。"""
    if not TOKEN_FILE.exists():
        return {}
    try:
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_tokens(tokens: dict) -> None:
    """将所有 ISV token 保存到本地文件。"""
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(tokens, f, ensure_ascii=False, indent=2)
    # 设置文件权限为 600（仅当前用户可读写）
    os.chmod(TOKEN_FILE, 0o600)


def get_token(app_key: str) -> Optional[str]:
    """
    获取指定 AppKey 的 token。

    查找顺序：
    1. 环境变量 ISV_TOKEN_<APPKEY>（APPKEY 转大写）
    2. 本地配置文件 ~/.isv_tokens.json
    """
    # 1. 优先从环境变量读取
    env_key = f"ISV_TOKEN_{app_key.upper()}"
    env_token = os.environ.get(env_key)
    if env_token:
        return env_token

    # 2. 从本地文件读取
    tokens = load_tokens()
    token_info = tokens.get(app_key)
    if isinstance(token_info, dict):
        return token_info.get("token")
    return None


def save_token(app_key: str, token: str, expire_hours: int = 24) -> None:
    """保存 ISV token 到本地文件。"""
    import time

    tokens = load_tokens()
    tokens[app_key] = {
        "token": token,
        "expireTime": int(time.time()) + expire_hours * 3600,
        "expireHours": expire_hours,
    }
    save_tokens(tokens)


def is_token_expired(app_key: str) -> bool:
    """
    检查指定 AppKey 的 token 是否已过期。
    注意：环境变量提供的 token 视为永不过期。
    """
    import time

    env_key = f"ISV_TOKEN_{app_key.upper()}"
    if os.environ.get(env_key):
        return False

    tokens = load_tokens()
    token_info = tokens.get(app_key)
    if not isinstance(token_info, dict):
        return True

    expire_time = token_info.get("expireTime", 0)
    return time.time() > expire_time


def get_remaining_hours(app_key: str) -> Optional[float]:
    """获取指定 AppKey 的 token 剩余有效小时数。"""
    import time

    env_key = f"ISV_TOKEN_{app_key.upper()}"
    if os.environ.get(env_key):
        return None

    tokens = load_tokens()
    token_info = tokens.get(app_key)
    if not isinstance(token_info, dict):
        return None

    expire_time = token_info.get("expireTime", 0)
    remaining = expire_time - int(time.time())
    return round(remaining / 3600, 1) if remaining > 0 else None
