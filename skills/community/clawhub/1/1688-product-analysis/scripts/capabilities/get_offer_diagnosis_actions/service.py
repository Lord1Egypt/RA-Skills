#!/usr/bin/env python3
"""商品库明细行动点查询服务。"""

from typing import Optional

from _errors import ParamError, ServiceError
from _http import api_post

# MCP 工具网关路径（code = alibaba.1688.newton.offer.panorama.query.offer.diagnosis）
_API_PATH = "/api/alibaba.1688.newton.offer.panorama.query.offer.diagnosis/1.0.0"


def get_offer_diagnosis_actions(
    offer_id: str,
    login_id: Optional[str] = None,
    timeout: int = 30,
    deadline=None,
) -> dict:
    """查询当前用户可访问商品的 AI 分析、状态和行动点。"""
    normalized_offer_id = str(offer_id or "").strip()
    if not normalized_offer_id:
        raise ParamError("offer_id 不能为空")

    payload = {"offer_id": normalized_offer_id}
    if login_id:
        payload["NEWTON_SHOP_LOGIN_ID"] = login_id

    data = api_post(_API_PATH, payload, timeout=timeout, _deadline=deadline)
    if not isinstance(data, dict):
        raise ServiceError("商品库行动点数据格式异常，请稍后重试")

    if data.get("success") is False or data.get("errorMsg"):
        raise ServiceError(str(data.get("errorMsg") or "商品库行动点查询失败"))

    # HSF 返回分页对象，Skill 只消费当前 offer 的一行明细。统一在 tool 层
    # 精确取值，避免 workflow 把 {offerList: [...]} 误判为未命中商品。
    if str(data.get("offerId") or "") == normalized_offer_id:
        return data

    offer_list = data.get("offerList")
    if offer_list is None:
        return {}
    if not isinstance(offer_list, list):
        raise ServiceError("商品库行动点数据格式异常，请稍后重试")

    for item in offer_list:
        if isinstance(item, dict) and str(item.get("offerId") or "") == normalized_offer_id:
            return item
    return {}
