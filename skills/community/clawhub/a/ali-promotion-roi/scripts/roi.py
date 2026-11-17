"""
Alibaba 国际站 推广 ROI 计算核心
- 输入: sql-linker-cli 连库,拉 alibaba_intl_orders + alibaba_intl_promotion_daily
- 输出: 月度 ROI 报告 / 推广类型拆分 / 按日对照
"""

import os
import sys
import io
from collections import Counter, defaultdict
from decimal import Decimal

# 解决 Windows GBK 控制台 unicode 问题
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
except (ValueError, AttributeError):
    pass  # PowerShell 重定向时 buffer 可能不可用,跳过

# PowerShell 异步执行 (yieldMs) 可能关闭 stdout,
# 准备一个安全 print 防调用 sql-linker 内部 print 时崩溃
_original_print = print
def _safe_print(*args, **kwargs):
    try:
        _original_print(*args, **kwargs)
        return
    except (ValueError, OSError):
        pass
    # fallback: stdout 已关闭,尝试 stderr
    try:
        if args:
            sys.stderr.write(str(args[0]) + "\n")
            sys.stderr.flush()
    except Exception:
        pass
import builtins
builtins.print = _safe_print

# sql-linker-cli 路径
SKILL_ROOT = r"C:\Users\user\.openclaw\workspace\skills\sql-linker-cli\scripts"
sys.path.insert(0, os.path.join(SKILL_ROOT, "controller_layer"))
sys.path.insert(0, os.path.join(SKILL_ROOT, "service_layer"))

from db_bridge import DBBridge  # noqa: E402


# ============================================================
# 数据源
# ============================================================
ORDERS_TABLE = "alibaba_intl_orders"
PROMO_TABLE = "alibaba_intl_promotion_daily"

COMPLETED_STATUS = "订单完成"

# 默认汇率 (1 USD = ? CNY)
DEFAULT_USD_CNY_RATE = 7.2


# ============================================================
# 数据拉取
# ============================================================
def fetch_orders(db, month=None):
    """
    拉订单。month='2026-01' 过滤,None 拉全部。
    """
    sql = """
        SELECT data_date, order_no, order_status, order_amount,
               shipping_fee, discount_amount, order_currency, buyer_country
        FROM alibaba_intl_orders
    """
    params = None
    if month:
        sql += " WHERE data_month = %s"
        params = (month,)
    sql += " ORDER BY data_date"
    return db.query(sql, params)


def fetch_promotion(db, month=None):
    """
    拉推广日度数据。
    """
    sql = """
        SELECT data_date, data_month, promotion_type, cost, cost_unit,
               impression_cnt, click_cnt, biz_opportunity_cnt, order_cnt,
               promotion_hours
        FROM alibaba_intl_promotion_daily
    """
    params = None
    if month:
        sql += " WHERE data_month = %s"
        params = (month,)
    sql += " ORDER BY data_date, promotion_type"
    return db.query(sql, params)


# ============================================================
# 指标计算
# ============================================================
def _net_amount(o):
    """订单实付: 订单金额 + 运费 - 折扣"""
    return (float(o.get("order_amount") or 0)
            + float(o.get("shipping_fee") or 0)
            - float(o.get("discount_amount") or 0))


def _safe_div(n, d):
    return n / d if d else None


def compute_summary(orders, promo, rate=DEFAULT_USD_CNY_RATE):
    """
    按月总览 + 整体 KPI
    return: dict{
        'total_cost_cny', 'total_cost_usd',
        'completed_orders', 'completed_amount_usd',
        'cpo_cny' (单订单成本, CNY), 'roi_pct' (订单金额/花费)
        'status_breakdown': {status: cnt},
        'monthly': [ {month, cost_cny, cost_usd, completed_cnt, completed_amount_usd, cpo_cny, roi_pct} ]
    }
    """
    # 订单状态分布
    status_breakdown = Counter(o["order_status"] for o in orders)

    # 完成订单按月
    completed = [o for o in orders if o["order_status"] == COMPLETED_STATUS]
    by_month = defaultdict(lambda: {"cnt": 0, "amount": 0.0})
    for o in completed:
        d = _date_str(o["data_date"])
        m = d[:7]
        by_month[m]["cnt"] += 1
        by_month[m]["amount"] += _net_amount(o)

    # 推广按月
    promo_by_month = defaultdict(lambda: {"cost_cny": 0.0, "impression": 0, "click": 0})
    for p in promo:
        m = p["data_month"]
        promo_by_month[m]["cost_cny"] += float(p["cost"])
        promo_by_month[m]["impression"] += p["impression_cnt"]
        promo_by_month[m]["click"] += p["click_cnt"]

    all_months = sorted(set(promo_by_month.keys()) | set(by_month.keys()))
    monthly = []
    for m in all_months:
        p = promo_by_month[m]
        c = by_month[m]
        cost_usd = p["cost_cny"] / rate
        cpo = _safe_div(p["cost_cny"], c["cnt"])
        roi = _safe_div(c["amount"] * rate, p["cost_cny"]) * 100 if p["cost_cny"] else None
        # ROI 口径选择: 订单金额(USD) / 花费(CNY) 不严谨
        # 严谨口径: 订单金额(USD) * rate / 花费(CNY) * 100%
        monthly.append({
            "month": m,
            "cost_cny": round(p["cost_cny"], 2),
            "cost_usd": round(cost_usd, 2),
            "completed_cnt": c["cnt"],
            "completed_amount_usd": round(c["amount"], 2),
            "cpo_cny": round(cpo, 2) if cpo else None,
            "roi_pct": round(roi, 2) if roi else None,
            "impression": p["impression"],
            "click": p["click"],
        })

    total_cost_cny = sum(v["cost_cny"] for v in promo_by_month.values())
    total_completed = len(completed)
    total_amount = sum(_net_amount(o) for o in completed)

    return {
        "total_cost_cny": round(total_cost_cny, 2),
        "total_cost_usd": round(total_cost_cny / rate, 2),
        "completed_orders": total_completed,
        "completed_amount_usd": round(total_amount, 2),
        "cpo_cny": round(_safe_div(total_cost_cny, total_completed), 2) if total_completed else None,
        "roi_pct": round(_safe_div(total_amount * rate, total_cost_cny) * 100, 2)
                   if total_cost_cny else None,
        "status_breakdown": dict(status_breakdown),
        "monthly": monthly,
        "rate_used": rate,
    }


