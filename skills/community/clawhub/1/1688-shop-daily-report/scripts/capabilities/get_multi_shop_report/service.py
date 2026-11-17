#!/usr/bin/env python3
"""多店铺日报批量查询服务 — 内部并行获取所有店铺数据，返回扁平化结构"""

import json as _json
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from _http import api_post
from _errors import ServiceError, ParamError
from capabilities.get_bindlist.service import get_bindlist
from capabilities.get_ad_report.service import get_ad_report
from capabilities.get_review_data.service import get_review_data

_TRADE_API = "/api/alibaba.1688.skill.shop.daily.report.get.trade.data/1.0.0"
_TRAFFIC_API = "/api/alibaba.1688.skill.shop.daily.report.get.traffic.data/1.0.0"
_USER_API = "/api/alibaba.1688.skill.shop.daily.report.get.user.data/1.0.0"

# 并发取数偏发失败（限流 429 / 超时 / 服务端 5xx）时的重试间隔（秒）：失败后短暂等待再重试一次
_RETRY_ONCE_DELAY = 0.8


def _parse_api_data(api_result: dict) -> dict:
    """解析 API 返回中的 data 字段（JSON 字符串 → dict）"""
    raw = api_result.get("data", "[]")
    if isinstance(raw, str):
        try:
            parsed = _json.loads(raw)
            if isinstance(parsed, list) and len(parsed) > 0:
                return parsed[0]
        except (ValueError, IndexError):
            pass
    elif isinstance(raw, dict):
        return raw
    return {}


def _round2(val):
    """安全 round：仅对 float 截断到 2 位小数，None/int 原样返回"""
    if val is None:
        return None
    if isinstance(val, float):
        return round(val, 2)
    return val


def _flatten_day_data(trade_raw: dict, traffic_raw: dict, user_raw: dict) -> dict:
    """将交易/流量/用户三个 API 返回合并为单层扁平字典（数值精度截断为2位小数）"""
    t = _parse_api_data(trade_raw)
    f = _parse_api_data(traffic_raw)
    u = _parse_api_data(user_raw)

    return {
        # 交易指标
        "gmv": _round2(t.get("当日GMV（元）", 0)),
        "orderCount": t.get("当日支付子订单数", 0),
        "avgPrice": _round2(t.get("客单价", 0)),
        "payConversionRate": _round2(t.get("支付转化率（%）", 0)),
        "inquiryCount": t.get("当日询盘数", 0),
        "gmvDayOnDay": _round2(t.get("GMV日环比（%）")),
        "gmvWeekOnWeek": _round2(t.get("GMV周环比（%）")),
        "orderDayOnDay": _round2(t.get("订单量日环比（%）")),
        "orderWeekOnWeek": _round2(t.get("订单量周环比（%）")),
        "inquiryDayOnDay": _round2(t.get("询盘数日环比（%）")),
        # 流量指标
        "uv": f.get("uv", 0),
        "pv": f.get("pv", 0),
        "searchUv": f.get("搜索uv", 0),
        "bounceRate": _round2(f.get("跳出率（%）", 0)),
        "uvCtr": _round2(f.get("UVCTR", 0)),
        "searchExposure": f.get("搜索曝光", 0),
        "adExposure": f.get("广告曝光", 0),
        # 用户指标
        "newBuyerCount": u.get("全店支付新买家数", 0),
        "newBuyerAmount": _round2(u.get("全店支付新买家支付金额", 0)),
        "oldBuyerCount": u.get("全店支付老买家数", 0),
        "oldBuyerAmount": _round2(u.get("全店支付老买家支付金额", 0)),
    }


_API_MAP = {
    "trade": _TRADE_API,
    "traffic": _TRAFFIC_API,
    "user": _USER_API,
}


def _fetch_metric(api_path: str, query_date: str, login_id: str = None) -> dict:
    """单个指标接口调用（供并发线程池提交，最小并发粒度）。

    并发压力下偏发失败（限流 429 / 超时 / 服务端 5xx，_http 层不会重试这些）时，
    在此再自动重试一次；两次都失败则抛出，由上层标记为该店 error（不会被当成 0）。
    """
    try:
        return api_post(api_path, {"query_date": query_date}, login_id=login_id)
    except Exception:
        time.sleep(_RETRY_ONCE_DELAY)
        return api_post(api_path, {"query_date": query_date}, login_id=login_id)


def _calc_change(today_val, prev_val):
    """计算环比变化率(%)，前一天为 0 或 None 时返回 None"""
    if not prev_val:
        return None
    return round((today_val - prev_val) / prev_val * 100, 2)


