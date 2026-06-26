#!/usr/bin/env python3
"""总询盘客户查询服务"""

from typing import List, Optional

from _http import api_post
from _errors import ServiceError


def find_total_inquiry_customers(
    buyer_type: str = None,
    follow_up_state_list: List[str] = None,
    nick_name: str = None,
    tag_list: List[str] = None,
    start_time: str = None,
    end_time: str = None,
    min_pay_amt_180d: int = None,
    max_pay_amt_180d: int = None,
    last_sales_name: str = None,
    identity_list: List[str] = None,
    is_buyer_active: int = None,
    page_size: int = 10,
) -> dict:
    """查询当前商家的总询盘客户列表（支持多种筛选条件）"""
    body = {}
    if buyer_type is not None:
        body["buyerType"] = buyer_type
    if follow_up_state_list is not None:
        body["followUpStateList"] = follow_up_state_list
    if nick_name is not None:
        body["nickName"] = nick_name
    if tag_list is not None:
        body["tagList"] = tag_list
    if start_time is not None:
        body["startTime"] = start_time
    if end_time is not None:
        body["endTime"] = end_time
    if min_pay_amt_180d is not None:
        body["minPayAmt180d"] = min_pay_amt_180d
    if max_pay_amt_180d is not None:
        body["maxPayAmt180d"] = max_pay_amt_180d
    if last_sales_name is not None:
        body["lastSalesName"] = last_sales_name
    if identity_list is not None:
        body["identityList"] = identity_list
    if is_buyer_active is not None:
        body["isBuyerActive"] = is_buyer_active
    if page_size is not None:
        body["pageSize"] = page_size

    data = api_post("/api/zkt_buyer_base_info_query/1.0.0", body)
    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")
    return data
