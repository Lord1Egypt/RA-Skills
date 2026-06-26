#!/usr/bin/env python3
"""
DigitalSalesClaw - smart_analytics.py
智能异常检测工具

功能:
- 内容效果异常波动告警（CTR、互动率、曝光量）
- 患者活跃度异常识别（突然失联、激增）
- 库存异常预警（断货、积压）

输入: {"action": "content_anomaly|patient_anomaly|inventory_anomaly|all", "period_days": 7, "threshold": 2.0}
输出: {"anomalies, summary, alerts}
"""

import sys
import json
import math
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent


def _get_conn():
    """获取数据库连接（MySQL 优先）"""
    try:
        import mysql.connector
        from mysql.connector import pooling
        pool = pooling.MySQLConnectionPool(
            host="localhost", port=3306, user="ontology", unix_socket="/tmp/mysql.sock",
            password="ontology", database="digitalsalesclaw",
            pool_name="dsc_analytics", pool_size=3, charset="utf8mb4"
        )
        conn = pool.get_connection()
        conn.autocommit = False
        return conn, False
    except Exception:
        conn = get_conn()
        return conn, True


# ─────────────────────────────────────────
# 异常检测核心算法
# ─────────────────────────────────────────

def zscore(values, current):
    """计算 Z-score：当前值偏离均值的标准差倍数"""
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    std = math.sqrt(variance) if variance > 0 else 1.0
    return (current - mean) / std


def detect_spike(values, current, factor=2.0):
    """检测是否异常激增（当前值是均值的 factor 倍）"""
    if not values:
        return False
    mean = sum(values) / len(values)
    return current > mean * factor


def detect_drop(values, current, factor=0.5):
    """检测是否异常下降（当前值低于均值的 factor 倍）"""
    if not values:
        return False
    mean = sum(values) / len(values)
    return 0 < current < mean * factor


# ─────────────────────────────────────────
# 内容效果异常检测
# ─────────────────────────────────────────

def detect_content_anomalies(period_days=7, threshold=2.0, conn=None):
    """
    检测内容效果异常波动
    - CTR 异常（暴涨/暴跌）
    - 互动率异常
    - 曝光量异常
    """
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        baseline_rows = conn.execute("""
            SELECT campaign_id, AVG(ctr) as avg_ctr, AVG(engagement_rate) as avg_eng,
                   SUM(impressions) as total_imp
            FROM content_metrics
            WHERE date < datetime('now', ?)
            GROUP BY campaign_id
        """, (f"-{period_days} days",)).fetchall()

        baseline = {}
        for row in baseline_rows:
            baseline[row["campaign_id"]] = {
                "avg_ctr": row["avg_ctr"] or 0,
                "avg_engagement": row["avg_eng"] or 0,
                "total_impressions": row["total_imp"] or 0,
            }

        current_rows = conn.execute("""
            SELECT cm.id, cm.campaign_id, cm.ctr, cm.engagement_rate,
                   cm.impressions, cm.clicks, cm.date, cc.name as campaign_name
            FROM content_metrics cm
            LEFT JOIN content_campaigns cc ON cc.id = cm.campaign_id
            WHERE cm.date >= datetime('now', ?)
            ORDER BY cm.date DESC
        """, (f"-{period_days} days",)).fetchall()

        cols = [d[0] for d in conn.execute("SELECT * FROM content_metrics LIMIT 0").description]
        current = [dict(zip(cols, r)) for r in current_rows]

        anomalies = []
        for metric in current:
            cid = metric.get("campaign_id")
            if cid not in baseline:
                continue

            b = baseline[cid]
            z_ctr = zscore([b["avg_ctr"]], metric.get("ctr") or 0)
            z_eng = zscore([b["avg_engagement"]], metric.get("engagement_rate") or 0)

            if abs(z_ctr) >= threshold:
                direction = "spike" if z_ctr > 0 else "drop"
                anomalies.append({
                    "type": "ctr_anomaly",
                    "campaign_id": cid,
                    "campaign_name": metric.get("campaign_name"),
                    "metric_date": metric.get("date"),
                    "current_ctr": round(metric.get("ctr") or 0, 4),
                    "baseline_ctr": round(b["avg_ctr"], 4),
                    "z_score": round(z_ctr, 2),
                    "direction": direction,
                    "severity": "critical" if abs(z_ctr) >= 3 else "high" if abs(z_ctr) >= 2 else "medium",
                    "suggestion": "CTR暴涨，建议追加投放" if direction == "spike" else "CTR暴跌，建议检查内容或外部因素",
                })

            imp = metric.get("impressions") or 0
            b_imp = b["total_impressions"]
            if b_imp > 0:
                ratio = imp / b_imp
                if ratio >= 2.5 or (0 < imp < b_imp * 0.3):
                    direction = "spike" if ratio >= 2.5 else "drop"
                    anomalies.append({
                        "type": "impression_anomaly",
                        "campaign_id": cid,
                        "campaign_name": metric.get("campaign_name"),
                        "metric_date": metric.get("date"),
                        "current_impressions": imp,
                        "baseline_impressions": b_imp,
                        "direction": direction,
                        "severity": "high",
                        "suggestion": "曝光量暴涨，关注转化承接" if direction == "spike" else "曝光量骤降，检查投放状态或平台限流",
                    })

        return {
            "period_days": period_days,
            "threshold": threshold,
            "total_campaigns_checked": len(baseline),
            "anomaly_count": len(anomalies),
            "anomalies": anomalies,
            "summary": {
                "critical": len([a for a in anomalies if a["severity"] == "critical"]),
                "high": len([a for a in anomalies if a["severity"] == "high"]),
                "medium": len([a for a in anomalies if a["severity"] == "medium"]),
            }
        }
    finally:
        if own_conn:
            conn.close()


