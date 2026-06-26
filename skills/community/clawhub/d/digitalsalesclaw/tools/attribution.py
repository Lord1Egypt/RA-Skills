#!/usr/bin/env python3
"""
DigitalSalesClaw - attribution.py
多触点归因分析引擎
支持6种归因模型：first_touch / last_touch / linear / time_decay / position_based / data_driven

输入: {"action": "attribute|models|channel_summary|funnel", "patient_id": "...", "conversion_id": "...", "model": "last_touch"}
输出: {"attribution, touchpoints, channel_weights, ...}
"""

import sys
import json
import math
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent


# ─────────────────────────────────────────
# 归因模型
# ─────────────────────────────────────────
class AttributionModel:
    FIRST_TOUCH = "first_touch"
    LAST_TOUCH = "last_touch"
    LINEAR = "linear"
    TIME_DECAY = "time_decay"
    POSITION_BASED = "position_based"
    DATA_DRIVEN = "data_driven"


SUPPORTED_MODELS = [
    AttributionModel.FIRST_TOUCH,
    AttributionModel.LAST_TOUCH,
    AttributionModel.LINEAR,
    AttributionModel.TIME_DECAY,
    AttributionModel.POSITION_BASED,
    AttributionModel.DATA_DRIVEN,
]


# ─────────────────────────────────────────
# CAC/LTV 计算
# ─────────────────────────────────────────

def calculate_cac(period_days: int = 30, channel: str = None) -> dict:
    """
    计算客户获取成本 (Customer Acquisition Cost)
    CAC = 总营销成本 / 新增客户数
    """
    conn = get_conn()
    
    try:
        # 获取周期内营销支出
        spend_sql = """
            SELECT SUM(spend) as total_spend
            FROM content_metrics
            WHERE date >= datetime('now', ?)
        """
        params = [f"-{period_days} days"]
        if channel:
            spend_sql += " AND channel = ?"
            params.append(channel)

        spend_row = conn.execute(spend_sql, params).fetchone()
        total_spend = spend_row[0] or 0 if spend_row else 0

        # 获取周期内新增转化（去重患者数）
        conv_sql = """
            SELECT COUNT(DISTINCT patient_id) as new_patients
            FROM conversion_events
            WHERE timestamp >= datetime('now', ?)
        """
        conv_params = [f"-{period_days} days"]
        if channel:
            conv_sql += " AND attributed_channel = ?"
            conv_params.append(channel)

        conv_row = conn.execute(conv_sql, conv_params).fetchone()
        new_patients = conv_row[0] or 0 if conv_row else 0

        cac = total_spend / new_patients if new_patients > 0 else 0

        return {
            "period_days": period_days,
            "channel": channel or "all",
            "total_spend": round(total_spend, 2),
            "new_patients": new_patients,
            "cac": round(cac, 2),
            "cac_currency": "CNY",
        }
    finally:
        close_conn(conn)


def calculate_ltv(period_days: int = 90, conn=None) -> dict:
    """
    计算客户生命周期价值 (Lifetime Value)
    LTV = 平均转化价值 × 平均生命周期转化次数
    """
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        # 获取所有转化事件
        rows = conn.execute("""
            SELECT patient_id, conversion_type, value, timestamp
            FROM conversion_events
            WHERE timestamp >= datetime('now', ?)
            ORDER BY patient_id, timestamp
        """, (f"-{period_days} days",)).fetchall()

        cols = [d[0] for d in conn.execute("SELECT * FROM conversion_events LIMIT 0").description]
        conversions = [dict(zip(cols, r)) for r in rows]

        if not conversions:
            return {"period_days": period_days, "error": "No conversion data"}

        # 按患者分组
        patient_values = {}
        for conv in conversions:
            pid = conv["patient_id"]
            patient_values[pid] = patient_values.get(pid, 0) + (conv.get("value") or 0)

        values = list(patient_values.values())
        avg_order_value = sum(values) / len(values) if values else 0
        total_patients = len(patient_values)

        # 计算平均购买频次
        total_conversions = len(conversions)
        avg_frequency = total_conversions / total_patients if total_patients > 0 else 0

        # LTV 估算（简化模型：按周期折算）
        # 假设用户生命周期为 1 年
        days_per_year = 365
        ltv = avg_order_value * avg_frequency * (days_per_year / period_days)

        return {
            "period_days": period_days,
            "total_patients": total_patients,
            "total_conversions": total_conversions,
            "avg_order_value": round(avg_order_value, 2),
            "avg_frequency": round(avg_frequency, 2),
            "ltv": round(ltv, 2),
            "ltv_currency": "CNY",
            "roi_estimate": "high" if ltv > 500 else "medium" if ltv > 200 else "low",
        }
    finally:
        if own_conn:
            conn.close()


