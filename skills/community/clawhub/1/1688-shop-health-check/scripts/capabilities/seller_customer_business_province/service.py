#!/usr/bin/env python3
"""客户地域分布查询服务"""

from _http import api_post
from _errors import ServiceError

VALID_DATE_TYPES = {"RECENT_7", "RECENT_30"}

def get_customer_business_province(
    date_type: str = "RECENT_7",
    page: int = 1,
    page_size: int = 50,
    is_translate: bool = True,
    login_id: str = None,
) -> dict:
    """获取客户地域分布（商家身份由 AK 自动识别）

    Args:
        date_type:    日期类型 RECENT_7/RECENT_30
        page:         页码
        page_size:    每页数量
        is_translate: 是否翻译地域名称
        login_id:     店铺登录 ID，传入时通过 NEWTON_SHOP_LOGIN_ID 指定查询店铺

    Returns:
        API 响应 data 字段，包含按省份维度的支付买家数及占比
    """
    if date_type not in VALID_DATE_TYPES:
        raise ValueError(f"date_type 必须为 {', '.join(sorted(VALID_DATE_TYPES))} 之一，当前值: {date_type}")

    payload = {
        "dateType": date_type,
        "page": str(page),
        "pageSize": str(page_size),
        "isTranslate": "true" if is_translate else "false",
    }
    if login_id:
        payload["NEWTON_SHOP_LOGIN_ID"] = login_id
    data = api_post("/api/alibaba.1688.seller.customer.business.province/1.0.0", payload)

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")

    return data
