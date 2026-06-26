from __future__ import annotations

import os


def get_required(key: str) -> str:
    value = os.environ.get(key, '').strip()
    if not value:
        raise RuntimeError(f'缺少配置：{key}。当前版本只允许从进程环境变量读取，不会读取 .env / .env.local，也不会临时提示输入。')
    return value


def get_optional(key: str, default: str) -> str:
    return os.environ.get(key, default).strip() or default