def cac_ltv_analysis(period_days: int = 30) -> dict:
    """
    综合 CAC/LTV 归因分析
    返回 CAC、LTV、以及 CAC/LTV 比值（应 < 1/3 才算健康）
    """
    cac_data = calculate_cac(period_days)
    ltv_data = calculate_ltv(period_days * 3)  # LTV 用更长周期

    cac = cac_data.get("cac", 0)
    ltv = ltv_data.get("ltv", 0)

    ratio = ltv / cac if cac > 0 else None

    # 健康度评估
    if ratio is None:
        health = "unknown"
        health_tip = "数据不足，无法评估"
    elif ratio >= 3:
        health = "healthy"
        health_tip = "CAC/LTV 比率健康，获客效率良好"
    elif ratio >= 1:
        health = "warning"
        health_tip = "CAC/LTV 比率偏低，需优化获客成本或提升客户价值"
    else:
        health = "critical"
        health_tip = "CAC/LTV 比率危险，当前获客模式不可持续"

    return {
        "period_days": period_days,
        "cac": cac,
        "ltv": ltv,
        "cac_ltv_ratio": round(ratio, 2) if ratio else None,
        "health": health,
        "health_tip": health_tip,
        "cac_detail": cac_data,
        "ltv_detail": ltv_data,
    }



def calculate_first_touch_weights(touchpoints: list[dict]) -> list[float]:
    """首次触点归因：100%归因给第一个触点"""
    if not touchpoints:
        return []
    return [1.0] + [0.0] * (len(touchpoints) - 1)


def calculate_last_touch_weights(touchpoints: list[dict]) -> list[float]:
    """末次触点归因：100%归因给最后一个触点"""
    if not touchpoints:
        return []
    return [0.0] * (len(touchpoints) - 1) + [1.0]


def calculate_linear_weights(touchpoints: list[dict]) -> list[float]:
    """线性归因：平均分配权重"""
    if not touchpoints:
        return []
    w = 1.0 / len(touchpoints)
    return [w] * len(touchpoints)


def calculate_time_decay_weights(touchpoints: list[dict], half_life: float = 7.0) -> list[float]:
    """时间衰减归因：越接近转化的触点权重越高，半衰期默认7天"""
    if not touchpoints:
        return []
    if len(touchpoints) == 1:
        return [1.0]

    # 按时间排序（从早到晚）
    sorted_tp = sorted(touchpoints, key=lambda x: x.get("timestamp", ""))
    first_ts = _parse_timestamp(sorted_tp[0].get("timestamp", ""))
    last_ts = _parse_timestamp(sorted_tp[-1].get("timestamp", ""))

    if not first_ts or not last_ts:
        return [1.0 / len(touchpoints)] * len(touchpoints)

    total_days = max((last_ts - first_ts).days, 1)

    weights = []
    for tp in sorted_tp:
        ts = _parse_timestamp(tp.get("timestamp", ""))
        if ts:
            days_from_first = (ts - first_ts).days
            decay = math.pow(0.5, days_from_first / half_life)
            weights.append(decay)
        else:
            weights.append(0.0)

    total = sum(weights)
    return [w / total for w in weights] if total > 0 else [1.0 / len(weights)] * len(weights)


