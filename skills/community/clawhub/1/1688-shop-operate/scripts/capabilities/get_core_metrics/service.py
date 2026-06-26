#!/usr/bin/env python3
"""店铺核心指标同行对比及趋势数据查询服务"""

from _http import api_post
from _errors import ServiceError

VALID_DATE_TYPES = {"RECENT_1", "RECENT_7", "RECENT_30"}
VALID_DEVICES = {"ALL", "PC", "WIRELESS"}

def get_core_metrics(date_type: str = "RECENT_7", device: str = "ALL") -> dict:
    """获取店铺核心指标同行对比及趋势数据

    Args:
        date_type: 日期类型 RECENT_1/RECENT_7/RECENT_30
        device:    设备类型 ALL/PC/WIRELESS

    Returns:
        API 响应 data 字段，包含 core_metrics 和 trend
    """
    if date_type not in VALID_DATE_TYPES:
        raise ValueError(f"date_type 必须为 {', '.join(sorted(VALID_DATE_TYPES))} 之一，当前值: {date_type}")
    if device not in VALID_DEVICES:
        raise ValueError(f"device 必须为 {', '.join(sorted(VALID_DEVICES))} 之一，当前值: {device}")

    data = api_post("/api/get_core_metrics/1.0.0", {
        "date_type": date_type,
        "device": device,
    })

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")

    return data
