#!/usr/bin/env python3
"""同款选品、竞品分析 V2 诊断的查询服务。"""

from typing import Optional

from _errors import ParamError, ServiceError
from _http import api_post

# MCP 工具网关路径（code = alibaba.1688.newton.same.competition.offer.compare.data）
_API_PATH = "/api/alibaba.1688.newton.same.competition.offer.compare.data/1.0.0"


def get_same_offer_competition(
    offer_id: str,
    login_id: Optional[str] = None,
    timeout: int = 90,
    deadline=None,
) -> dict:
    """按同款 Top1 选品，并返回竞品分析 V2 的完整诊断事实。"""
    normalized_offer_id = str(offer_id or "").strip()
    if not normalized_offer_id:
        raise ParamError("offer_id 不能为空")

    # This tool's registered input contract uses camelCase field names.
    payload = {"offerId": normalized_offer_id}
    normalized_login_id = str(login_id or "").strip()
    if normalized_login_id:
        payload["shopLoginId"] = normalized_login_id

    data = api_post(_API_PATH, payload, timeout=timeout, _deadline=deadline)
    if not isinstance(data, dict):
        raise ServiceError("同款竞品分析数据格式异常，请稍后重试")
    return data
