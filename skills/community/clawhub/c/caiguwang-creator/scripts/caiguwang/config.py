# -*- coding: utf-8 -*-
"""令牌与接口地址配置：~/.caiguwang/config.json + 环境变量"""
import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".caiguwang"
CONFIG_PATH = CONFIG_DIR / "config.json"

DEFAULT_BASE = "https://www.chinacaigu.com"
DEFAULT_TIMEOUT = 30


def get_api_base():
    return (os.environ.get("CAIGU_API_BASE") or DEFAULT_BASE).rstrip("/")


def load_token():
    env_token = os.environ.get("X_CAIGU_TOKEN")
    if env_token:
        return env_token.strip()
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return str(data.get("token", "")).strip()
    except (OSError, ValueError):
        return ""


def save_token(token):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump({"token": token}, f, ensure_ascii=False, indent=2)
    return str(CONFIG_PATH)
