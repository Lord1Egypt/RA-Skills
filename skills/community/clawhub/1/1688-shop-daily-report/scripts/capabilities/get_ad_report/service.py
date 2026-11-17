#!/usr/bin/env python3
"""广告投放数据查询与汇总服务

调用 alibaba.1688.query.shop.data 接口（dataSource=AD, apiPath=/ad/customer）获取广告数据，
按日期汇总计算核心指标（消耗、曝光、点击、CTR、CPC、询盘、成交、ROI）。
"""

import json as _json
from _http import api_post
from _errors import ServiceError, ParamError

_QUERY_SHOP_DATA_API = "/api/alibaba.1688.query.shop.data/1.0.0"


def _safe_num(val, default=0):
    """安全转换数值，处理 None / 字符串 / 非数值类型"""
    if val is None:
        return default
    if isinstance(val, (int, float)):
        return val
    if isinstance(val, str):
        try:
            return float(val)
        except (ValueError, TypeError):
            return default
    return default


def _fetch_ad_raw(date_str: str, login_id: str = None) -> list:
    """获取指定日期的广告原始数据列表

    Args:
        date_str: 日期，格式 yyyyMMdd（如 20260629）
        login_id: 可选，目标店铺的 loginId

    Returns:
        广告计划数据列表（每条记录为一个计划的当天数据），保证返回 list
    """
    try:
        data = api_post(_QUERY_SHOP_DATA_API, {
            "dataSource": "AD",
            "apiPath": "/ad/customer",
            "params": {"startDate": date_str, "endDate": date_str},
        }, login_id=login_id)
    except Exception:
        return []

    if not data or not isinstance(data, dict):
        return []

    # data.data 是数组
    raw_list = data.get("data", [])
    if isinstance(raw_list, str):
        try:
            raw_list = _json.loads(raw_list)
        except (ValueError, TypeError):
            raw_list = []
    if not isinstance(raw_list, list):
        raw_list = []

    # 过滤非 dict 记录
    return [item for item in raw_list if isinstance(item, dict)]


def _aggregate_daily(records: list) -> dict:
    """将多个计划记录汇总为单日整体指标

    Returns:
        {
            "spend": float,        # 总消耗
            "exposure": int,       # 实曝光
            "clicks": int,         # 点击量
            "visitors": int,       # 广告访客(去重)
            "inquiries": int,      # 询盘数
            "deals": int,          # 成交数量
            "deal_amount": float,  # 成交金额
            "favorites": int,      # 收藏商品数
            "cart_adds": int,      # 加入购物车数
            "plan_count": int,     # 投放计划数
            "ctr": float,          # CTR (%)
            "cpc": float,          # CPC (元)
            "roi": float,          # ROI
        }
    """
    if not records:
        return {
            "spend": 0.0, "exposure": 0, "clicks": 0, "visitors": 0,
            "inquiries": 0, "deals": 0, "deal_amount": 0.0,
            "favorites": 0, "cart_adds": 0, "plan_count": 0,
            "ctr": 0, "cpc": 0, "roi": 0,
        }

    agg = {
        "spend": 0.0, "exposure": 0, "clicks": 0, "visitors": 0,
        "inquiries": 0, "deals": 0, "deal_amount": 0.0,
        "favorites": 0, "cart_adds": 0, "plan_count": 0,
    }

    for item in records:
        agg["spend"] += _safe_num(item.get("消耗金额/元"))
        agg["exposure"] += int(_safe_num(item.get("实曝光")))
        agg["clicks"] += int(_safe_num(item.get("点击量")))
        agg["visitors"] += int(_safe_num(item.get("广告访客数去重只有cpc")))
        agg["inquiries"] += int(_safe_num(item.get("询盘数量")))
        agg["deals"] += int(_safe_num(item.get("成交数量")))
        agg["deal_amount"] += _safe_num(item.get("成交金额"))
        agg["favorites"] += int(_safe_num(item.get("收藏商品数量")))
        agg["cart_adds"] += int(_safe_num(item.get("加入购物车数量")))
        agg["plan_count"] += 1

    # 累加金额截断精度，避免浮点溢出如 481.99999999999966
    agg["spend"] = round(agg["spend"], 2)
    agg["deal_amount"] = round(agg["deal_amount"], 2)

    # 计算派生指标
    agg["ctr"] = round((agg["clicks"] / agg["exposure"] * 100), 2) if agg["exposure"] > 0 else 0
    agg["cpc"] = round((agg["spend"] / agg["clicks"]), 2) if agg["clicks"] > 0 else 0
    agg["roi"] = round((agg["deal_amount"] / agg["spend"]), 2) if agg["spend"] > 0 else 0

    return agg