def _patch_day_on_day(today_data: dict, prev_data: dict) -> None:
    """用原始数据自行计算日环比，覆盖 API 预计算字段（API 部分字段始终返回 0）

    流量类环比（uv/pv/searchUv）接口不提供，同样在此补算：这些环比是基础日报核心摘要与
    机会/风险判定的直接输入，在服务端算好可避免 Agent 端逐店手算带来的算错风险。

    注意：**不补算支付转化率环比**。转化率本身是百分比，「跌 1.41 个百分点」与
    「跌 17.3%」两种口径含义差 10 倍以上，极易被误读；SKILL.md 亦规定转化率仅展示当日值。
    需要判断转化率走势时，用精简输出中保留的前一天原始转化率直接比对。
    """
    patch_map = [
        # (环比字段, today原始字段, prevDay原始字段)
        ("orderDayOnDay", "orderCount", "orderCount"),
        ("inquiryDayOnDay", "inquiryCount", "inquiryCount"),
        ("uvDayOnDay", "uv", "uv"),
        ("pvDayOnDay", "pv", "pv"),
        ("searchUvDayOnDay", "searchUv", "searchUv"),
    ]
    for ratio_key, today_key, prev_key in patch_map:
        today_val = today_data.get(today_key, 0) or 0
        prev_val = prev_data.get(prev_key, 0) or 0
        today_data[ratio_key] = _calc_change(today_val, prev_val)


def _patch_week_on_week(today_data: dict, week_data: dict) -> None:
    """用上周同日原始数据自行计算周环比，覆盖 API 预计算字段

    必须自算的依据（已实测验证）：同一接口对同一家店返回
    「订单量日环比（%）」=0、「询盘数日环比（%）」=0，而真实日环比分别是 +20.72% / +46.55%，
    证明这组预计算字段恒为 0（未计算）；周环比同理（orderWeekOnWeek / 询盘数周环比 各店全为 0，
    而 GMV周环比 各店不同、明显是真值）。因此只能多查一天（上周同日）自己算。

    与日环比一致：**不算支付转化率周环比**（百分比的环比口径歧义），需要时用 weekAgo 原值比对。
    """
    patch_map = [
        # (环比字段, today原始字段, weekAgo原始字段)
        ("gmvWeekOnWeek", "gmv", "gmv"),
        ("orderWeekOnWeek", "orderCount", "orderCount"),
        ("inquiryWeekOnWeek", "inquiryCount", "inquiryCount"),
        ("uvWeekOnWeek", "uv", "uv"),
        ("pvWeekOnWeek", "pv", "pv"),
        ("searchUvWeekOnWeek", "searchUv", "searchUv"),
        ("avgPriceWeekOnWeek", "avgPrice", "avgPrice"),
    ]
    for ratio_key, today_key, week_key in patch_map:
        today_val = today_data.get(today_key, 0) or 0
        week_val = week_data.get(week_key, 0) or 0
        today_data[ratio_key] = _calc_change(today_val, week_val)


def _safe_ad_report(query_date: str, prev_date: str, login_id: str = None):
    """广告查询包装：日期转 yyyyMMdd，失败自动重试一次；两次都失败返回 None
    （广告为可选板块，None 时日报省略广告段，不影响主体）"""
    for attempt in range(2):
        try:
            return get_ad_report(query_date.replace("-", ""), prev_date.replace("-", ""), login_id=login_id)
        except Exception:
            if attempt == 0:
                time.sleep(_RETRY_ONCE_DELAY)
    return None


def _safe_review_data(query_date: str, login_id: str = None):
    """评价查询包装：与日报同一天，失败自动重试一次；两次都失败返回 None
    （评价为可选板块，None 时日报省略评价段，不影响主体）"""
    day = query_date.replace("-", "")
    for attempt in range(2):
        try:
            return get_review_data(day, day, login_id=login_id)
        except Exception:
            if attempt == 0:
                time.sleep(_RETRY_ONCE_DELAY)
    return None


