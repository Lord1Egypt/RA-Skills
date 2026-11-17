#!/usr/bin/env python3
"""商品概览统计查询服务"""

import logging

from _http import api_post
from _errors import ServiceError

logger = logging.getLogger('get_item_overview')


def get_item_overview() -> dict:
    """获取商品总体概况统计，了解数据规模以决定后续查询策略。

    Returns:
        API 响应 data 字段，包含商品总数、有销售商品数、总销售额等
    """
    data = api_post(
        "/api/alibaba.1688.skill.item.select.get.item.overview/1.0.0",
        {},
    )

    logger.info("api_post returned type=%s, value=%s", type(data).__name__, str(data)[:300])

    # _http.py 循环剥壳可能剥成 list / None / str，统一处理
    if isinstance(data, list):
        if not data:
            raise ServiceError("商品概览数据为空，请确认店铺有在售商品")
        data = data[0]

    if not isinstance(data, dict):
        raise ServiceError(
            f"格式异常（api_post 返回 {type(data).__name__}），请稍后重试"
        )

    return data