def _top_plans(records: list, top_n: int = 3) -> list:
    """提取消耗 Top N 计划的关键指标

    托管类解决方案会返回多条同名子计划记录（接口无计划 ID 字段），
    先按计划名称合并累加指标，再按消耗降序取 Top N。

    Returns:
        [{"name": str, "category": str, "spend": float, "clicks": int,
          "inquiries": int, "deals": int, "deal_amount": float, "roi": float}, ...]
    """
    if not records:
        return []

    # 按计划名称合并同名记录（累加指标，planLabel/category 取首条非空值）
    merged = {}
    for item in records:
        name = item.get("计划名称") or "未知计划"
        plan = merged.setdefault(name, {
            "name": name,
            "planLabel": "",
            "category": "",
            "spend": 0.0,
            "clicks": 0,
            "inquiries": 0,
            "deals": 0,
            "deal_amount": 0.0,
        })
        plan["planLabel"] = plan["planLabel"] or (item.get("plan_label") or "")
        plan["category"] = plan["category"] or (item.get("广告产品分类，按BP页面展示分类") or "")
        plan["spend"] += _safe_num(item.get("消耗金额/元"))
        plan["clicks"] += int(_safe_num(item.get("点击量")))
        plan["inquiries"] += int(_safe_num(item.get("询盘数量")))
        plan["deals"] += int(_safe_num(item.get("成交数量")))
        plan["deal_amount"] += _safe_num(item.get("成交金额"))

    # 过滤零消耗计划，按合并后消耗降序取 Top N
    sorted_plans = sorted(
        [p for p in merged.values() if p["spend"] > 0],
        key=lambda x: x["spend"], reverse=True,
    )

    plans = []
    for plan in sorted_plans[:top_n]:
        spend = round(plan["spend"], 2)
        deal_amount = round(plan["deal_amount"], 2)
        plans.append({
            "name": plan["name"],
            "planLabel": plan["planLabel"],
            "category": plan["category"],
            "spend": spend,
            "clicks": plan["clicks"],
            "inquiries": plan["inquiries"],
            "deals": plan["deals"],
            "deal_amount": deal_amount,
            "roi": round(deal_amount / spend, 2) if spend > 0 else 0,
        })
    return plans


def get_ad_report(query_date: str, prev_date: str, login_id: str = None) -> dict:
    """获取广告投放日报数据（当天 + 前一天 + 环比 + Top 计划）

    Args:
        query_date: 查询日期，格式 yyyyMMdd
        prev_date: 前一天日期，格式 yyyyMMdd
        login_id: 可选，目标店铺的 loginId

    Returns:
        {
            "query_date": str,
            "prev_date": str,
            "today": {汇总指标},
            "prevDay": {汇总指标},
            "changes": {各指标环比变化率(%)},
            "topPlans": [Top3计划详情],
        }
    """
    if not query_date:
        raise ParamError("query_date 不能为空")
    if not prev_date:
        raise ParamError("prev_date 不能为空")

    # 获取当天和前一天的原始数据
    today_records = _fetch_ad_raw(query_date, login_id=login_id)
    prev_records = _fetch_ad_raw(prev_date, login_id=login_id)

    # 两天数据都为空 → 该店铺无广告投放，返回明确标识
    if not today_records and not prev_records:
        return {
            "query_date": query_date,
            "prev_date": prev_date,
            "hasData": False,
            "message": "当天及前一天均无广告投放数据",
            "today": None,
            "prevDay": None,
            "changes": None,
            "topPlans": [],
        }

    # 汇总
    today_agg = _aggregate_daily(today_records)
    prev_agg = _aggregate_daily(prev_records)

    # 计算环比变化率（仅当前一天有数据时才有意义）
    changes = {}
    if prev_records:
        for key in ["spend", "exposure", "clicks", "visitors", "inquiries", "deals", "deal_amount"]:
            old_val = prev_agg[key]
            new_val = today_agg[key]
            if old_val > 0:
                changes[key] = round((new_val - old_val) / old_val * 100, 1)
            else:
                changes[key] = None  # 前一天为0，无法计算环比
    else:
        changes = None  # 前一天无数据，整体环比不可用

    # Top 计划（取当天数据）
    top_plans = _top_plans(today_records, top_n=3)

    return {
        "query_date": query_date,
        "prev_date": prev_date,
        "hasData": True,
        "today": today_agg,
        "prevDay": prev_agg if prev_records else None,
        "changes": changes,
        "topPlans": top_plans,
    }
