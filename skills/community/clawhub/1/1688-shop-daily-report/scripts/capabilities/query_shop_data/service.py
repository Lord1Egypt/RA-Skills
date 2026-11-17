#!/usr/bin/env python3
"""商家数据自由查询服务 — 从 1688-shop-freedom-query-data 移植"""

from _http import api_post
from _errors import ServiceError, ParamError

# SYCM dateType 合法枚举值及常见非标写法映射
_DATA_TYPE_MAPPING = {
    "RECENT_1": "RECENT_1",
    "RECENT_7": "RECENT_7",
    "RECENT_30": "RECENT_30",
    "WEEK": "WEEK",
    "MONTH": "MONTH",
    "DAY": "RECENT_1",
    "recent_1": "RECENT_1",
    "recent_7": "RECENT_7",
    "recent_30": "RECENT_30",
    "recent1": "RECENT_1",
    "recent7": "RECENT_7",
    "recent30": "RECENT_30",
    "recnt7": "RECENT_7",
    "recnt1": "RECENT_1",
    "recnt30": "RECENT_30",
    "week": "WEEK",
    "month": "MONTH",
    "day": "RECENT_1",
    "today": "RECENT_1",
}

# SYCM device 合法枚举值及常见非标写法映射
_DEVICE_MAPPING = {
    "ALL": "ALL",
    "PC": "PC",
    "WIRELESS": "WIRELESS",
    "all": "ALL",
    "pc": "PC",
    "wireless": "WIRELESS",
    "0": "ALL",
    "1": "PC",
    "2": "WIRELESS",
}

# periodsAgo 仅支持以下 dataType 回溯历史周期
_PERIODS_AGO_SUPPORTED = {"RECENT_1", "WEEK", "MONTH"}


def _normalize_sycm_params(params: dict) -> dict:
    """将 SYCM 接口的 dateType / device 标准化为大写枚举值，并校验 periodsAgo"""
    normalized = dict(params)

    if "dateType" in normalized:
        raw = str(normalized["dateType"]).strip()
        matched = _DATA_TYPE_MAPPING.get(raw)
        if matched is None:
            matched = _DATA_TYPE_MAPPING.get(raw.upper(), raw.upper())
        normalized["dateType"] = matched

    if "device" in normalized:
        raw = str(normalized["device"]).strip()
        matched = _DEVICE_MAPPING.get(raw)
        if matched is None:
            matched = _DEVICE_MAPPING.get(raw.upper(), raw.upper())
        normalized["device"] = matched

    # periodsAgo 校验：仅 RECENT_1 / WEEK / MONTH 支持
    if "periodsAgo" in normalized:
        periods_ago = normalized["periodsAgo"]
        if periods_ago is not None:
            try:
                periods_ago = int(periods_ago)
            except (ValueError, TypeError):
                raise ParamError(f"periodsAgo 必须为非负整数，收到: {normalized['periodsAgo']}")
            if periods_ago < 0:
                raise ParamError(f"periodsAgo 必须为非负整数，收到: {periods_ago}")

            date_type = normalized.get("dateType", "")
            if date_type not in _PERIODS_AGO_SUPPORTED:
                raise ParamError(
                    f"periodsAgo 仅支持 dataType 为 {', '.join(sorted(_PERIODS_AGO_SUPPORTED))}，"
                    f"当前 dataType={date_type}。建议改用自然周(WEEK)或自然月(MONTH)查询历史数据"
                )
            normalized["periodsAgo"] = periods_ago

    return normalized


def query_shop_data(data_source: str, api_path: str, params: dict, login_id: str = None) -> dict:
    """
    调用 alibaba.1688.query.shop.data，查询商家经营数据。
    userId 由网关根据 AK 签名自动注入，脚本无需传递。

    Args:
        data_source: 数据源标识（如 SYCM、AD、ITEM）
        api_path: 接口路径（如 portal/core/overview）
        params: 业务参数（如 {"dateType": "RECENT_7", "device": "ALL"}）
        login_id: 可选，目标店铺的 loginId，用于多店铺场景

    Returns:
        接口返回的数据 dict
    """
    if not data_source:
        raise ParamError("dataSource 不能为空")
    if not api_path:
        raise ParamError("apiPath 不能为空")

    # SYCM 接口参数标准化
    if data_source.upper() == "SYCM":
        params = _normalize_sycm_params(params or {})

    final_params = dict(params or {})
    if login_id:
        final_params["NEWTON_SHOP_LOGIN_ID"] = login_id

    data = api_post("/api/alibaba.1688.query.shop.data/1.0.0", {
        "dataSource": data_source,
        "apiPath": api_path,
        "params": final_params,
    })

    if not isinstance(data, dict):
        raise ServiceError("数据接口返回格式异常")

    return data
