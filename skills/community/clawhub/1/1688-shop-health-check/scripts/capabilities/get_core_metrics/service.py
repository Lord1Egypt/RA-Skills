#!/usr/bin/env python3
"""店铺核心指标同行对比及趋势数据查询服务"""

import json
from _http import api_post
from _errors import ServiceError

VALID_DATE_TYPES = {"RECENT_7", "RECENT_30"}

def get_core_metrics(date_type: str = "RECENT_7", login_id: str = None) -> dict:
    """获取店铺核心指标同行对比及趋势数据（商家身份由 AK 自动识别）

    Args:
        date_type:  日期类型 RECENT_7/RECENT_30
        login_id:   店铺登录 ID，传入时通过 NEWTON_SHOP_LOGIN_ID 指定查询店铺

    Returns:
        API 响应 data 字段，包含 core_metrics（同行对比）和 trend（趋势数据）
    """
    if date_type not in VALID_DATE_TYPES:
        raise ValueError(f"date_type 必须为 {', '.join(sorted(VALID_DATE_TYPES))} 之一，当前值: {date_type}")

    payload = {"date_type": date_type}
    if login_id:
        payload["NEWTON_SHOP_LOGIN_ID"] = login_id
    data = api_post("/api/alibaba.1688.get.core.metrics/1.0.0", payload)

    # API 响应结构：api_post 返回 {"data": "{JSON字符串}", "success": ..., "msgInfo": ...}
    # 实际指标数据嵌套在 data["data"] 中，且为 JSON 字符串，需逐层解包
    if isinstance(data, dict) and 'data' in data:
        inner = data['data']
        if isinstance(inner, str):
            try:
                data = json.loads(inner)
            except json.JSONDecodeError:
                raise ServiceError("返回数据格式异常，无法解析内层 JSON")
        elif isinstance(inner, (dict, list)):
            data = inner
    elif isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise ServiceError("返回数据格式异常，无法解析")

    if not isinstance(data, dict):
        raise ServiceError("返回数据格式异常，期望字典")

    return data
