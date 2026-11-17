#!/usr/bin/env python3
"""店铺维度数据查询服务"""

import logging

from _http import api_post
from _errors import ServiceError

logger = logging.getLogger('get_shop_data')


def get_shop_data() -> dict:
    """获取店铺维度数据，作为商品评分的对比基准。

    Returns:
        API 响应 data 字段，包含店铺支付金额、支付买家数、在线商品数等
    """
    data = api_post(
        "/api/alibaba.1688.skill.item.select.get.shop.data/1.0.0",
        {},
    )

    logger.info("api_post returned type=%s, value=%s", type(data).__name__, str(data)[:300])

    # _http.py 循环剥壳可能剥成 list / None / str，统一处理
    if isinstance(data, list):
        if not data:
            raise ServiceError("店铺数据为空，请确认店铺有经营数据")
        data = data[0]

    if not isinstance(data, dict):
        raise ServiceError(
            f"格式异常（api_post 返回 {type(data).__name__}），请稍后重试"
        )

    return data
