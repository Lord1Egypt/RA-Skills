#!/usr/bin/env python3
"""买家数据查询服务"""

from _http import api_post
from _errors import ServiceError, ParamError

def get_user_data(query_date: str, login_id: str = None) -> dict:
    """获取指定日期的买家数据

    Args:
        query_date: 查询日期，格式 YYYY-MM-DD
        login_id: 可选，目标店铺的 loginId，用于多店铺场景

    Returns:
        API 响应 data 字段，包含新买家数、老买家数及对应支付金额
    """
    if not query_date:
        raise ParamError("query_date 不能为空")

    data = api_post(
        "/api/alibaba.1688.skill.shop.daily.report.get.user.data/1.0.0",
        {"query_date": query_date},
        login_id=login_id,
    )

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")

    return data
