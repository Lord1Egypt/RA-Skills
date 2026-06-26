#!/usr/bin/env python3
"""优秀商品榜单查询服务

支持四种榜单：
- payAmt           成交主力
- uv               流量主力
- payNewByrCnt     拉新主力
- itemMultiByrCnt  复购主力
"""

from _http import api_post
from _errors import ServiceError

VALID_RANGE_TYPES = {"RECENT_7", "RECENT_30"}
VALID_DEVICES = {"ALL", "PC", "WIRELESS"}
VALID_ORDER_BY = {"payAmt", "uv", "payNewByrCnt", "itemMultiByrCnt"}
VALID_ORDER = {"desc", "asc"}

DEFAULT_INDEX_CODE = "revealCnt,uv,payByrCnt,payRate,payAmt,payItemQty,payNewByrCnt,payOldByrCnt,itemMultiByrCnt,itemMultiByrPayAmt"

def get_top_offer(
    order_by: str = "payAmt",
    range_type: str = "RECENT_7",
    device: str = "ALL",
    order: str = "desc",
    page: int = 1,
    page_size: int = 50,
    index_code: str = DEFAULT_INDEX_CODE,
) -> dict:
    """获取优秀商品榜单（商家身份由 AK 自动识别）

    Args:
        order_by:   排序字段 payAmt/uv/payNewByrCnt/itemMultiByrCnt
        range_type: 时间范围 RECENT_7/RECENT_30
        device:     设备类型 ALL/PC/WIRELESS
        order:      排序方向 desc/asc
        page:       页码
        page_size:  每页数量
        index_code: 返回的指标列（逗号分隔）

    Returns:
        API 响应 data 字段，包含商品列表
    """
    if order_by not in VALID_ORDER_BY:
        raise ValueError(f"order_by 必须为 {', '.join(sorted(VALID_ORDER_BY))} 之一，当前值: {order_by}")
    if range_type not in VALID_RANGE_TYPES:
        raise ValueError(f"range_type 必须为 {', '.join(sorted(VALID_RANGE_TYPES))} 之一，当前值: {range_type}")
    if device not in VALID_DEVICES:
        raise ValueError(f"device 必须为 {', '.join(sorted(VALID_DEVICES))} 之一，当前值: {device}")
    if order not in VALID_ORDER:
        raise ValueError(f"order 必须为 desc/asc 之一，当前值: {order}")

    data = api_post("/api/seller_top_offer/1.0.0", {
        "order": order,
        "orderBy": order_by,
        "device": device,
        "rangeType": range_type,
        "indexCode": index_code,
        "page": str(page),
        "pageSize": str(page_size),
    })

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")

    return data
