#!/usr/bin/env python3
"""头部老客户明细查询服务（高价值客户稳定性与复购基本盘分析）"""

from _http import api_post
from _errors import ServiceError

VALID_DATE_TYPES = {"RECENT_7", "RECENT_30"}
VALID_BUYER_TYPES = {"头部老客户", "新客户", "老客户", "流失客户"}
VALID_ORDER_BY = {"payAmount", "payAmtAll", "lastPayDate", "payParentOrderNum"}
VALID_ORDER = {"desc", "asc"}

def get_top_old_customers(
    date_type: str = "RECENT_7",
    buyer_type: str = "头部老客户",
    order_by: str = "payAmount",
    order: str = "desc",
    page: int = 1,
    page_size: int = 50,
) -> dict:
    """获取头部老客户明细（商家身份由 AK 自动识别）

    Args:
        date_type:  日期类型 RECENT_7/RECENT_30
        buyer_type: 买家类型，默认 "头部老客户"
        order_by:   排序字段（默认 payAmount）
        order:      排序方向 desc/asc
        page:       页码
        page_size:  每页数量

    Returns:
        API 响应 data 字段，包含头部老客户明细列表
    """
    if date_type not in VALID_DATE_TYPES:
        raise ValueError(f"date_type 必须为 {', '.join(sorted(VALID_DATE_TYPES))} 之一，当前值: {date_type}")
    if order_by not in VALID_ORDER_BY:
        raise ValueError(f"order_by 必须为 {', '.join(sorted(VALID_ORDER_BY))} 之一，当前值: {order_by}")
    if order not in VALID_ORDER:
        raise ValueError(f"order 必须为 desc/asc 之一，当前值: {order}")

    data = api_post("/api/seller_customer_detail/1.0.0", {
        "dateType": date_type,
        "buyerType": buyer_type,
        "orderBy": order_by,
        "order": order,
        "page": str(page),
        "pageSize": str(page_size),
    })

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")

    return data
