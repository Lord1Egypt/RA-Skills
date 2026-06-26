#!/usr/bin/env python3
"""异常商品识别查询服务（风险定位关键接口）"""

from _http import api_post
from _errors import ServiceError

VALID_DATE_TYPES = {"RECENT_7", "RECENT_30"}
VALID_DEVICES = {"ALL", "PC", "WIRELESS"}

def get_import_abnormal_offer(date_type: str = "RECENT_7", device: str = "ALL") -> dict:
    """获取需要商家重点关注的异常商品列表（商家身份由 AK 自动识别）

    Args:
        date_type: 日期类型 RECENT_7/RECENT_30
        device:    设备类型 ALL/PC/WIRELESS

    Returns:
        API 响应 data 字段，包含异常商品（含 reason / valueMap 变化率等）
    """
    if date_type not in VALID_DATE_TYPES:
        raise ValueError(f"date_type 必须为 {', '.join(sorted(VALID_DATE_TYPES))} 之一，当前值: {date_type}")
    if device not in VALID_DEVICES:
        raise ValueError(f"device 必须为 {', '.join(sorted(VALID_DEVICES))} 之一，当前值: {device}")

    data = api_post("/api/seller_import_abnormal_offer/1.0.0", {
        "dateType": date_type,
        "device": device,
    })

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")

    return data
