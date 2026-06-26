"""
Server URL 配置

优先级:
  1. 显式传入的 server_url / --server 参数
  2. 环境变量 DEX_QUANT_SERVER_URL
  3. 默认生产地址
"""

from __future__ import annotations

import os

DEFAULT_SERVER_URL = "https://quant.supersafeclaw.com"


def resolve_server_url(server_url: str | None = None) -> str:
    """解析回测服务器地址。"""
    value = (server_url or "").strip() or os.getenv("DEX_QUANT_SERVER_URL", "").strip()
    return value or DEFAULT_SERVER_URL
