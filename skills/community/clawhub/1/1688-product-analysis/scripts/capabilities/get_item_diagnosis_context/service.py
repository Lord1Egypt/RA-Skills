#!/usr/bin/env python3
"""商品诊断上下文聚合 —— seller-agent HSF Tool 薄透传。

身份解析、三路聚合编排（profile/performance/增强）与超时降级已收敛到
seller-agent BotToolService.alibaba.1688.get.item.diagnosis.context（HSF）。本层只做：
itemId 本地校验 → Gateway 调用 → 信封判定（业务失败/结构异常/原样透传）。
"""

import re

from _errors import ParamError, RateLimitError, ServiceError, SkillError
from _http import api_post

_API_PATH = "/api/alibaba.1688.get.item.diagnosis.context/1.0.0"
_MAX_JAVA_LONG = 9223372036854775807
_REQUIRED_KEYS = ("itemId", "loginId", "offerData")


def _require_item_id(item_id):
    value = str(item_id or "").strip()
    if not re.fullmatch(r"\d{10,}", value) or not 0 < int(value) <= _MAX_JAVA_LONG:
        raise ParamError("item_id 必须是 10 位及以上且在 Java Long 正数范围内的纯数字")
    return value


def get_item_diagnosis_context(item_id: str) -> dict:
    """聚合查询单个商品的诊断上下文（薄透传 seller-agent payload）。

    成功：原样返回 payload（itemId/loginId/shopName/title/imageUrl/
    identityResolvedBy/offerData/enhancements/traceId/protocolVersion）。
    业务失败：payload.success==False → SkillError(data=失败 payload)。
    结构异常：缺 itemId/loginId/offerData → SkillError(internal_error)。
    技术异常：api_post 抛出后补挂 failureType=internal_error 再上抛。
    """
    item_id = _require_item_id(item_id)
    try:
        payload = api_post(_API_PATH, {"ITEM_ID": item_id}, timeout=60)
    except (ParamError, RateLimitError, ServiceError) as error:
        error.data = {
            "failureType": "internal_error",
            "retryable": True,
            "itemId": item_id,
        }
        raise
    except Exception as error:
        # 非 SkillError 泄漏路径（网关 200 非 JSON 体、重定向/URL 异常等）：
        # 包装为带 failureType data 的 ServiceError，保证 CLI 失败形状可分类
        wrapped = ServiceError("商品诊断上下文查询失败，请稍后重试")
        wrapped.data = {
            "failureType": "internal_error",
            "retryable": True,
            "itemId": item_id,
        }
        raise wrapped from error

    if isinstance(payload, dict) and payload.get("success") is False:
        raise SkillError(str(payload.get("message") or "商品诊断上下文查询失败"), data=payload)
    if not isinstance(payload, dict) or any(not payload.get(key) for key in _REQUIRED_KEYS):
        raise SkillError("聚合响应结构异常", data={
            "failureType": "internal_error",
            "retryable": True,
            "itemId": item_id,
        })
    return payload