# ─────────────────────────────────────────
# 患者活跃度异常检测
# ─────────────────────────────────────────

def detect_patient_anomalies(period_days=7, threshold=2.0, conn=None):
    """
    检测患者活跃度异常
    - 突然失联（长期活跃患者突然无消息）
    - 活跃度激增（大量新患者涌入）
    """
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        daily_new = conn.execute("""
            SELECT date(created_at) as day, COUNT(*) as new_sessions
            FROM patient_sessions
            WHERE created_at >= datetime('now', ?)
            GROUP BY day
            ORDER BY day
        """, (f"-{period_days * 2} days",)).fetchall()

        days = [str(r[0]) for r in daily_new]
        counts = [r[1] for r in daily_new]

        mid = len(counts) // 2
        baseline = counts[:mid] if mid > 0 else counts
        current = counts[mid:] if mid > 0 else []

        anomalies = []

        if len(current) >= 2:
            current_avg = sum(current) / len(current)
            baseline_avg = sum(baseline) / len(baseline) if baseline else 0

            if baseline_avg > 0 and current_avg > baseline_avg * 2:
                anomalies.append({
                    "type": "new_session_spike",
                    "description": "新增患者会话激增",
                    "baseline_avg": baseline_avg,
                    "current_avg": current_avg,
                    "multiplier": round(current_avg / baseline_avg, 1),
                    "severity": "high",
                    "suggestion": "患者涌入增加，建议检查是否有活动推广或突发事件",
                })
            elif baseline_avg > 0 and current_avg < baseline_avg * 0.3:
                anomalies.append({
                    "type": "new_session_drop",
                    "description": "新增患者会话骤降",
                    "baseline_avg": baseline_avg,
                    "current_avg": current_avg,
                    "severity": "medium",
                    "suggestion": "新患者来源减少，建议检查渠道投放或内容曝光",
                })

        silent = conn.execute("""
            SELECT ps.session_id, ps.patient_name, ps.status,
                   MAX(pm.created_at) as last_message,
                   julianday('now') - julianday(MAX(pm.created_at)) as daysSilent
            FROM patient_sessions ps
            LEFT JOIN patient_messages pm ON pm.session_id = ps.session_id
            WHERE ps.status = 'active'
            GROUP BY ps.session_id
            HAVING daysSilent > 3
            ORDER BY daysSilent DESC
            LIMIT 20
        """).fetchall()

        silent_list = []
        for row in silent:
            silent_list.append({
                "session_id": row[0],
                "patient_name": row[1],
                "status": row[2],
                "last_message": row[3],
                "days_silent": round(row[4], 1),
            })

        critical_silent = [s for s in silent_list if s["days_silent"] > 7]
        if critical_silent:
            anomalies.append({
                "type": "silent_patients",
                "description": f"发现 {len(critical_silent)} 位患者超过7天无消息",
                "critical_count": len(critical_silent),
                "total_silent_over_3d": len(silent_list),
                "severity": "high" if len(critical_silent) >= 3 else "medium",
                "silent_patients": critical_silent[:5],
                "suggestion": "高风险失联患者建议电话/短信主动触达",
            })

        return {
            "period_days": period_days,
            "anomaly_count": len(anomalies),
            "anomalies": anomalies,
            "silent_patients_3d_plus": len(silent_list),
            "summary": {
                "critical": len([a for a in anomalies if a["severity"] == "critical"]),
                "high": len([a for a in anomalies if a["severity"] == "high"]),
                "medium": len([a for a in anomalies if a["severity"] == "medium"]),
            }
        }
    finally:
        if own_conn:
            conn.close()


# ─────────────────────────────────────────
# 库存异常检测
# ─────────────────────────────────────────

