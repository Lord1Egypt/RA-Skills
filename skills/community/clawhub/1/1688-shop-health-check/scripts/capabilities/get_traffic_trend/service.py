#!/usr/bin/env python3
"""逐日流量趋势数据查询服务"""

import json
from _http import api_post
from _errors import ServiceError

VALID_DAYS = {7, 30}

def get_traffic_trend(query_date: str, days: int = 7) -> list:
    """获取逐日流量趋势数据（商家身份由 AK 自动识别）

    Args:
        query_date:  查询日期（昨日日期，格式：YYYY-MM-DD）
        days:        天数，7 或 30（默认 7）

    Returns:
        逐日流量数据列表，每项包含 uv/pv/UVCTR/日期
    """
    if not query_date:
        raise ValueError("query_date 不能为空")
    if days not in VALID_DAYS:
        raise ValueError(f"days 必须为 {', '.join(map(str, sorted(VALID_DAYS)))} 之一，当前值: {days}")

    data = api_post("/api/get_traffic_trend/1.0.0", {
        "query_date": query_date,
        "days": days,
    })

    # 返回的 data 是 dict，内层还有一个 "data" 字段才是实际的 JSON 字符串
    # 结构: {"data": "[{...}]", "success": true, "msgInfo": "执行成功"}
    if isinstance(data, dict):
        data = data.get("data", data)

    # 内层 data 是 JSON 字符串，需要解析
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise ServiceError("返回数据格式异常，无法解析")

    if not isinstance(data, list):
        raise ServiceError("返回数据格式异常，期望列表")

    return data
