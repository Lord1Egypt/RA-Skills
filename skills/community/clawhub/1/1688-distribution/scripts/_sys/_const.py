#!/usr/bin/env python3
"""
全局常量

所有模块统一从这里 import，禁止各模块自定义同名常量。
"""

import os
from pathlib import Path

# ── Skill 版本 ────────────────────────────────────────────────────────────────
SKILL_VERSION = "1.0.0"

# ── Workspace 目录自动发现 ────────────────────────────────────────────────────
def _find_workspace_dir() -> Path:
    """
    查找 workspace 目录。

    查找顺序：
    1. 环境变量 AGENT_WORK_ROOT + /workspace
    2. 从当前目录向上查找 workspace 目录
    3. 从当前目录向上查找 .skills 目录，其兄弟目录 workspace
    4. fallback 到当前目录
    """
    agent_work_root = os.environ.get("AGENT_WORK_ROOT")
    if agent_work_root:
        return Path(agent_work_root) / "workspace"

    cwd = Path.cwd().resolve()

    for parent in [cwd] + list(cwd.parents):
        if parent.name == "workspace":
            return parent

    for parent in cwd.parents:
        skills_dir = parent / ".skills"
        if skills_dir.exists() and skills_dir.is_dir():
            return parent / "workspace"

    return cwd


WORKSPACE_DIR = _find_workspace_dir()

# ── AK 本地存储 ──────────────────────────────────────────────────────────────
AK_DATA_DIR = Path(os.environ.get("AGENT_WORK_ROOT", str(WORKSPACE_DIR)), "workspace", ".1688-AK")
AK_STORE_FILE = AK_DATA_DIR / ".ak_store.json"

# ── AK 授权获取配置 ──────────────────────────────────────────────────────────
AUTHORIZE_ENDPOINT = "https://air.1688.com/app/tai/oauth_page/index.html"

import sys as _sys
# Windows 上 localhost 可能解析为 ::1（IPv6），固定用 127.0.0.1 避免 DNS 歧义，
# 同时确保 redirect_uri 与服务端绑定地址严格一致。
CALLBACK_HOST = "127.0.0.1" if _sys.platform == "win32" else "localhost"
# Windows 防火墙对绑定 0.0.0.0 的进程会拦截入向连接（即使是 localhost 流量）；
# 绑定 127.0.0.1 明确标识为 loopback，防火墙不干预。
CALLBACK_BIND_ADDRESS = "127.0.0.1" if _sys.platform == "win32" else "0.0.0.0"
CALLBACK_PORT_START = 8080
CALLBACK_PORT_RETRIES = 10
AUTHORIZATION_TIMEOUT = 300

# ── 日志文件路径 ──────────────────────────────────────────────────────────────
LOG_FILE = AK_DATA_DIR / "skill.log"
