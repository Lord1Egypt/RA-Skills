#!/usr/bin/env python3
"""商品评价数据查询与解析服务

调用 alibaba.1688.query.shop.data 接口（dataSource=ITEM, apiPath=/item/rate）获取评价数据，
按 5 分制分类统计（5星好评、3-4星中评、1-2星差评），收集好差评原因。
"""

import json as _json
from _http import api_post
from _errors import ServiceError, ParamError

_QUERY_SHOP_DATA_API = "/api/alibaba.1688.query.shop.data/1.0.0"

# 评价分类阈值
_GOOD_SCORES = {5}         # 5星 = 好评
_NEUTRAL_SCORES = {3, 4}   # 3-4星 = 中评
_BAD_SCORES = {1, 2}       # 1-2星 = 差评


def _safe_int(val, default=0):
    """安全转换为整数"""
    if val is None:
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def _fetch_review_raw(start_date: str, end_date: str, login_id: str = None, limit: int = 100) -> list:
    """获取指定日期范围的评价原始数据

    Args:
        start_date: 起始日期，格式 yyyyMMdd
        end_date: 截止日期，格式 yyyyMMdd
        login_id: 可选，目标店铺的 loginId
        limit: 返回数量，默认100

    Returns:
        评价数据列表，保证返回 list
    """
    try:
        data = api_post(_QUERY_SHOP_DATA_API, {
            "dataSource": "ITEM",
            "apiPath": "/item/rate",
            "params": {"startDate": start_date, "endDate": end_date, "limit": limit},
        }, login_id=login_id)
    except Exception:
        return []

    if not data or not isinstance(data, dict):
        return []

    raw_list = data.get("data", [])
    if isinstance(raw_list, str):
        try:
            raw_list = _json.loads(raw_list)
        except (ValueError, TypeError):
            raw_list = []
    if not isinstance(raw_list, list):
        raw_list = []

    return [item for item in raw_list if isinstance(item, dict)]


def _classify_reviews(records: list) -> dict:
    """将评价按5分制分类，并收集好差评原因

    Returns:
        {
            "total": int,           # 总评价数
            "good": int,            # 好评数（5星）
            "neutral": int,         # 中评数（3-4星）
            "bad": int,             # 差评数（1-2星）
            "goodRate": float,      # 好评率（%）
            "badRate": float,       # 差评率（%）
            "goodReasons": list,    # 好评原因列表（去重，最多5条）
            "badReasons": list,     # 差评原因列表（去重，最多5条）
            "topProducts": list,    # 评价涉及的商品汇总
        }
    """
    if not records:
        return {
            "total": 0, "good": 0, "neutral": 0, "bad": 0,
            "goodRate": 0, "badRate": 0,
            "goodReasons": [], "badReasons": [], "topProducts": [],
        }

    good_count = 0
    neutral_count = 0
    bad_count = 0
    good_reasons = []
    bad_reasons = []
    product_stats = {}  # {商品ID: {"name": str, "good": int, "neutral": int, "bad": int}}

    for item in records:
        score = _safe_int(item.get("分数"))
        review_text = (item.get("评价") or "").strip()
        good_text = (item.get("好评") or "").strip()
        bad_text = (item.get("差评") or "").strip()
        product_id = item.get("商品ID")
        product_name = item.get("商品名称") or "未知商品"

        # 初始化商品统计
        if product_id and product_id not in product_stats:
            product_stats[product_id] = {
                "name": product_name, "good": 0, "neutral": 0, "bad": 0
            }

        # 分类计数
        if score in _GOOD_SCORES:
            good_count += 1
            if product_id:
                product_stats[product_id]["good"] += 1
            # 收集好评原因（优先用好评字段，否则用评价字段）
            reason = good_text or review_text
            if reason and "该用户觉得商品" not in reason:  # 过滤系统默认文案
                good_reasons.append(reason)
        elif score in _NEUTRAL_SCORES:
            neutral_count += 1
            if product_id:
                product_stats[product_id]["neutral"] += 1
            # 中评中如果有差评内容也收集
            if bad_text:
                bad_reasons.append(bad_text)
            elif review_text and "该用户觉得商品" not in review_text:
                bad_reasons.append(review_text)
        elif score in _BAD_SCORES:
            bad_count += 1
            if product_id:
                product_stats[product_id]["bad"] += 1
            # 收集差评原因
            reason = bad_text or review_text
            if reason and "该用户觉得商品" not in reason:
                bad_reasons.append(reason)

    total = good_count + neutral_count + bad_count

    # 去重并限制数量
    good_reasons = list(dict.fromkeys(good_reasons))[:5]
    bad_reasons = list(dict.fromkeys(bad_reasons))[:5]

    # 商品维度汇总（按评价总数排序，取Top5）
    top_products = []
    for pid, stats in sorted(product_stats.items(),
                             key=lambda x: x[1]["good"] + x[1]["neutral"] + x[1]["bad"],
                             reverse=True)[:5]:
        product_total = stats["good"] + stats["neutral"] + stats["bad"]
        top_products.append({
            "productId": pid,
            "name": stats["name"],
            "total": product_total,
            "good": stats["good"],
            "neutral": stats["neutral"],
            "bad": stats["bad"],
            "goodRate": round(stats["good"] / product_total * 100, 1) if product_total > 0 else 0,
        })

    return {
        "total": total,
        "good": good_count,
        "neutral": neutral_count,
        "bad": bad_count,
        "goodRate": round(good_count / total * 100, 1) if total > 0 else 0,
        "badRate": round(bad_count / total * 100, 1) if total > 0 else 0,
        "goodReasons": good_reasons,
        "badReasons": bad_reasons,
        "topProducts": top_products,
    }


def get_review_data(start_date: str, end_date: str, login_id: str = None) -> dict:
    """获取商品评价数据并分类汇总

    Args:
        start_date: 起始日期，格式 yyyyMMdd
        end_date: 截止日期，格式 yyyyMMdd
        login_id: 可选，目标店铺的 loginId

    Returns:
        {
            "startDate": str,
            "endDate": str,
            "hasData": bool,
            "summary": {分类统计},
        }
    """
    if not start_date or not end_date:
        raise ParamError("startDate 和 endDate 不能为空")

    records = _fetch_review_raw(start_date, end_date, login_id=login_id)

    if not records:
        return {
            "startDate": start_date,
            "endDate": end_date,
            "hasData": False,
            "message": "该时间段内无评价数据",
            "summary": None,
        }

    summary = _classify_reviews(records)

    return {
        "startDate": start_date,
        "endDate": end_date,
        "hasData": True,
        "summary": summary,
    }
