#!/usr/bin/env python3
"""单店铺全量经营数据采集服务

使用指定店铺的 AK 调用多个 API 接口，一次性获取该店铺的全量经营数据。
每个接口独立 try/except，失败则返回 None 并记录错误，不影响其他接口。
"""

import json
import logging
from datetime import datetime, timedelta

from _http import api_post_with_ak
from _errors import ServiceError

logger = logging.getLogger("get_shop_data")

VALID_DATE_TYPES = {"RECENT_7", "RECENT_30"}


def _safe_call(func, label: str):
    """安全调用接口，失败返回 None 并记录日志"""
    try:
        return func()
    except Exception as exc:
        logger.warning("接口 %s 调用失败: %s", label, exc)
        return None


def _parse_json_data(data):
    """解析可能是 JSON 字符串的 data"""
    if isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return data
    return data


def _fetch_trade_index(raw_ak: str, date_type: str) -> dict:
    """获取店铺交易核心指标（总盘）"""
    return api_post_with_ak("/api/seller_trade_code_index/1.0.0", raw_ak, {
        "dateType": date_type,
        "device": "ALL",
    })


def _fetch_core_metrics(raw_ak: str, date_type: str) -> dict:
    """获取店铺核心指标同行对比及趋势数据"""
    data = api_post_with_ak("/api/get_core_metrics/1.0.0", raw_ak, {
        "date_type": date_type,
    })
    return _parse_json_data(data)


def _fetch_traffic_trend(raw_ak: str, days: int = 7) -> list:
    """获取逐日流量趋势数据"""
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    data = api_post_with_ak("/api/get_traffic_trend/1.0.0", raw_ak, {
        "query_date": yesterday,
        "days": days,
    })
    return _parse_json_data(data)


def _fetch_abnormal_offer(raw_ak: str, date_type: str) -> dict:
    """获取异常商品列表"""
    return api_post_with_ak("/api/seller_import_abnormal_offer/1.0.0", raw_ak, {
        "dateType": date_type,
        "device": "ALL",
    })


def _fetch_top_offer(raw_ak: str, order_by: str, range_type: str) -> dict:
    """获取优秀商品榜单（单个榜单）"""
    index_code = "revealCnt,uv,payByrCnt,payRate,payAmt,payItemQty,payNewByrCnt,payOldByrCnt,itemMultiByrCnt,itemMultiByrPayAmt"
    return api_post_with_ak("/api/seller_top_offer/1.0.0", raw_ak, {
        "order": "desc",
        "orderBy": order_by,
        "device": "ALL",
        "rangeType": range_type,
        "indexCode": index_code,
        "page": "1",
        "pageSize": "10",
    })


def _fetch_activity_info(raw_ak: str) -> dict:
    """获取近 30 天活动参与及效果"""
    return api_post_with_ak("/api/seller_activity_registered_info/1.0.0", raw_ak, {})


def _fetch_province(raw_ak: str, date_type: str) -> dict:
    """获取客户地域分布"""
    return api_post_with_ak("/api/seller_customer_business_province/1.0.0", raw_ak, {
        "dateType": date_type,
        "page": "1",
        "pageSize": "50",
        "isTranslate": "true",
    })


def _fetch_customer_detail(raw_ak: str, date_type: str) -> dict:
    """获取头部老客户明细"""
    return api_post_with_ak("/api/seller_customer_detail/1.0.0", raw_ak, {
        "dateType": date_type,
        "buyerType": "头部老客户",
        "orderBy": "payAmount",
        "order": "desc",
        "page": "1",
        "pageSize": "20",
    })


def get_shop_data(raw_ak: str, date_type: str = "RECENT_7") -> dict:
    """获取单个店铺的全量经营数据（商家身份由传入的 AK 自动识别）

    Args:
        raw_ak:     该店铺的原始 AK
        date_type:  日期类型 RECENT_7/RECENT_30

    Returns:
        包含各维度数据的字典，每个 key 为数据维度名，value 为接口返回数据或 None（调用失败时）
    """
    if not raw_ak:
        raise ValueError("raw_ak 不能为空")
    if date_type not in VALID_DATE_TYPES:
        raise ValueError(f"date_type 必须为 {VALID_DATE_TYPES} 之一")

    result = {}

    # 1. 交易核心指标（总盘）
    result["trade_index"] = _safe_call(
        lambda: _fetch_trade_index(raw_ak, date_type),
        "trade_index"
    )

    # 2. 核心指标同行对比及趋势
    result["core_metrics"] = _safe_call(
        lambda: _fetch_core_metrics(raw_ak, date_type),
        "core_metrics"
    )

    # 3. 逐日流量趋势
    result["traffic_trend"] = _safe_call(
        lambda: _fetch_traffic_trend(raw_ak, days=7 if date_type == "RECENT_7" else 30),
        "traffic_trend"
    )

    # 4. 异常商品
    result["abnormal_offer"] = _safe_call(
        lambda: _fetch_abnormal_offer(raw_ak, date_type),
        "abnormal_offer"
    )

    # 5. 优秀商品榜单（按支付金额排序）
    result["top_offer_by_pay_amt"] = _safe_call(
        lambda: _fetch_top_offer(raw_ak, order_by="payAmt", range_type=date_type),
        "top_offer_by_pay_amt"
    )

    # 6. 优秀商品榜单（按访客数排序）
    result["top_offer_by_uv"] = _safe_call(
        lambda: _fetch_top_offer(raw_ak, order_by="uv", range_type=date_type),
        "top_offer_by_uv"
    )

    # 7. 优秀商品榜单（按拉新买家数排序）
    result["top_offer_by_new_buyer"] = _safe_call(
        lambda: _fetch_top_offer(raw_ak, order_by="payNewByrCnt", range_type=date_type),
        "top_offer_by_new_buyer"
    )

    # 8. 优秀商品榜单（按复购买家数排序）
    result["top_offer_by_repurchase"] = _safe_call(
        lambda: _fetch_top_offer(raw_ak, order_by="itemMultiByrCnt", range_type=date_type),
        "top_offer_by_repurchase"
    )

    # 9. 活动信息
    result["activity_info"] = _safe_call(
        lambda: _fetch_activity_info(raw_ak),
        "activity_info"
    )

    # 10. 客户地域分布
    result["province"] = _safe_call(
        lambda: _fetch_province(raw_ak, date_type),
        "province"
    )

    # 11. 头部老客户明细
    result["customer_detail"] = _safe_call(
        lambda: _fetch_customer_detail(raw_ak, date_type),
        "customer_detail"
    )

    return result
