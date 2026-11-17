"""判定层连接信息的读取：环境变量优先，其次本地密钥文件。

本地文件用于放 API Key 等敏感值，路径：
  1. 环境变量 `DND_JUDGE_ENV_FILE` 指定的文件
  2. dnd-engine 根目录下的 `.judge.env`

文件格式（每行 KEY=VALUE，# 开头为注释）：
    DND_JUDGE_BASE_URL=https://api.deepseek.com
    DND_JUDGE_MODEL=deepseek-chat
    DND_JUDGE_API_KEY=sk-xxxx

为什么要有它：这样密钥只需写在本地文件里，不必出现在命令行、聊天记录或全局环境变量中。
本模块从不打印、不记录任何取值。
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

ENV_FILE_VAR = "DND_JUDGE_ENV_FILE"
DEFAULT_ENV_FILE = Path(__file__).resolve().parents[3] / ".judge.env"


def env_file_path() -> Path:
    override = os.environ.get(ENV_FILE_VAR, "").strip()
    return Path(override) if override else DEFAULT_ENV_FILE


@lru_cache(maxsize=1)
def _read_env_file() -> dict[str, str]:
    path = env_file_path()
    values: dict[str, str] = {}
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return values
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def get_env(name: str, default: str = "") -> str:
    """按 环境变量 → 本地文件 → 默认值 的顺序取值。"""
    value = os.environ.get(name, "")
    if value:
        return value
    return _read_env_file().get(name, default) or default


def reload_env_file() -> None:
    """清除缓存（写入文件后调用可立即生效）。"""
    _read_env_file.cache_clear()


def describe_env_source(name: str) -> str:
    """诊断用：返回取值来源（不返回值本身）。"""
    if os.environ.get(name):
        return "env"
    if name in _read_env_file():
        return "file"
    return "unset"
