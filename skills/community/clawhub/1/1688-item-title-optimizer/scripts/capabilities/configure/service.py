#!/usr/bin/env python3
"""AK 配置服务 — 校验、状态查询"""

import os
import sys
from typing import Tuple

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

def validate_ak(ak: str) -> Tuple[bool, str]:
    """校验明文 AK 格式，返回 (is_valid, error_msg)"""
    if not ak:
        return False, "AK 不能为空"
    if len(ak) < 32:
        return False, f"AK 长度不足（当前 {len(ak)}，需要至少 32 位）"
    allowed = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-=")
    if not all(c in allowed for c in ak):
        return False, "AK 包含非法字符"
    return True, ""

def check_existing_config() -> Tuple[bool, str]:
    """检查是否已有 AK（从环境变量读取）"""
    env_ak = os.environ.get("ALI_1688_AK", "")
    if env_ak:
        return True, env_ak
    return False, ""
