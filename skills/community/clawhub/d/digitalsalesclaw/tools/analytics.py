#!/usr/bin/env python3
"""
DigitalSalesClaw - analytics.py
运营数据分析工具

输入: {"action": "overview|content|trend|patient", "period": "7d|30d|90d"}
输出: {...}
"""
import sys
import json
from pathlib import Path
from datetime import datetime, date, timedelta
from decimal import Decimal
from db import get_conn, close_conn, query_all, query_one


def _json_serial(obj):
    """JSON serializer for objects not serializable by default."""
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def get_period_days(period: str) -> int:
    return {"7d": 7, "30d": 30, "90d": 90}.get(period, 30)


def get_overview(conn, period: str = "30d") -> dict:
    """运营总览"""
    days = get_period_days(period)

    # 内容指标
    content_agg = query_one(f"""
        SELECT
            COUNT(DISTINCT campaign_id) as campaigns,
            SUM(impressions) as impressions,
            SUM(clicks) as clicks,
            SUM(conversions) as conversions,
            SUM(spend) as spend,
            AVG(engagement_rate) as avg_engagement,
            AVG(ctr) as avg_ctr
        FROM content_metrics
        WHERE date >= DATE_SUB(NOW(), INTERval %s day)
    """, (days,)) or {}

    # 患者模块
    active_patients = query_one("SELECT COUNT(*) as c FROM patient_sessions WHERE status = 'active'")["c"]
    total_sessions = query_one("SELECT COUNT(*) as c FROM patient_sessions")["c"]
    pending_msgs = query_one("SELECT COUNT(*) as c FROM patient_messages WHERE sent = 0")["c"]

    # 合规
    compliance_alerts = query_one("""
        SELECT COUNT(*) as c FROM compliance_reviews
        WHERE risk_level IN ('critical', 'high')
          AND created_at >= DATE_SUB(NOW(), INTERVAL %s day)
    """, (days,))["c"]

    # 药房
    low_stock = query_one("SELECT COUNT(*) as c FROM pharmacy_inventory WHERE status IN ('low', 'out')")["c"]

    # 活动
    active_campaigns = query_one("SELECT COUNT(*) as c FROM content_campaigns WHERE status = 'active'")["c"]

    impressions = content_agg.get("impressions") or 0
    clicks = content_agg.get("clicks") or 0
    ctr = round(clicks / impressions * 100, 2) if impressions > 0 else 0

    if ctr >= 5:
        ctr_rating = "excellent"
    elif ctr >= 2:
        ctr_rating = "good"
    elif ctr >= 1:
        ctr_rating = "average"
    else:
        ctr_rating = "poor"

    alerts = []
    if compliance_alerts > 0:
        alerts.append(f"⚠️ {compliance_alerts} 条高风险合规告警")
    if low_stock > 0:
        alerts.append(f"💊 {low_stock} 个品种库存不足")
    if pending_msgs > 5:
        alerts.append(f"👥 {pending_msgs} 条患者消息待回复")

    return {
        "period": period,
        "period_days": days,
        "content": {
            "active_campaigns": active_campaigns,
            "impressions": impressions,
            "clicks": clicks,
            "conversions": content_agg.get("conversions") or 0,
            "spend": content_agg.get("spend") or 0,
            "avg_ctr": ctr,
            "ctr_rating": ctr_rating,
            "avg_engagement": round(content_agg.get("avg_engagement") or 0, 2),
        },
        "patient": {
            "active_sessions": active_patients,
            "total_sessions": total_sessions,
            "pending_messages": pending_msgs,
        },
        "compliance": {
            "high_risk_alerts": compliance_alerts,
        },
        "pharmacy": {
            "low_stock_items": low_stock,
        },
        "alerts": alerts,
        "suggestions": [
            f"近{days}天运营概览",
            f"曝光 {impressions:,} 次，CTR {ctr}%" if impressions else "暂无内容数据",
            f"活跃患者 {active_patients} 个",
            " ".join(alerts) if alerts else "各模块运行正常"
        ]
    }


def get_content_trend(conn, period: str = "30d") -> dict:
    """内容趋势"""
    days = get_period_days(period)

    rows = query_all(f"""
        SELECT date, SUM(impressions) as impressions, SUM(clicks) as clicks,
               SUM(conversions) as conversions, AVG(engagement_rate) as eng_rate
        FROM content_metrics
        WHERE date >= DATE_SUB(NOW(), INTERVAL %s day)
        GROUP BY date
        ORDER BY date ASC
    """, (days,))

    trend = [dict(r) for r in rows]

    if len(trend) >= 2:
        half = len(trend) // 2
        first_half = trend[:half]
        second_half = trend[half:]
        avg_impr_first = float(sum(t.get("impressions", 0) for t in first_half)) / max(len(first_half), 1)
        avg_impr_second = float(sum(t.get("impressions", 0) for t in second_half)) / max(len(second_half), 1)
        trend_direction = "up" if avg_impr_second > avg_impr_first * 1.1 else "down" if avg_impr_second < avg_impr_first * 0.9 else "stable"
        impressions_trend = round((avg_impr_second - avg_impr_first) / max(avg_impr_first, 1) * 100, 1)
    else:
        trend_direction = "stable"
        impressions_trend = 0

    return {
        "period": period,
        "data_points": len(trend),
        "trend_direction": trend_direction,
        "impressions_change_pct": impressions_trend,
        "daily_data": trend,
        "suggestions": [
            f"近{period}内容趋势{'上升📈' if trend_direction=='up' else '下降📉' if trend_direction=='down' else '稳定➡️'} {impressions_trend:+.1f}%" if impressions_trend else "数据不足",
            f"共 {len(trend)} 天数据",
        ]
    }


