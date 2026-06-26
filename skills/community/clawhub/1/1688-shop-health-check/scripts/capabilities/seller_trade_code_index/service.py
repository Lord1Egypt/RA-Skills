#!/usr/bin/env python3
"""店铺交易核心指标查询服务（总盘健康判断核心接口）"""

from _http import api_post
from _errors import ServiceError

VALID_DATE_TYPES = {"RECENT_7", "RECENT_30"}
VALID_DEVICES = {"ALL", "PC", "WIRELESS"}

def get_trade_code_index(date_type: str = "RECENT_7", device: str = "ALL") -> dict:
    """获取店铺交易核心指标（商家身份由 AK 自动识别）

    Args:
        date_type: 日期类型 RECENT_7/RECENT_30
        device:    设备类型 ALL/PC/WIRELESS

    Returns:
        API 响应 data 字段，包含 payAmt/payByrCnt/payRate 等核心指标
    """
    if date_type not in VALID_DATE_TYPES:
        raise ValueError(f"date_type 必须为 {', '.join(sorted(VALID_DATE_TYPES))} 之一，当前值: {date_type}")
    if device not in VALID_DEVICES:
        raise ValueError(f"device 必须为 {', '.join(sorted(VALID_DEVICES))} 之一，当前值: {device}")

    data = api_post("/api/seller_trade_code_index/1.0.0", {
        "dateType": date_type,
        "device": device,
    })

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")

    return data
