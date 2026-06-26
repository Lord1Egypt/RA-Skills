#!/usr/bin/env python3
"""商家异常商品列表查询服务

通过 1688 Skills 网关调用 MCP 工具 `seller_import_abnormal_offer`，
返回需要商家重点关注的异常商品（多个异常榜单取交集）。
"""

from _http import api_post
from _errors import ParamError, ServiceError

# 支持的 dateType 取值
ALLOWED_DATE_TYPES = {"RECENT_7", "RECENT_30"}

# 支持的 device 取值
ALLOWED_DEVICES = {"ALL", "PC", "APP"}

# MCP 工具网关路径
_API_PATH = "/api/seller_import_abnormal_offer/1.0.0"


def get_abnormal_offers(date_type: str = "RECENT_7", device: str = "ALL") -> list:
    """查询商家异常商品列表。

    Args:
        date_type: 日期类型，可选 RECENT_7（近 7 天）、RECENT_30（近 30 天）。默认 RECENT_7。
        device:    设备筛选，可选 ALL / PC / APP。默认 ALL。

    Returns:
        异常商品列表，每条包含 itemId、offerTitle、reason、valueMap 等字段。
    """
    date_type = (date_type or "RECENT_7").strip().upper()
    device = (device or "ALL").strip().upper()

    if date_type not in ALLOWED_DATE_TYPES:
        raise ParamError(
            f"dateType 取值非法：{date_type}；可选：{', '.join(sorted(ALLOWED_DATE_TYPES))}"
        )
    if device not in ALLOWED_DEVICES:
        raise ParamError(
            f"device 取值非法：{device}；可选：{', '.join(sorted(ALLOWED_DEVICES))}"
        )

    payload = {
        "dateType": date_type,
        "device": device,
    }

    data = api_post(_API_PATH, payload, timeout=60)

    if data is None:
        raise ServiceError("异常商品数据为空，请确认账号是否已沉淀有效数据")

    # 兼容多层封装：data 可能直接是 list，也可能是 dict 包了 data 字段
    if isinstance(data, dict):
        items = data.get("data") or data.get("items") or []
        if isinstance(items, str):
            import json
            try:
                items = json.loads(items)
            except json.JSONDecodeError:
                items = []
    elif isinstance(data, list):
        items = data
    else:
        items = []

    return items
