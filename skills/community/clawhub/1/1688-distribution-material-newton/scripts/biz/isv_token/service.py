#!/usr/bin/env python3
"""ISV Token 获取服务 — 调用 distribution_isv_token 接口"""

import os
import sys

_PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
sys.path.insert(0, _PROJECT_ROOT)

from scripts._sys._http import api_post
from scripts._sys._errors import ServiceError
from scripts.biz.isv_token.token_store import get_token, save_token, is_token_expired, get_remaining_hours


def fetch_isv_token(app_key: str, expire_hours: int = 24, force_refresh: bool = False) -> str:
    """
    获取 ISV token。

    流程：
    1. 检查本地是否已有有效 token（除非 force_refresh=True）
    2. 如果 token 不存在或已过期，调用 distribution_isv_token 接口获取新 token
    3. 将新 token 保存到本地文件
    """
    # 1. 检查本地是否有有效 token
    if not force_refresh:
        existing_token = get_token(app_key)
        if existing_token and not is_token_expired(app_key):
            return existing_token

    # 2. 调用接口获取新 token
    data = api_post(
        tool_name="distribution_isv_token",
        body={"appKey": app_key, "expireHours": expire_hours},
        timeout=30,
    )

    token = data.get("model")
    if not token:
        msg = data.get("message") or data.get("msg") or "获取 ISV token 失败"
        raise ServiceError(f"获取 ISV token 失败（AppKey: {app_key}）：{msg}")

    # 3. 保存到本地
    save_token(app_key, str(token), expire_hours)

    return str(token)


def check_token_status(app_key: str) -> dict:
    """检查指定 AppKey 的 token 状态。"""
    token = get_token(app_key)
    expired = is_token_expired(app_key) if token else True

    return {
        "exists": token is not None,
        "expired": expired,
        "token": token,
        "remainingHours": get_remaining_hours(app_key) if token and not expired else None,
    }