def get_multi_shop_report(
    query_date: str,
    prev_date: str,
    login_id: str = None,
    week_date: str = None,
) -> dict:
    """批量并发查询店铺日报数据

    默认查询所有绑定店铺；传入 login_id 时仅查询该店铺（单店铺模式复用同一套
    取数/汇总/广告/评价管线）。所有独立请求（N 店 × 日期数 × 3 接口 + 广告 + 评价）
    拍平到单一线程池并发执行，将关键路径压缩到约 1 次往返。

    Args:
        query_date: 查询日期 YYYY-MM-DD
        prev_date: 前一天日期 YYYY-MM-DD（用于日环比）
        login_id: 可选，指定则仅查询该 loginId 对应店铺；广告/评价也按该店铺查询
        week_date: 可选，上周同日 YYYY-MM-DD。传入则额外查该日数据并自算周环比
            （接口的周环比预计算字段除 GMV 外恒为 0，不可用）；不传则不查，节省 1/3 调用量。

    Returns:
        {
            "query_date": str,
            "prev_date": str,
            "week_date": str 或 None,
            "shops": [
                {
                    "companyName": str,
                    "loginId": str,
                    "isOwner": bool,
                    "today": {"gmv": ..., "orderCount": ..., ...},
                    "prevDay": {"gmv": ..., "orderCount": ..., ...},
                    "weekAgo": {...} 或 None（仅传入 week_date 时）,
                    "error": None 或 str
                }
            ],
            "adReport": dict 或 None,
            "reviewData": dict 或 None
        }
    """
    if not query_date:
        raise ParamError("query_date 不能为空")
    if not prev_date:
        raise ParamError("prev_date 不能为空")

    # 获取绑定店铺列表
    bind_data = get_bindlist()
    bind_list = bind_data.get("data", [])
    if not bind_list:
        raise ServiceError("未查询到绑定的店铺列表，请确认账号已绑定店铺")

    # 单店铺过滤：指定 login_id 时仅保留该店铺
    if login_id:
        bind_list = [s for s in bind_list if s.get("loginId") == login_id]
        if not bind_list:
            raise ServiceError(f"未在绑定店铺中找到 loginId={login_id} 对应的店铺")

    # 拍平所有独立请求到单一线程池：N 店 × 日期数 × 3 接口 + 广告 + 评价 全部并发
    # 传入 week_date 时多查一天（上周同日）用于自算周环比；并发执行所以墙钟耗时增加有限
    date_pairs = [("today", query_date), ("prevDay", prev_date)]
    if week_date:
        date_pairs.append(("weekAgo", week_date))
    metric_futures = {}  # future -> (shop_index, date_key, metric_key)
    total_metric_calls = len(bind_list) * len(_API_MAP) * len(date_pairs)
    max_workers = min(total_metric_calls + 2, 16)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for idx, shop in enumerate(bind_list):
            shop_login_id = shop.get("loginId")
            for date_key, date_val in date_pairs:
                for metric_key, api_path in _API_MAP.items():
                    fut = executor.submit(_fetch_metric, api_path, date_val, shop_login_id)
                    metric_futures[fut] = (idx, date_key, metric_key)

        # 广告 + 评价与店铺数据并发；单店场景按该店查询，多店保持全局（不带 loginId）
        ad_future = executor.submit(_safe_ad_report, query_date, prev_date, login_id)
        review_future = executor.submit(_safe_review_data, query_date, login_id)

        # 收集各指标原始返回
        raw = defaultdict(dict)  # (shop_index, date_key) -> {metric_key: api_result}
        shop_errors = {}         # shop_index -> 首个错误信息
        for fut in as_completed(metric_futures):
            idx, date_key, metric_key = metric_futures[fut]
            try:
                raw[(idx, date_key)][metric_key] = fut.result()
            except Exception as exc:
                # 已在 _fetch_metric 内重试一次仍失败：记为该店错误，装配时 today/prevDay 置 None
                shop_errors.setdefault(idx, f"数据查询失败（已自动重试1次仍失败）：{exc}")

        ad_report = ad_future.result()
        review_data = review_future.result()

    # 按店铺装配结果（遍历 bind_list，保证每店恰好一条，无需额外兜底）
    results = []
    for idx, shop in enumerate(bind_list):
        shop_info = {
            "companyName": shop.get("companyName", "未知店铺"),
            "loginId": shop.get("loginId") or "",
            "isOwner": shop.get("isOwner", False),
        }
        if idx in shop_errors:
            results.append({**shop_info, "today": None, "prevDay": None, "weekAgo": None, "error": shop_errors[idx]})
            continue

        today_raw = raw.get((idx, "today"), {})
        prev_raw = raw.get((idx, "prevDay"), {})
        today_data = _flatten_day_data(
            today_raw.get("trade", {}), today_raw.get("traffic", {}), today_raw.get("user", {})
        )
        prev_data = _flatten_day_data(
            prev_raw.get("trade", {}), prev_raw.get("traffic", {}), prev_raw.get("user", {})
        )
        # 用真实原始数据补算日环比，覆盖 API 返回的 0 值
        _patch_day_on_day(today_data, prev_data)
        week_data = None
        if week_date:
            week_raw = raw.get((idx, "weekAgo"), {})
            week_data = _flatten_day_data(
                week_raw.get("trade", {}), week_raw.get("traffic", {}), week_raw.get("user", {})
            )
            # 同理覆盖周环比：接口除 GMV 外的周环比字段恒为 0，不可直接用
            _patch_week_on_week(today_data, week_data)
        results.append({**shop_info, "today": today_data, "prevDay": prev_data, "weekAgo": week_data, "error": None})

    return {
        "query_date": query_date,
        "prev_date": prev_date,
        "week_date": week_date,
        "shops": results,
        "adReport": ad_report,
        "reviewData": review_data,
    }
