#!/usr/bin/env python3
"""店铺健康检查聚合工具服务

单工具、三 code：order_risk（订单履约）/ shop_punish（合规扣分）/ feedback（买家评价）。
仅透传后端业务数据，不在 Python 侧加工。
"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _http import api_post
from _errors import ServiceError

# 支持的 code 枚举
VALID_CODES = ("order_risk", "shop_punish", "feedback")


def get_shop_health_check(code: str, login_id: str = None) -> dict:
    """店铺健康检查聚合取数

    Args:
        code:     order_risk / shop_punish / feedback 之一
        login_id: 可选，目标店铺 loginId，用于多店铺查询

    Returns:
        工具结果 map（含 success / message / data 三键）
    """
    if code not in VALID_CODES:
        raise ServiceError("参数错误：code 必须为 order_risk / shop_punish / feedback 之一")

    payload = {"code": code}
    if login_id:
        payload["NEWTON_SHOP_LOGIN_ID"] = login_id

    # api_post 已剥掉网关最外层 data，但本工具网关在工具结果 map 外还多包了一层 data
    result = api_post("/api/alibaba.1688.tool.shop.health.check/1.0.0", payload)
    if not isinstance(result, dict):
        raise ServiceError("格式异常，请稍后重试")
    # 下钻一层取真正的工具结果 map（含 success / message / data 三键）；
    # 业务 payload 不含 success 键，以此做确定式区分，不使用循环剥壳
    inner = result.get("data")
    if isinstance(inner, dict) and "success" in inner:
        return inner
    return result
