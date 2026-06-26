#!/usr/bin/env python3
"""采购数字人服务 — 解析采购需求并发起采购任务"""

from _http import api_post
from _errors import ParamError, ServiceError

API_PATH = "/api/1688_procurement_digital_human_tool/1.0.0"


def create_procurement_task(offer_name: str, count: str, demand: str) -> dict:
    """
    创建采购任务

    Args:
        offer_name: 商品名称，如 "衣服"、"螺丝"
        count: 采购数量，如 "10"
        demand: 采购需求描述，如 "价格便宜"、"要求包邮"

    Returns:
        API 返回的结果数据

    Raises:
        ParamError: 参数缺失或不合法
        ServiceError: 服务端异常
    """
    if not offer_name:
        raise ParamError("商品名称（offerName）不能为空")
    if not count:
        raise ParamError("采购数量（count）不能为空")
    if not count.isdigit():
        raise ParamError("采购数量（count）必须是纯数字，不能包含单位（如\"斤\"、\"件\"等），请去掉单位后重试")
    if not demand:
        raise ParamError("采购需求（demand）不能为空")

    body = {
        "offerName": offer_name,
        "count": count,
        "demand": demand,
    }

    resp = api_post(API_PATH, body)

    if not isinstance(resp, dict):
        raise ServiceError("API 返回格式异常，请稍后重试")
    return resp
