#!/usr/bin/env python3
"""采购单汇总服务 — 查询采购单汇总信息、格式化"""

import json
import re
from typing import List, Optional, Dict, Any

from _http import api_post
from _errors import ServiceError
from _const import SKILL_NAME, SKILL_VERSION, SITE


def _append_tracelog(url: str) -> str:
    """为链接追加 tracelog 参数"""
    if not url:
        return url
    separator = "&" if "?" in url else "?"
    return f"{url}{separator}tracelog=88sytskill"


def _build_markdown(data: Dict[str, Any]) -> str:
    if not data:
        return "未返回数据。"

    success = data.get("success")
    if not success:
        code = data.get("responseCode", "-")
        msg = data.get("responseMessage", "未知错误")
        return f"错误代码: {code}\n错误信息: {msg}"

    data_list = data.get("data", {}).get("dataList", [])

    if not data_list:
        return "暂无汇总数据。"

    parts: List[str] = ["## 采购单汇总信息"]

    for item in data_list:
        name = item.get("name", "-")
        value = item.get("value", "-")
        link = item.get("link", "")

        # 尝试将 name 翻译为中文
        name_cn = name
        name_map = {
            "pendingConfirm": "待确认",
            "receivedAmount": "已收款金额",
            "pendingReceiveAmount": "待收款金额",
            "pendingPayAmount": "待支付金额",
            "paidAmount": "已支付金额"
        }
        name_cn = name_map.get(name, name)

        if link:
            link = _append_tracelog(link)
            parts.append(f"- {name_cn}: {value} [查看详情]({link})")
        else:
            parts.append(f"- {name_cn}: {value}")

    return "\n\n".join(parts)


def query_contract_summary() -> dict:
    """
    查询采购单汇总信息

    Returns:
        {"success": bool, "markdown": str, "data": dict}

    Raises:
        SkillError 子类: API 调用失败
    """
    body = {
        "site": SITE,
        "skillName": SKILL_NAME,
        "skillVersion": SKILL_VERSION
    }

    model = api_post("/api/SYT_QUERY_CONTRACT_SUMMARY/1.0.0", body, timeout=10)
    if not isinstance(model, dict):
        raise ServiceError("查询异常，请稍后重试")

    markdown = _build_markdown(model)
    return {"success": model.get("success"), "markdown": markdown, "data": model}
