#!/usr/bin/env python3
"""商家数据查询服务"""

import json

from _http import call_tool
from _const import TOOL_QUERY_SHOP_DATA
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


# periodsAgo 仅支持以下 dateType 回溯历史周期
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
                    f"periodsAgo 仅支持 dateType 为 {', '.join(sorted(_PERIODS_AGO_SUPPORTED))}，"
                    f"当前 dateType={date_type}。建议改用自然周(WEEK)或自然月(MONTH)查询历史数据"
                )
            normalized["periodsAgo"] = periods_ago

    return normalized


def query_shop_data(data_source: str, api_path: str, params: dict):
    """
    调用 1688_query_shop_data，查询商家经营数据。
    userId 由本地网关登录态自动注入，脚本无需传递。

    Args:
        data_source: 数据源标识（如 SYCM、ITEM）
        api_path: 接口路径（如 portal/core/overview）
        params: 业务参数（如 {"dateType": "RECENT_7", "device": "ALL"}）

    Returns:
        接口返回的最内层数据（dict 或 list，视接口而定；call_tool 已剥信封）
    """
    if not data_source:
        raise ParamError("dataSource 不能为空")
    if not api_path:
        raise ParamError("apiPath 不能为空")

    # SYCM 接口参数标准化
    if data_source.upper() == "SYCM":
        params = _normalize_sycm_params(params or {})

    final_params = dict(params or {})

    data = call_tool(TOOL_QUERY_SHOP_DATA, {
        "dataSource": data_source,
        "apiPath": api_path,
        "params": final_params,
    })

    # call_tool 已剥信封并返回最内层数据；不同接口形状不一（dict / list），
    # 仅当为字符串时二次解析，其余原样返回，交由各命令按自身形状消费
    if data is None:
        raise ServiceError("数据接口返回为空")
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except (ValueError, TypeError):
            raise ServiceError("数据接口返回内容无法解析")

    return data