def calculate_position_based_weights(touchpoints: list[dict],
                                     first_weight: float = 0.4,
                                     last_weight: float = 0.4) -> list[float]:
    """位置归因：首尾各40%，中间平均分配20%"""
    n = len(touchpoints)
    if n == 0:
        return []
    if n == 1:
        return [1.0]
    if n == 2:
        return [first_weight, last_weight]

    middle_count = n - 2
    middle_weight = (1.0 - first_weight - last_weight) / middle_count

    weights = [first_weight]
    for _ in range(middle_count):
        weights.append(middle_weight)
    weights.append(last_weight)
    return weights


def calculate_data_driven_weights(touchpoints: list[dict]) -> list[float]:
    """数据驱动归因（简化版：基于触点类型重要性权重）"""
    if not touchpoints:
        return []

    # 触点类型重要性权重（可配置）
    type_weights = {
        "content_view": 0.15,
        "kol_recommendation": 0.25,
        "search": 0.1,
        "social_share": 0.1,
        "ad_click": 0.15,
        "email": 0.05,
        "sms": 0.05,
        "pharmacy_visit": 0.15,
    }

    raw_weights = []
    for tp in touchpoints:
        touch_type = tp.get("touchpoint_type", "content_view")
        w = type_weights.get(touch_type, 0.1)
        # 位置加成：越接近转化越重要
        position = tp.get("position", 0)
        recency_bonus = 1.0 + (position / max(len(touchpoints), 1)) * 0.3
        raw_weights.append(w * recency_bonus)

    total = sum(raw_weights)
    return [w / total for w in raw_weights] if total > 0 else [1.0 / len(touchpoints)] * len(touchpoints)


def _parse_timestamp(ts_str: str) -> datetime:
    """解析时间戳字符串"""
    if not ts_str:
        return None
    for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%f"]:
        try:
            return datetime.strptime(ts_str[:19], fmt)
        except ValueError:
            pass
    return None


def get_attribution_weights(touchpoints: list[dict], model: str) -> list[float]:
    """根据模型计算归因权重"""
    if model == AttributionModel.FIRST_TOUCH:
        return calculate_first_touch_weights(touchpoints)
    elif model == AttributionModel.LAST_TOUCH:
        return calculate_last_touch_weights(touchpoints)
    elif model == AttributionModel.LINEAR:
        return calculate_linear_weights(touchpoints)
    elif model == AttributionModel.TIME_DECAY:
        return calculate_time_decay_weights(touchpoints)
    elif model == AttributionModel.POSITION_BASED:
        return calculate_position_based_weights(touchpoints)
    elif model == AttributionModel.DATA_DRIVEN:
        return calculate_data_driven_weights(touchpoints)
    else:
        return calculate_last_touch_weights(touchpoints)


