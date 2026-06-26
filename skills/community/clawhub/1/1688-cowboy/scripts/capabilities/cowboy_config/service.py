# -*- coding: utf-8 -*-
"""牛仔配置服务

提供 5 个网关接口调用：
- create_cowboy:        创建牛仔（初始化卖家 AI 客服）
- update_cowboy:        更新牛仔配置
- pause_cowboy:         暂停牛仔接待
- resume_cowboy:        恢复牛仔接待
- load_cowboy_config:   加载牛仔配置（查询状态 + 允许接待的买家等级）

sellerUserId 由网关从上下文自动注入，无需显式传入。
网关双层 Result 包装：外层 {success, data} + 内层业务数据。
"""

from typing import Any, Dict, Iterable, List, Optional

from _errors import ServiceError
from _http import api_post
from settings import settings


_VALID_LEVELS = {"L0", "L1", "L2", "L3", "L4", "L5", "L6"}


def _normalize_levels(levels: Iterable[str]) -> List[str]:
    """清洗 + 验证 L 等级列表：去重、保留输入顺序、拒绝非法值 / 空列表。"""
    if levels is None:
        raise ServiceError("必须传入 allow_buyer_level_list，至少勾 1 项")
    seen = set()
    cleaned: List[str] = []
    for raw in levels:
        if raw is None:
            continue
        item = str(raw).strip().upper()
        if not item:
            continue
        if item not in _VALID_LEVELS:
            raise ServiceError("非法买家等级：{}（合法值：L0-L6）".format(item))
        if item in seen:
            continue
        seen.add(item)
        cleaned.append(item)
    if not cleaned:
        raise ServiceError("allow_buyer_level_list 不能为空，至少勾 1 项")
    return cleaned


def _call_cowboy_api(
    path: str,
    action_desc: str,
    body: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    通用牛仔配置 API 调用

    Args:
        path: settings 中定义的 API 路径
        action_desc: 操作描述（用于错误提示和 markdown 输出）
        body: 可选请求体；create / update 会传 allowBuyerLevelList，pause / resume 留空

    Returns:
        {"markdown": str, "data": dict}

    Note:
        sellerUserId 由网关自动从上下文注入，无需显式传入。
    """
    resp = api_post(
        path=path,
        body=body or {},
        timeout=settings.API_TIMEOUT,
    )

    # 网关双层 Result 包装处理
    inner = resp.get("data")
    if isinstance(inner, dict):
        biz_success = inner.get("success", resp.get("success"))
        biz_err = (inner.get("errorMsg") or inner.get("message")
                   or resp.get("errorMsg") or resp.get("message"))
    else:
        biz_success = resp.get("success")
        biz_err = resp.get("errorMsg") or resp.get("message")

    if not biz_success:
        raise ServiceError("{}失败：{}".format(action_desc, biz_err or resp))

    markdown = "✅ {}成功".format(action_desc)

    return {
        "markdown": markdown,
        "data": {"success": True},
    }


def create_cowboy(allow_buyer_level_list: Iterable[str]) -> Dict[str, Any]:
    """创建牛仔（初始化卖家 AI 客服）

    Args:
        allow_buyer_level_list: 允许接待的买家等级列表，如 ["L0", "L1", "L2"]；
            接口要求逗号分隔字符串，service 层负责 join。
    """
    levels = _normalize_levels(allow_buyer_level_list)
    return _call_cowboy_api(
        path=settings.CREATE_COWBOY_PATH,
        action_desc="创建牛仔",
        body={"allowBuyerLevelList": ",".join(levels)},
    )


def update_cowboy(allow_buyer_level_list: Iterable[str]) -> Dict[str, Any]:
    """更新牛仔配置中的买家等级列表（仅更新 allowBuyerLevelList）。

    Args:
        allow_buyer_level_list: 允许接待的买家等级列表；不会影响 enable / pause 状态。
    """
    levels = _normalize_levels(allow_buyer_level_list)
    return _call_cowboy_api(
        path=settings.UPDATE_COWBOY_PATH,
        action_desc="更新牛仔配置",
        body={"allowBuyerLevelList": ",".join(levels)},
    )


def pause_cowboy() -> Dict[str, Any]:
    """暂停牛仔接待"""
    return _call_cowboy_api(
        path=settings.PAUSE_COWBOY_PATH,
        action_desc="暂停牛仔接待",
    )


def resume_cowboy() -> Dict[str, Any]:
    """恢复牛仔接待"""
    return _call_cowboy_api(
        path=settings.RESUME_COWBOY_PATH,
        action_desc="恢复牛仔接待",
    )


# 状态码 -> 中文描述
_STATUS_MAP = {
    "not_hired": "未招聘",
    "active": "正常运行",
    "paused": "已暂停",
}


def load_cowboy_config() -> Dict[str, Any]:
    """
    加载牛仔配置

    返回：
        {
            "markdown": str,
            "data": {
                "status": str,                # not_hired | active | paused
                "allow_buyer_level_list": list[str],  # 例：["L1", "L2"]
            }
        }

    Note:
        sellerUserId 由网关自动从上下文注入，无需显式传入；外部也不需要返回。
    """
    resp = api_post(
        path=settings.LOAD_COWBOY_PATH,
        body={},
        timeout=settings.API_TIMEOUT,
    )

    # 这个接口可能出现两种响应结构，需动态识别：
    # 1) 双层包装：resp.data = AiSellerCcResult，inner.data = CowboyConfigDTO
    # 2) 单层包装：resp.data 就是 CowboyConfigDTO（含 sellerUserId/status 字段）
    inner = resp.get("data")

    biz_success = resp.get("success")
    biz_err = resp.get("errorMsg") or resp.get("message")
    biz_data = None

    if isinstance(inner, dict):
        # 启发式判断：如果存在 success / errorMsg / errorCode 且同时没有 status、sellerUserId
        # 字段，认为是内层 Result；否则认为 inner 已经是 DTO 本体。
        looks_like_inner_result = (
            ("success" in inner or "errorMsg" in inner or "errorCode" in inner)
            and "status" not in inner
            and "sellerUserId" not in inner
        )
        if looks_like_inner_result:
            biz_success = inner.get("success", biz_success)
            biz_err = (inner.get("errorMsg") or inner.get("message") or biz_err)
            biz_data = inner.get("data")
        else:
            biz_data = inner

    if not biz_success:
        raise ServiceError("加载牛仔配置失败：{}".format(biz_err or resp))

    # 允许 biz_data 为 None：卖家还未招聘牛仔时，服务端可能返回空 data
    if biz_data is None:
        biz_data = {}
    elif not isinstance(biz_data, dict):
        raise ServiceError(
            "加载牛仔配置失败：返回数据格式异常 resp={}".format(resp)
        )

    # sellerUserId 不读也不透出：由网关从上下文注入，上层不需要。
    status = biz_data.get("status") or "not_hired"
    allow_buyer_level_list = biz_data.get("allowBuyerLevelList") or []

    status_zh = _STATUS_MAP.get(status, status)
    levels_str = ", ".join(allow_buyer_level_list) if allow_buyer_level_list else "未配置"

    markdown = (
        "**牛仔配置**\n\n"
        "- 状态：{}\n"
        "- 接待买家等级：{}"
    ).format(status_zh, levels_str)

    return {
        "markdown": markdown,
        "data": {
            "status": status,
            "allow_buyer_level_list": allow_buyer_level_list,
        },
    }
