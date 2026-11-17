# -*- coding: utf-8 -*-
"""
询盘对话配置能力实现

调用 alibaba.1688.a2a.gateway 网关，按 serviceName 路由到
cbuAiInquiryOrderSingleRoundWriteService，写入用户的询盘对话轮次配置。

接口入参（body）：
  - userId：买家 userId。由网关根据 AK 签名自动注入（占位符 __userId__），无需手动传递
  - serviceName：固定 cbuAiInquiryOrderSingleRoundWriteService
  - params：配置项 map，当前仅含 orderSingleRound
    - orderSingleRound: true  → 单轮对话（不需要 AI 自动多轮回复）
    - orderSingleRound: false → 多轮对话（AI 自动多轮回复）

接口出参：
  - success：bool，配置是否成功
"""

import logging
import time
from typing import Dict, Any

from _http import api_post
from _errors import ServiceError
from settings import settings

logger = logging.getLogger(__name__)

# 固定路由的服务名，由网关按此值分发到对应 Java 服务
_SERVICE_NAME = "cbuAiInquiryOrderSingleRoundWriteService"

# userId 占位符：网关根据 AK 签名自动替换为真实买家 userId
_USER_ID_PLACEHOLDER = "__userId__"


def inquiry_config(
    order_single_round: bool = True,
    user_id: str = _USER_ID_PLACEHOLDER,
) -> Dict[str, Any]:
    """
    写入询盘对话轮次配置。

    Args:
        order_single_round: 是否单轮对话。默认 True（单轮）；
            用户明确要求支持多轮对话时传 False
        user_id: 买家 userId，默认使用网关占位符 __userId__（自动注入）

    Returns:
        {"success": bool, "orderSingleRound": bool, "elapsed_seconds": float}
    """
    # 该后端服务 params.orderSingleRound 需原生布尔（非字符串）
    body: Dict[str, Any] = {
        "userId": user_id,
        "serviceName": _SERVICE_NAME,
        "params": {
            "orderSingleRound": order_single_round,
        },
    }

    start_time = time.time()

    resp = api_post(
        path=settings.A2A_GATEWAY_PATH,
        body=body,
        timeout=settings.TOOL_TIMEOUT,
    )

    elapsed = round(time.time() - start_time, 1)

    # _http 层已拦截 {"success": false} 的业务错误，走到这里说明请求成功
    # 兼容 data 可能包一层 model / 直接返回布尔的情况
    success = True
    data = resp.get("data")
    if isinstance(data, dict):
        if "model" in data and isinstance(data["model"], dict):
            success = bool(data["model"].get("suc", data["model"].get("success", True)))
        elif "suc" in data or "success" in data:
            success = bool(data.get("suc", data.get("success", True)))

    if not success:
        raise ServiceError("对话配置写入失败: {}".format(resp))

    return {
        "success": success,
        "orderSingleRound": order_single_round,
        "elapsed_seconds": elapsed,
    }
