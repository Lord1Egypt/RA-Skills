#!/usr/bin/env python3
"""
全局常量
"""

import os
from pathlib import Path

# Skill 版本
SKILL_VERSION = "0.1.0"
SKILL_NAME = "1688-distribution-shop-bind-newton"

# 1688 网关地址
BASE_URL = os.environ.get(
    "DISTRIBUTE_BASE_URL",
    "https://skills-gateway.1688.com",
)

# OpenClaw 配置文件路径
OPENCLAW_CONFIG_PATH: Path = Path(
    os.environ.get("OPENCLAW_CONFIG_DIR", Path.home() / ".openclaw")
) / "openclaw.json"

# 浏览器配置
BROWSER_TIMEOUT = 30  # 浏览器操作超时（秒）
QR_LOGIN_TIMEOUT = 180  # 扫码登录超时（秒）

# 绑店流程配置
FLOW_POLL_INTERVAL = 3  # 流程状态轮询间隔（秒）
FLOW_POLL_MAX_RETRIES = 60  # 流程状态轮询最大次数

# 重试配置
MAX_RETRIES = 3
RETRY_DELAY_BASE = 1
