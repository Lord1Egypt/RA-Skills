#!/usr/bin/env python3
"""店铺核心指标同行对比及趋势数据查询服务"""

import json
from _http import api_post
from _errors import ServiceError

VALID_DATE_TYPES = {"RECENT_7", "RECENT_30"}

def get_core_metrics(date_type: str = "RECENT_7") -> dict:
    """获取店铺核心指标同行对比及趋势数据（商家身份由 AK 自动识别）

    Args:
        date_type:  日期类型 RECENT_7/RECENT_30

    Returns:
        API 响应 data 字段，包含 core_metrics（同行对比）和 trend（趋势数据）
    """
    if date_type not in VALID_DATE_TYPES:
        raise ValueError(f"date_type 必须为 {', '.join(sorted(VALID_DATE_TYPES))} 之一，当前值: {date_type}")

    data = api_post("/api/get_core_metrics/1.0.0", {
        "date_type": date_type,
    })

    # 返回的 data 是 JSON 字符串，需要解析
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise ServiceError("返回数据格式异常，无法解析")

    if not isinstance(data, dict):
        raise ServiceError("返回数据格式异常，期望字典")

    return data
