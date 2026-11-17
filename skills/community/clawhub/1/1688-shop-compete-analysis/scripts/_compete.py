#!/usr/bin/env python3
"""
竞争（compete）域共享工具

集中处理经网关调用 /ms/compete/* 的三个固有差异，避免各处重复实现：
1. dateType / device 必须为大写枚举，否则网关静默返 data:null
2. 最内层可能是 JSON 字符串（需二次解析）；call_tool 已剥信封，不再多剥
3. 返回 key 被网关汉化（会员ID / 商品ID / 流量指数 …），且商品标题正文里的
   英文串也会被误替换（UV400 → 访客数400）
"""

import json
from datetime import date, timedelta

from _http import call_tool
from _const import TOOL_QUERY_SHOP_DATA

# 网关汉化会把标题正文里的同名英文串一起替换，展示前需还原
_TEXT_FIX = (("访客数400", "UV400"), ("访客数", "UV"), ("浏览量", "PV"))

# 判定为「无数据」类错误的关键词（网关对竞争接口返空时的 msgInfo 实测取值）
_NO_DATA_KEYS = ("数据查询无结果", "无结果", "返回为空", "暂无数据")


def enrich_no_data_error(exc, scope: str = ""):
    """给竞争类接口的「无结果」错误补上商家可操作的下一步，其它错误原样返回。

    背景：竞争接口返空时网关只给一句 msgInfo「数据查询无结果」，命令原样透出后
    商家完全无从下手。实测同一家店铺 compete_category 与竞店监控清单能正常返回、
    而行业榜 shopList 返空，说明返空往往是**权限/类目**问题而非登录问题，
    这类可判别的下一步应当直接告诉商家。

    直接改写 exc.message（print_error 读的就是它），避免各 cmd.py 重复判断。

    Args:
        exc:   捕获到的异常
        scope: 出错的业务环节中文名（如「行业店铺排行」），用于提示定位
    """
    msg = str(getattr(exc, "message", exc) or "")
    if not any(k in msg for k in _NO_DATA_KEYS):
        return exc

    where = f"（{scope}）" if scope else ""
    hint = (
        f"\n\n{where}竞争分析暂时取不到数据，常见原因与下一步：\n"
        "1. 本店未开通竞争情报权限（行业排行 / 竞店下钻）——"
        "请到生意参谋「竞争」模块确认是否已订购，或联系服务商开通；\n"
        "2. 类目未授权或层级不匹配——重新执行 compete_category 获取本店类目树，"
        "并确认 cate_id 与 cate_level 属同一层级；\n"
        "3. 该时段确实无数据——改用近 30 天再试。\n"
        "参考：若 compete_category 与竞店监控清单能正常返回，说明登录与鉴权没有问题，"
        "多为上述第 1 或第 2 项。"
    )
    if hasattr(exc, "message"):
        exc.message = msg + hint
    return exc


def compete_query(api_path: str, params: dict):
    """调用一个 compete 接口，返回最内层数据（call_tool 已剥信封，此处不再多剥）。

    Args:
        api_path: 如 compete/competeShop/shopList
        params:   业务参数（dateType/device 需已是大写枚举）

    Returns:
        最内层数据（dict / list / None）。分页接口为 {data:[...], recordCount:N}，
        由调用方自行取 data / recordCount。
    """
    body = {"dataSource": "SYCM", "apiPath": api_path, "params": dict(params or {})}

    inner = call_tool(TOOL_QUERY_SHOP_DATA, body)
    if isinstance(inner, str):
        try:
            inner = json.loads(inner)
        except (json.JSONDecodeError, ValueError):
            pass
    return inner


def val(row: dict, key: str, sub: str = "value", default=None):
    """取 {value, cycleCrc} 包装字段；非包装结构则原样返回"""
    x = (row or {}).get(key)
    if isinstance(x, dict):
        return x.get(sub, default)
    return default if x is None else x


def fix_text(s):
    """还原网关汉化对文本正文（商品标题/关键词）的误替换"""
    if not isinstance(s, str):
        return s
    for zh, en in _TEXT_FIX:
        s = s.replace(zh, en)
    return s


def member_id_of(row: dict):
    """从行数据里取 memberId（兼容汉化 key 与 shop 子对象）"""
    if not isinstance(row, dict):
        return None
    for k in ("会员ID", "memberId"):
        v = row.get(k)
        if isinstance(v, dict):
            v = v.get("value")
        if v:
            return v
    shop = row.get("shop") or {}
    return shop.get("会员ID") or shop.get("memberId")


def offer_id_of(row: dict):
    """从行数据里取 offerId（兼容汉化 key 与 item 子对象）"""
    if not isinstance(row, dict):
        return None
    for k in ("商品ID", "offerId", "itemId"):
        v = row.get(k)
        if isinstance(v, dict):
            v = v.get("value")
        if v:
            return v
    item = row.get("item") or {}
    return item.get("商品ID") or item.get("offerId")


def recent_range(days: int, end_offset: int = 1) -> str:
    """生成 dateRange 字符串。

    Args:
        days:       窗口天数（7 / 30）
        end_offset: 结束日相对今天的偏移天数，默认 1（截至昨天，因当天数据未出）
    """
    end = date.today() - timedelta(days=end_offset)
    start = end - timedelta(days=days - 1)
    return f"{start.isoformat()}|{end.isoformat()}"


def single_day(days_ago: int = 1) -> str:
    """生成单日 dateRange（首尾同一天），默认昨天"""
    d = (date.today() - timedelta(days=days_ago)).isoformat()
    return f"{d}|{d}"


def date_range_for(date_type: str) -> str:
    """按 dateType 生成配套 dateRange"""
    dt = (date_type or "").upper()
    if dt == "RECENT_30":
        return recent_range(30)
    if dt == "RECENT_1":
        return single_day(1)
    return recent_range(7)
