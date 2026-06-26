#!/usr/bin/env python3
"""客户跟进话术建议服务"""

from _http import api_post
from _errors import ServiceError


def suggest_follow_up_script(nick_name: str = None, buyer_id_list: list = None, buyer_type: str = None) -> dict:
    """查询客户跟进话术建议

    优先批量调用：buyer_id_list 不为空时，一次调用即可返回多个客户的话术建议；
    nick_name 仅在没有 buyer_id_list 时作为单查兜底。
    buyer_type 用于指定话术类型：lostRiskType-流失风险（挽留话术）, wakeUpType-商机唤醒（唤醒话术）
    """
    body = {}
    if buyer_id_list:
        body["buyerIdList"] = buyer_id_list
    elif nick_name:
        body["nickName"] = nick_name
    
    # 新增：传递 buyer_type 参数
    if buyer_type:
        body["buyerType"] = buyer_type
    
    data = api_post("/api/zkt_buyer_suggest_info_query/1.0.0", body)
    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")
    return data
