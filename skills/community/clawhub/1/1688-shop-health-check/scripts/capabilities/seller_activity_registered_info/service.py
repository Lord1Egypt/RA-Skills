#!/usr/bin/env python3
"""商家近 30 天活动参与信息查询服务"""

from _http import api_post
from _errors import ServiceError

def get_activity_registered_info(login_id: str = None) -> dict:
    """获取商家近 30 天活动参与及活动效果数据（商家身份由 AK 自动识别）

    Args:
        login_id: 店铺登录 ID，传入时通过 NEWTON_SHOP_LOGIN_ID 指定查询店铺

    Returns:
        API 响应 data 字段，包含活动列表（含访客、订单、GMV、同行基准等）
    """
    payload = {}
    if login_id:
        payload["NEWTON_SHOP_LOGIN_ID"] = login_id
    data = api_post("/api/alibaba.1688.seller.activity.registered.info/1.0.0", payload)

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")

    return data
