#!/usr/bin/env python3
"""AK 配置服务 — 校验、写入、状态查询"""

import os
import sys
from typing import Tuple

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))


def validate_ak(ak: str) -> Tuple[bool, str]:
    """校验 AK 格式"""
    if not ak:
        return False, "AK 不能为空"
    if len(ak) < 32:
        return False, f"AK 长度不足（当前 {len(ak)}，需要至少 32 位）"
    allowed = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-=")
    if not all(c in allowed for c in ak):
        return False, "AK 包含非法字符"
    return True, ""


def save_ak(api_key: str) -> bool:
    """将 AK 写入环境变量（当前进程立即生效）"""
    os.environ["ALI_1688_AK"] = api_key
    return True


def check_existing_config() -> Tuple[bool, str]:
    """检查当前是否已配置 AK"""
    env_ak = os.environ.get("ALI_1688_AK", "")
    if env_ak:
        return True, env_ak
    return False, ""