def detect_inventory_anomalies(conn=None):
    """检测库存异常（断货预警、积压预警）"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        items = conn.execute("""
            SELECT product_id, product_name, quantity, reorder_point,
                   pharmacy, status, last_restocked
            FROM pharmacy_inventory
            ORDER BY (CAST(quantity AS REAL) / NULLIF(reorder_point, 0)) ASC
        """).fetchall()

        cols = [d[0] for d in conn.execute("SELECT * FROM pharmacy_inventory LIMIT 0").description]
        inventory = [dict(zip(cols, r)) for r in items]

        anomalies = []

        for item in inventory:
            qty = item.get("quantity") or 0
            reorder = item.get("reorder_point") or 10
            ratio = qty / reorder if reorder > 0 else 0

            if qty == 0 or item.get("status") == "out":
                anomalies.append({
                    "type": "stockout",
                    "product_id": item.get("product_id"),
                    "product_name": item.get("product_name"),
                    "current_stock": qty,
                    "reorder_point": reorder,
                    "severity": "critical",
                    "suggestion": f"{item.get('product_name')} 已售罄，立即补货",
                })
            elif ratio < 0.5:
                days_until_empty = round(ratio * 7)
                anomalies.append({
                    "type": "low_stock",
                    "product_id": item.get("product_id"),
                    "product_name": item.get("product_name"),
                    "current_stock": qty,
                    "reorder_point": reorder,
                    "stock_ratio": round(ratio, 2),
                    "estimated_days_remaining": days_until_empty,
                    "severity": "high" if ratio < 0.25 else "medium",
                    "suggestion": f"{item.get('product_name')} 库存不足，预计可支撑 {days_until_empty} 天",
                })
            elif ratio > 3:
                anomalies.append({
                    "type": "overstock",
                    "product_id": item.get("product_id"),
                    "product_name": item.get("product_name"),
                    "current_stock": qty,
                    "reorder_point": reorder,
                    "stock_ratio": round(ratio, 2),
                    "severity": "medium",
                    "suggestion": f"{item.get('product_name')} 库存积压，是正常备货量的 {round(ratio, 1)} 倍",
                })

        return {
            "anomaly_count": len(anomalies),
            "anomalies": anomalies,
            "summary": {
                "critical": len([a for a in anomalies if a["severity"] == "critical"]),
                "high": len([a for a in anomalies if a["severity"] == "high"]),
                "medium": len([a for a in anomalies if a["severity"] == "medium"]),
                "overstock": len([a for a in anomalies if a["type"] == "overstock"]),
            }
        }
    finally:
        if own_conn:
            conn.close()


# ─────────────────────────────────────────
# 综合异常检测（纯检测，不含告警；告警由 triggers.py 负责）
# ─────────────────────────────────────────

def full_anomaly_scan(period_days=7, threshold=2.0):
    """
    执行全维度异常扫描
    告警逻辑已移至 triggers.py（职责分离：检测结果 → 推送 triggers → 告警）
    """
    conn, is_sqlite = _get_conn()

    try:
        content = detect_content_anomalies(period_days, threshold, conn)
        patient = detect_patient_anomalies(period_days, threshold, conn)
        inventory = detect_inventory_anomalies(conn)

        all_anomalies = content["anomalies"] + patient["anomalies"] + inventory["anomalies"]
        critical = len([a for a in all_anomalies if a.get("severity") == "critical"])
        high = len([a for a in all_anomalies if a.get("severity") == "high"])

        return {
            "scan_id": f"SCAN-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "period_days": period_days,
            "threshold": threshold,
            "total_anomalies": len(all_anomalies),
            "severity_summary": {"critical": critical, "high": high, "medium": len(all_anomalies) - critical - high},
            "content_anomalies": content["anomalies"],
            "patient_anomalies": patient["anomalies"],
            "inventory_anomalies": inventory["anomalies"],
            "alert_suggestions": [  # 仅建议，不执行告警
                f"发现 {critical} 个 critical 级别异常需立即处理",
                f"发现 {high} 个 high 级别异常需尽快处理",
                "建议优先处理 critical → high → medium"
            ] if all_anomalies else ["未检测到明显异常"],
        }
    finally:
        close_conn(conn)


# ─────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────

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
    action = args.get("action", "all")
    period_days = args.get("period_days", 7)
    threshold = args.get("threshold", 2.0)

    if action == "content_anomaly":
        result = detect_content_anomalies(period_days, threshold)
    elif action == "patient_anomaly":
        result = detect_patient_anomalies(period_days, threshold)
    elif action == "inventory_anomaly":
        result = detect_inventory_anomalies()
    elif action == "all":
        result = full_anomaly_scan(period_days, threshold)
    else:
        result = {"error": f"Unknown action: {action}"}

    print(json.dumps(result, ensure_ascii=False, indent=2))
