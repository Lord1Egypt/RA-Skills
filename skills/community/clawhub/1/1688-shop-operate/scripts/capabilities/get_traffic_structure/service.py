#!/usr/bin/env python3
"""店铺流量结构数据查询服务"""

from _http import api_post
from _errors import ServiceError

VALID_DATE_TYPES = {"RECENT_1", "RECENT_7", "RECENT_30"}
VALID_DEVICES = {"ALL", "PC", "WIRELESS"}

def get_traffic_structure(date_type: str = "RECENT_7", device: str = "ALL") -> dict:
    """获取店铺流量结构数据

    Args:
        date_type: 日期类型 RECENT_1/RECENT_7/RECENT_30
        device:    设备类型 ALL/PC/WIRELESS

    Returns:
        API 响应 data 字段，包含 traffic 流量来源排行等
    """
    if date_type not in VALID_DATE_TYPES:
        raise ValueError(f"date_type 必须为 {', '.join(sorted(VALID_DATE_TYPES))} 之一，当前值: {date_type}")
    if device not in VALID_DEVICES:
        raise ValueError(f"device 必须为 {', '.join(sorted(VALID_DEVICES))} 之一，当前值: {device}")

    data = api_post("/api/get_traffic_structure/1.0.0", {
        "date_type": date_type,
        "device": device,
    })

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")

    return data