def attribute_conversion(conversion_id: str = None, patient_id: str = None, model: str = "last_touch", conn=None) -> dict:
    """单次转化归因分析（基于统一患者旅程事件模型）"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        # 检查是否使用新统一模型
        new_model = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='patient_journey_events'"
        ).fetchone() is not None

        if new_model:
            return _attribute_conversion_unified(conversion_id, patient_id, model, conn)
        else:
            return _attribute_conversion_legacy(conversion_id, patient_id, model, conn)
    finally:
        if own_conn:
            conn.close()


def _attribute_conversion_unified(conversion_id: str = None, patient_id: str = None, model: str = "last_touch", conn=None) -> dict:
    """基于 patient_journey_events 统一模型的归因分析"""
    # 获取该患者所有旅程事件（按时间顺序）
    sql = """
        SELECT * FROM patient_journey_events
        WHERE patient_id = ? AND event_type = 'touchpoint'
        ORDER BY timestamp ASC
    """
    params = [patient_id] if patient_id else []
    rows = conn.execute(sql, params).fetchall()
    cols = [d[0] for d in conn.execute("SELECT * FROM patient_journey_events LIMIT 0").description]
    touchpoints = [dict(zip(cols, r)) for r in rows]

    # 获取转化事件
    conv_sql = "SELECT * FROM patient_journey_events WHERE event_type = 'conversion'"
    conv_params = []
    if patient_id:
        conv_sql += " AND patient_id = ?"
        conv_params.append(patient_id)
    conv_sql += " ORDER BY timestamp DESC"

    conv_rows = conn.execute(conv_sql, conv_params).fetchall()
    conv_cols = [d[0] for d in conn.execute("SELECT * FROM patient_journey_events LIMIT 0").description]
    conversions = [dict(zip(conv_cols, r)) for r in conv_rows]

    if not touchpoints:
        return {"error": "No touchpoints found", "patient_id": patient_id, "data_source": "patient_journey_events"}

    weights = get_attribution_weights(touchpoints, model)

    attributed = []
    total_value = sum(c.get("value", 0) for c in conversions) if conversions else 0

    for i, tp in enumerate(touchpoints):
        w = weights[i] if i < len(weights) else 0
        attributed.append({
            "touchpoint_id": tp.get("id"),
            "patient_id": tp.get("patient_id"),
            "content_id": tp.get("content_id"),
            "kol_id": tp.get("kol_id"),
            "channel": tp.get("channel"),
            "platform": tp.get("platform"),
            "touchpoint_type": tp.get("touchpoint_type"),
            "timestamp": tp.get("timestamp"),
            "weight": round(w, 4),
            "attributed_value": round(total_value * w, 2),
        })

    attributed.sort(key=lambda x: -x["weight"])

    channel_weights = defaultdict(lambda: {"weight": 0, "count": 0, "attributed_value": 0})
    for a in attributed:
        ch = a.get("channel", "unknown")
        channel_weights[ch]["weight"] += a["weight"]
        channel_weights[ch]["count"] += 1
        channel_weights[ch]["attributed_value"] += a["attributed_value"]

    return {
        "conversion_id": conversion_id,
        "patient_id": patient_id,
        "model": model,
        "data_source": "patient_journey_events",
        "touchpoint_count": len(touchpoints),
        "conversion_count": len(conversions),
        "total_attributed_value": round(sum(a["attributed_value"] for a in attributed), 2),
        "top_touchpoints": attributed[:10],
        "channel_summary": [
            {**{"channel": ch}, **v} for ch, v in channel_weights.items()
        ],
    }


def _attribute_conversion_legacy(conversion_id: str = None, patient_id: str = None, model: str = "last_touch", conn=None) -> dict:
    """基于旧 patient_touchpoints + conversion_events 表的归因分析（兼容）"""
    query = "SELECT * FROM patient_touchpoints WHERE 1=1"
    params = []
    if patient_id:
        query += " AND patient_id = ?"
        params.append(patient_id)
    query += " ORDER BY timestamp ASC"

    rows = conn.execute(query, params).fetchall()
    cols = [d[0] for d in conn.execute("SELECT * FROM patient_touchpoints LIMIT 0").description]
    all_touchpoints = [dict(zip(cols, r)) for r in rows]

    if not all_touchpoints:
        return {"error": "No touchpoints found", "conversion_id": conversion_id, "patient_id": patient_id}

    conv_query = "SELECT * FROM conversion_events WHERE 1=1"
    conv_params = []
    if patient_id:
        conv_query += " AND patient_id = ?"
        conv_params.append(patient_id)
    if conversion_id:
        conv_query += " AND id = ?"
        conv_params.append(conversion_id)
    conv_query += " ORDER BY timestamp DESC"

    conv_rows = conn.execute(conv_query, conv_params).fetchall()
    conv_cols = [d[0] for d in conn.execute("SELECT * FROM conversion_events LIMIT 0").description]
    conversions = [dict(zip(conv_cols, r)) for r in conv_rows]

    weights = get_attribution_weights(all_touchpoints, model)

    attributed = []
    for i, tp in enumerate(all_touchpoints):
        w = weights[i] if i < len(weights) else 0
        conv_value = sum(c.get("value", 0) for c in conversions) * w if conversions else 0
        attributed.append({
            "touchpoint_id": tp.get("id"),
            "patient_id": tp.get("patient_id"),
            "content_id": tp.get("content_id"),
            "kol_id": tp.get("kol_id"),
            "channel": tp.get("channel"),
            "platform": tp.get("platform"),
            "touchpoint_type": tp.get("touchpoint_type"),
            "timestamp": tp.get("timestamp"),
            "weight": round(w, 4),
            "attributed_value": round(conv_value, 2),
        })

    attributed.sort(key=lambda x: -x["weight"])

    channel_weights = defaultdict(lambda: {"weight": 0, "count": 0, "attributed_value": 0})
    for a in attributed:
        ch = a.get("channel", "unknown")
        channel_weights[ch]["weight"] += a["weight"]
        channel_weights[ch]["count"] += 1
        channel_weights[ch]["attributed_value"] += a["attributed_value"]

    return {
        "conversion_id": conversion_id,
        "patient_id": patient_id,
        "model": model,
        "data_source": "legacy (touchpoints+conversions)",
        "touchpoint_count": len(all_touchpoints),
        "conversion_count": len(conversions),
        "total_attributed_value": sum(a["attributed_value"] for a in attributed),
        "top_touchpoints": attributed[:10],
        "channel_summary": [
            {**{"channel": ch}, **v} for ch, v in channel_weights.items()
        ],
    }


def get_channel_summary(period_days: int = 30, model: str = "last_touch") -> dict:
    """渠道汇总归因（跨所有转化，基于统一患者旅程事件模型）"""
    conn = get_conn()
    
    try:
        # 检查新模型
        new_model = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='patient_journey_events'"
        ).fetchone() is not None

        if new_model:
            rows = conn.execute("""
                SELECT * FROM patient_journey_events
                WHERE event_type = 'touchpoint'
                  AND timestamp >= datetime('now', ?)
                ORDER BY timestamp ASC
            """, (f"-{period_days} days",)).fetchall()

            cols = [d[0] for d in conn.execute("SELECT * FROM patient_journey_events LIMIT 0").description]
            touchpoints = [dict(zip(cols, r)) for r in rows]

            conv_rows = conn.execute("""
                SELECT * FROM patient_journey_events
                WHERE event_type = 'conversion'
                  AND timestamp >= datetime('now', ?)
            """, (f"-{period_days} days",)).fetchall()
            conv_cols = [d[0] for d in conn.execute("SELECT * FROM patient_journey_events LIMIT 0").description]
            conversions = [dict(zip(conv_cols, r)) for r in conv_rows]
        else:
            rows = conn.execute("""
                SELECT * FROM patient_touchpoints
                WHERE timestamp >= datetime('now', ?)
                ORDER BY timestamp ASC
            """, (f"-{period_days} days",)).fetchall()
            cols = [d[0] for d in conn.execute("SELECT * FROM patient_touchpoints LIMIT 0").description]
            touchpoints = [dict(zip(cols, r)) for r in rows]

            conv_rows = conn.execute("""
                SELECT * FROM conversion_events
                WHERE timestamp >= datetime('now', ?)
            """, (f"-{period_days} days",)).fetchall()
            conv_cols = [d[0] for d in conn.execute("SELECT * FROM conversion_events LIMIT 0").description]
            conversions = [dict(zip(conv_cols, r)) for r in conv_rows]

        if not touchpoints:
            return {
                "period_days": period_days,
                "model": model,
                "error": "No touchpoints in period",
                "data_source": "patient_journey_events" if new_model else "legacy"
            }

        patient_weights = defaultdict(list)
        patient_conversions = defaultdict(list)

        for tp in touchpoints:
            patient_weights[tp["patient_id"]].append(tp)
        for conv in conversions:
            patient_conversions[conv["patient_id"]].append(conv)

        channel_totals = defaultdict(lambda: {"attributed_value": 0, "touchpoint_count": 0})

        for patient_id, tp_list in patient_weights.items():
            weights = get_attribution_weights(tp_list, model)
            convs = patient_conversions.get(patient_id, [])
            total_value = sum(c.get("value", 0) for c in convs)

            for i, tp in enumerate(tp_list):
                w = weights[i] if i < len(weights) else 0
                ch = tp.get("channel", "unknown")
                channel_totals[ch]["attributed_value"] += total_value * w
                channel_totals[ch]["touchpoint_count"] += 1

        summary = [
            {
                "channel": ch,
                "attributed_value": round(v["attributed_value"], 2),
                "touchpoint_count": v["touchpoint_count"],
                "value_share": 0,
            }
            for ch, v in channel_totals.items()
        ]

        total_value = sum(s["attributed_value"] for s in summary) or 1
        for s in summary:
            s["value_share"] = round(s["attributed_value"] / total_value, 4)

        summary.sort(key=lambda x: -x["attributed_value"])

        return {
            "period_days": period_days,
            "model": model,
            "data_source": "patient_journey_events" if new_model else "legacy",
            "total_touchpoints": len(touchpoints),
            "total_conversions": len(conversions),
            "channel_summary": summary,
        }
    finally:
        close_conn(conn)


def analyze_funnel(period_days: int = 30) -> dict:
    """漏斗分析（基于统一患者旅程事件模型）"""
    conn = get_conn()
    
    try:
        new_model = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='patient_journey_events'"
        ).fetchone() is not None

        if new_model:
            touchpoint_counts = conn.execute("""
                SELECT touchpoint_type, COUNT(*) as cnt
                FROM patient_journey_events
                WHERE event_type = 'touchpoint'
                  AND timestamp >= datetime('now', ?)
                GROUP BY touchpoint_type
                ORDER BY cnt DESC
            """, (f"-{period_days} days",)).fetchall()

            conversion_counts = conn.execute("""
                SELECT touchpoint_type as conversion_type, COUNT(*) as cnt, SUM(value) as total_value
                FROM patient_journey_events
                WHERE event_type = 'conversion'
                  AND timestamp >= datetime('now', ?)
                GROUP BY touchpoint_type
                ORDER BY cnt DESC
            """, (f"-{period_days} days",)).fetchall()

            return {
                "period_days": period_days,
                "data_source": "patient_journey_events",
                "touchpoint_funnel": [{"type": r[0], "count": r[1]} for r in touchpoint_counts],
                "conversion_funnel": [{"type": r[0], "count": r[1], "total_value": r[2] or 0} for r in conversion_counts],
            }
        else:
            touchpoint_counts = conn.execute("""
                SELECT touchpoint_type, COUNT(*) as cnt
                FROM patient_touchpoints
                WHERE timestamp >= datetime('now', ?)
                GROUP BY touchpoint_type
                ORDER BY cnt DESC
            """, (f"-{period_days} days",)).fetchall()

            conversion_counts = conn.execute("""
                SELECT conversion_type, COUNT(*) as cnt, SUM(value) as total_value
                FROM conversion_events
                WHERE timestamp >= datetime('now', ?)
                GROUP BY conversion_type
                ORDER BY cnt DESC
            """, (f"-{period_days} days",)).fetchall()

            return {
                "period_days": period_days,
                "data_source": "legacy",
                "touchpoint_funnel": [{"type": r[0], "count": r[1]} for r in touchpoint_counts],
                "conversion_funnel": [{"type": r[0], "count": r[1], "total_value": r[2] or 0} for r in conversion_counts],
            }
    finally:
        close_conn(conn)


def _parse_args():
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError:
            return {}
    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return {}
    return {}


if __name__ == "__main__":
    args = _parse_args()
    action = args.get("action", "channel_summary")
    model = args.get("model", "last_touch")
    conversion_id = args.get("conversion_id")
    patient_id = args.get("patient_id")
    period_days = args.get("period_days", 30)

    if action == "attribute":
        result = attribute_conversion(conversion_id, patient_id, model)
    elif action == "channel_summary":
        result = get_channel_summary(period_days, model)
    elif action == "funnel":
        result = analyze_funnel(period_days)
    elif action == "models":
        result = {"supported_models": SUPPORTED_MODELS}
    elif action == "cac":
        result = calculate_cac(period_days)
    elif action == "ltv":
        result = calculate_ltv(period_days)
    elif action == "cac_ltv":
        result = cac_ltv_analysis(period_days)
    else:
        result = {"error": f"Unknown action: {action}"}

    print(json.dumps(result, ensure_ascii=False, indent=2))