def get_patient_analytics(conn, period: str = "30d") -> dict:
    """患者分析"""
    days = get_period_days(period)

    sessions = query_one("""
        SELECT COUNT(*) as c FROM patient_sessions
        WHERE created_at >= DATE_SUB(NOW(), INTERVAL %s day)
    """, (days,))["c"]

    resolved = query_one("""
        SELECT COUNT(*) as c FROM patient_sessions
        WHERE status = 'resolved' AND updated_at >= DATE_SUB(NOW(), INTERVAL %s day)
    """, (days,))["c"]

    total_messages = query_one("""
        SELECT COUNT(*) as c FROM patient_messages
        WHERE created_at >= DATE_SUB(NOW(), INTERVAL %s day)
    """, (days,))["c"]

    resolution_rate = round(resolved / sessions * 100, 1) if sessions > 0 else 0

    return {
        "period": period,
        "new_sessions": sessions,
        "resolved_sessions": resolved,
        "total_messages": total_messages,
        "resolution_rate": resolution_rate,
        "suggestions": [
            f"近{period}新增会话 {sessions} 个",
            f"解决率 {resolution_rate}%" if sessions else "暂无数据",
        ]
    }


def roi_analysis(campaign_id: str = None, period: str = "30d", model: str = "last_touch") -> dict:
    """
    ROI 分析（整合归因 + ROI 计算 + 趋势环比）
    调用 attribution.py 归因模型，支持 6 种归因方式
    """
    days = get_period_days(period)

    # 活动花费汇总
    if campaign_id:
        spend_row = query_one("""
            SELECT SUM(spend) as total_spend, SUM(conversions) as total_conversions,
                   SUM(impressions) as total_impressions, SUM(clicks) as total_clicks
            FROM content_metrics
            WHERE campaign_id = %s AND date >= DATE_SUB(NOW(), INTERVAL %s DAY)
        """, (campaign_id, days))
        cname_row = query_one("SELECT name FROM content_campaigns WHERE id = %s", (campaign_id,))
        campaign_name = cname_row["name"] if cname_row else campaign_id
    else:
        spend_row = query_one("""
            SELECT SUM(spend) as total_spend, SUM(conversions) as total_conversions,
                   SUM(impressions) as total_impressions, SUM(clicks) as total_clicks
            FROM content_metrics
            WHERE date >= DATE_SUB(NOW(), INTERVAL %s DAY)
        """, (days,))
        campaign_name = "全渠道"

    spend = spend_row.get("total_spend") or 0
    conversions = spend_row.get("total_conversions") or 0
    impressions = spend_row.get("total_impressions") or 0
    clicks = spend_row.get("total_clicks") or 0

    # 归因渠道数据（调用 attribution 模块）
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from attribution import get_channel_summary
        channel_data = get_channel_summary(period_days=days, model=model)
    except Exception as e:
        channel_data = {"error": f"归因模块不可用: {e}"}

    # ROI 计算
    avg_conversion_value = 100  # placeholder，待业务确认
    revenue = conversions * avg_conversion_value
    roi = round((revenue - spend) / spend * 100, 2) if spend > 0 else 0
    cpa = round(spend / conversions, 2) if conversions > 0 else 0
    ctr = round(clicks / impressions * 100, 2) if impressions > 0 else 0

    # 环比（上一个等长周期）
    prev_row = query_one("""
        SELECT SUM(spend) as ps, SUM(conversions) as pc
        FROM content_metrics
        WHERE date BETWEEN DATE_SUB(NOW(), INTERVAL %s DAY) - INTERVAL %s DAY
                          AND DATE_SUB(NOW(), INTERVAL %s DAY) - INTERVAL 1 DAY
    """, (days, days, days))
    prev_spend = prev_row.get("ps") or 0
    prev_conv = prev_row.get("pc") or 0
    spend_chg = round((spend - prev_spend) / prev_spend * 100, 2) if prev_spend > 0 else 0
    conv_chg = round((conversions - prev_conv) / prev_conv * 100, 2) if prev_conv > 0 else 0

    return {
        "campaign": campaign_name,
        "campaign_id": campaign_id,
        "period": period,
        "days": days,
        "spend": spend,
        "conversions": conversions,
        "impressions": impressions,
        "clicks": clicks,
        "ctr": ctr,
        "revenue": revenue,
        "roi_percent": roi,
        "cpa": cpa,
        "avg_conversion_value_assumed": avg_conversion_value,
        "attribution_model": model,
        "channel_attribution": channel_data.get("channels", {}),
        "period_change": {"spend_pct": spend_chg, "conversions_pct": conv_chg},
        "suggestions": [
            f"ROI {roi:.1f}%，{'盈利' if roi > 0 else '亏损'}",
            f"CPA {cpa:.2f} 元/转化",
            f"花费环比 {spend_chg:+.1f}%，转化环比 {conv_chg:+.1f}%",
        ],
    }


def _parse_args():
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError:
            return {"action": "overview"}
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
    action = args.get("action", "overview")
    period = args.get("period", "30d")

    conn = get_conn()

    try:
        if action == "overview":
            result = get_overview(conn, period)
        elif action in ("content", "trend"):
            result = get_content_trend(conn, period)
        elif action == "patient":
            result = get_patient_analytics(conn, period)
        elif action == "roi":
            result = roi_analysis(campaign_id=args.get("campaign_id"), period=period, model=args.get("model", "last_touch"))
        else:
            result = {"error": f"Unknown action: {action}"}
    finally:
        close_conn(conn)

    print(json.dumps(result, ensure_ascii=False, indent=2, default=_json_serial))