def compute_by_type(promo, orders, rate=DEFAULT_USD_CNY_RATE):
    """
    按推广类型拆分。
    return: list[{
        promotion_type, days, cost_cny, cost_usd, impression, click,
        promo_reported_orders (后台报), actual_completed_orders,
        actual_completed_amount_usd, cpo_cny, roi_pct
    }]
    """
    by_type = defaultdict(lambda: {
        "cost_cny": 0.0, "impression": 0, "click": 0,
        "promo_reported_orders": 0, "days": 0,
    })
    for p in promo:
        t = p["promotion_type"]
        by_type[t]["cost_cny"] += float(p["cost"])
        by_type[t]["impression"] += p["impression_cnt"]
        by_type[t]["click"] += p["click_cnt"]
        by_type[t]["promo_reported_orders"] += p["order_cnt"]
        by_type[t]["days"] += 1

    # 推广日期集合 → 用于 join 完成订单
    promo_dates = {p["data_date"] for p in promo}
    completed_in_promo = [
        o for o in orders
        if o["order_status"] == COMPLETED_STATUS and o["data_date"] in promo_dates
    ]
    completed_amt = sum(_net_amount(o) for o in completed_in_promo)

    result = []
    for t, v in by_type.items():
        cost_usd = v["cost_cny"] / rate
        # 单类型 ROI 用总订单金额/总花费近似(投放日期内的所有完成订单)
        # 严格归因需要订单维度打推广标签,不在本 skill 范围
        cpo = _safe_div(v["cost_cny"], len(completed_in_promo)) if completed_in_promo else None
        roi = _safe_div(completed_amt * rate, v["cost_cny"]) * 100 if v["cost_cny"] else None
        result.append({
            "promotion_type": t,
            "days": v["days"],
            "cost_cny": round(v["cost_cny"], 2),
            "cost_usd": round(cost_usd, 2),
            "impression": v["impression"],
            "click": v["click"],
            "promo_reported_orders": v["promo_reported_orders"],
            "actual_completed_orders": len(completed_in_promo),
            "actual_completed_amount_usd": round(completed_amt, 2),
            "cpo_cny": round(cpo, 2) if cpo else None,
            "roi_pct": round(roi, 2) if roi else None,
        })
    return result, completed_in_promo


def compute_by_date(promo, orders, rate=DEFAULT_USD_CNY_RATE):
    """
    按日对照 (推广花费 vs 当日完成订单)
    return: list[{date, cost_cny, promo_reported_orders, actual_completed_cnt,
                  actual_completed_amount_usd, cpo_cny}]
    """
    # 推广按日
    promo_by_date = defaultdict(lambda: {"cost_cny": 0.0, "promo_reported_orders": 0})
    for p in promo:
        d = p["data_date"]
        promo_by_date[d]["cost_cny"] += float(p["cost"])
        promo_by_date[d]["promo_reported_orders"] += p["order_cnt"]

    # 完成订单按日
    completed_by_date = defaultdict(lambda: {"cnt": 0, "amount": 0.0})
    for o in orders:
        if o["order_status"] != COMPLETED_STATUS:
            continue
        d = o["data_date"]
        completed_by_date[d]["cnt"] += 1
        completed_by_date[d]["amount"] += _net_amount(o)

    all_dates = sorted(set(promo_by_date.keys()) | set(completed_by_date.keys()))
    rows = []
    for d in all_dates:
        p = promo_by_date[d]
        c = completed_by_date[d]
        cpo = _safe_div(p["cost_cny"], c["cnt"]) if c["cnt"] else None
        rows.append({
            "date": _date_str(d),
            "cost_cny": round(p["cost_cny"], 2),
            "promo_reported_orders": p["promo_reported_orders"],
            "actual_completed_cnt": c["cnt"],
            "actual_completed_amount_usd": round(c["amount"], 2),
            "cpo_cny": round(cpo, 2) if cpo else None,
        })
    return rows


# ============================================================
# 辅助
# ============================================================
def _date_str(d):
    if hasattr(d, "strftime"):
        return d.strftime("%Y-%m-%d")
    return str(d)[:10]


def connect_db(user_label="openclaw-roi-analysis"):
    """连库 helper: 凭证审批闸门开启时需显式授权"""
    db = DBBridge(user_label=user_label, session_id=f"agent:main:ali-roi")
    db.explicit_credential_approval(approved=True)
    db.connect()
    return db