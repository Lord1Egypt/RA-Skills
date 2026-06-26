#!/usr/bin/env python3
"""账号服务 — 查询账号账号、格式化"""

import json
import os
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from _http import api_post
from _errors import ServiceError
from _const import SKILL_NAME, SKILL_VERSION, SITE


def _build_markdown(biz_data: Dict[str, Any]) -> str:
    if not biz_data:
        return "未返回账号数据。"

    success = biz_data.get("success")

    if not success:
        return f"错误代码: {biz_data.get('responseCode')}\n错误信息: {biz_data.get('responseMessage')}"

    parts: List[str] = ["## 基本信息"]
    parts.append(f"- 账号: {biz_data.get('loginId')}")
    parts.append(f"- 姓名/企业名称: {biz_data.get('name')}")
    parts.append("## 账号状态")
    parts.append(f"- 签约状态: {'✅' if biz_data.get('hasSign') else '❌'} ")
    parts.append(f"- 认证状态: {'✅' if biz_data.get('hasVerified') else '❌'} ")
    parts.append(f"- 绑卡状态: {'✅' if biz_data.get('hasBoundCard') else '❌'} ")

    return "\n\n".join(parts)

def query_account() -> dict:
    """
    查询账号状态

    Args:
        NONE

    Returns:
        {"success": bool, "markdown": str, "data": dict}

    Raises:
        ValueError: 渠道名不合法
        SkillError 子类: API 调用失败
    """
    body = {"site": SITE, "skillName": SKILL_NAME, "skillVersion": SKILL_VERSION}
    model = api_post("/api/SYT_QUERY_USER_INFO/1.0.0", body, timeout=10)
    if not isinstance(model, dict):
        raise ServiceError("查询异常，请稍后重试")

    markdown = _build_markdown(model)
    return { "success": model.get("success"), "markdown": markdown, "data": model}
