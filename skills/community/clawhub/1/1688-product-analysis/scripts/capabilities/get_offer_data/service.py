#!/usr/bin/env python3
"""商品综合数据查询服务

通过 1688 Skills 网关调用 MCP 工具 `get_offer_data`，一次性返回商品的：
    profile / performance / huopan / search_issues / purchase_factors
    / sycm_anomaly / ad_analysis / hotwords / hot_items
"""

from typing import Iterable, Optional, Union

from _http import api_post
from _errors import ParamError, ServiceError

# 支持的 modules 取值（与上游 MCP 工具对齐）
ALLOWED_MODULES = {
    "profile",
    "performance",
    "huopan",
    "search_issues",
    "purchase_factors",
    "sycm_anomaly",
    "ad_analysis",
    "hotwords",
    "hot_items",
    "all",
}

# MCP 工具网关路径（code = get_offer_data，版本固定 1.0.0）
_API_PATH = "/api/get_offer_data/1.0.0"


def _normalize_modules(modules: Optional[Union[str, Iterable[str]]]) -> str:
    """规范化 modules 入参为逗号分隔字符串，并校验取值合法性。"""
    if modules is None or modules == "":
        return "all"

    if isinstance(modules, str):
        items = [m.strip() for m in modules.split(",") if m.strip()]
    else:
        items = [str(m).strip() for m in modules if str(m).strip()]

    if not items:
        return "all"

    invalid = [m for m in items if m not in ALLOWED_MODULES]
    if invalid:
        raise ParamError(
            f"modules 取值非法：{','.join(invalid)}；可选：{','.join(sorted(ALLOWED_MODULES))}"
        )

    # 去重保序
    seen = set()
    deduped = []
    for m in items:
        if m not in seen:
            seen.add(m)
            deduped.append(m)
    return ",".join(deduped)


def get_offer_data(offer_id: str, modules: Optional[Union[str, Iterable[str]]] = "all") -> dict:
    """获取商品综合数据。

    Args:
        offer_id: 1688 商品 ID（字符串）
        modules:  数据模块，可传字符串（逗号分隔）或可迭代对象。
                  默认 "all"，即拉取全部维度。

    Returns:
        网关返回的 data 字段（dict 结构，按模块组织）。
    """
    if not offer_id or not str(offer_id).strip():
        raise ParamError("offer_id 不能为空")

    payload = {
        "offer_id": str(offer_id).strip(),
        "modules": _normalize_modules(modules),
    }

    data = api_post(_API_PATH, payload, timeout=120)

    if data is None:
        raise ServiceError("商品数据为空，请确认 offer_id 是否归属当前账号")

    return data
