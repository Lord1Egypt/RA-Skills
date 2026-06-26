#!/usr/bin/env python3
"""客户采购意图分析服务"""

from _http import api_post
from _errors import ServiceError


def analyze_customer_intent(nick_name: str = None, buyer_id_list: list = None) -> dict:
    """查询客户采购意图分析数据

    优先批量调用：buyer_id_list 不为空时，一次调用即可返回多个客户的意图分析；
    nick_name 仅在没有 buyer_id_list 时作为单查兜底。
    """
    body = {}
    if buyer_id_list:
        body["buyerIdList"] = buyer_id_list
    elif nick_name:
        body["nickName"] = nick_name
    data = api_post("/api/zkt_buyer_analysis_info_query/1.0.0", body)
    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")
    return data
