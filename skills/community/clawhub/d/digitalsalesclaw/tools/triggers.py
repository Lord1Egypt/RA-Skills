#!/usr/bin/env python3
"""
DigitalSalesClaw - triggers.py
事件触发器引擎
支持定时触发 + 条件触发 + 数据异常触发

输入: {"action": "check|list|trigger", "trigger_name": "...", "params": {...}}
输出: {"triggered: [...], alerts: [...]}
"""

import sys
import json
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
            pool_name="dsc_triggers", pool_size=3, charset="utf8mb4"
        )
        conn = pool.get_connection()
        conn.autocommit = False
        return conn, False
    except Exception:
        conn = get_conn()
        return conn, True


# ─────────────────────────────────────────
# 触发器定义
# ─────────────────────────────────────────
TRIGGERS = {
    "low_inventory_alert": {
        "name": "低库存告警",
        "type": "data_threshold",
        "condition": "pharmacy_inventory.status == 'low' OR pharmacy_inventory.status == 'out'",
        "threshold": 1,
        "severity": "high",
        "message": "库存不足告警",
    },
    "compliance_violation": {
        "name": "合规违规告警",
        "type": "data_threshold",
        "condition": "compliance_reviews.risk_level == 'critical'",
        "threshold": 1,
        "severity": "critical",
        "message": "发现合规严重违规",
    },
    "high_risk_patient": {
        "name": "高风险患者告警",
        "type": "data_threshold",
        "condition": "patient_sessions.status == 'pending' AND pending_messages >= 3",
        "threshold": 1,
        "severity": "high",
        "message": "高风险患者需干预",
    },
    "content_low_performance": {
        "name": "内容低绩效告警",
        "type": "data_threshold",
        "condition": "content_metrics.engagement_rate < 0.01",
        "threshold": 3,
        "severity": "medium",
        "message": "多内容互动率持续走低",
    },
    "campaign_budget_exceeded": {
        "name": "预算超支告警",
        "type": "data_threshold",
        "condition": "content_campaigns.budget > 0 AND SUM(spend) > budget",
        "threshold": 1,
        "severity": "high",
        "message": "营销活动预算超支",
    },
    "daily_digest": {
        "name": "每日运营摘要",
        "type": "scheduled",
        "schedule": "0 9 * * *",  # 每天9点
        "severity": "info",
        "message": "每日运营数据摘要",
    },
}


def check_all_triggers() -> dict:
    """
    检查所有触发器（数据阈值触发）
    内容/患者/库存的异常检测委托给 smart_analytics.py，triggers.py 专注告警逻辑
    """
    conn, is_sqlite = _get_conn()
    triggered = []
    alerts = []

    try:
        # 1. 低库存告警（独立查询）
        date_filter = "datetime('now', '-7 days')" if is_sqlite else "DATE_SUB(NOW(), INTERVAL 7 DAY)"
        if is_sqlite:
            low_inv = conn.execute("""
                SELECT COUNT(*) as cnt FROM pharmacy_inventory
                WHERE status IN ('low', 'out')
            """).fetchone()
            crit_compliance = conn.execute(f"""
                SELECT COUNT(*) as cnt FROM compliance_reviews
                WHERE risk_level = 'critical'
                  AND created_at >= {date_filter}
            """).fetchone()
            pending_msgs = conn.execute("""
                SELECT COUNT(*) as cnt FROM patient_messages
                WHERE sent = 0 AND role = 'user'
            """).fetchone()
            low_perf = conn.execute(f"""
                SELECT COUNT(DISTINCT campaign_id) as cnt FROM content_metrics
                WHERE engagement_rate < 0.01
                  AND date >= date('now', '-7 days')
            """).fetchone()
        else:
            low_inv = conn.execute("""
                SELECT COUNT(*) as cnt FROM pharmacy_inventory
                WHERE status IN ('low', 'out')
            """).fetchone()
            crit_compliance = conn.execute(f"""
                SELECT COUNT(*) as cnt FROM compliance_reviews
                WHERE risk_level = 'critical'
                  AND created_at >= {date_filter}
            """).fetchone()
            pending_msgs = conn.execute("""
                SELECT COUNT(*) as cnt FROM patient_messages
                WHERE sent = 0 AND role = 'user'
            """).fetchone()
            low_perf = conn.execute(f"""
                SELECT COUNT(DISTINCT campaign_id) as cnt FROM content_metrics
                WHERE engagement_rate < 0.01
                  AND date >= DATE_SUB(NOW(), INTERVAL 7 DAY)
            """).fetchone()

        if low_inv and low_inv[0] >= 1:
            triggered.append({"trigger": "low_inventory_alert", "name": TRIGGERS["low_inventory_alert"]["name"],
                              "count": low_inv[0], "severity": "high", "message": f"{low_inv[0]} 个品种库存不足"})
            alerts.append({"type": "low_inventory", "severity": "high", "count": low_inv[0], "action": "建议立即启动补货"})

        if crit_compliance and crit_compliance[0] >= 1:
            triggered.append({"trigger": "compliance_violation", "name": TRIGGERS["compliance_violation"]["name"],
                              "count": crit_compliance[0], "severity": "critical",
                              "message": f"近7天 {crit_compliance[0]} 条严重合规告警"})
            alerts.append({"type": "compliance", "severity": "critical", "count": crit_compliance[0],
                           "action": "立即处理合规违规内容"})

        if pending_msgs and pending_msgs[0] >= 3:
            triggered.append({"trigger": "high_risk_patient", "name": TRIGGERS["high_risk_patient"]["name"],
                              "count": pending_msgs[0], "severity": "high", "message": f"{pending_msgs[0]} 条患者消息待回复"})
            alerts.append({"type": "patient", "severity": "high", "count": pending_msgs[0],
                           "action": "优先回复高风险患者消息"})

        if low_perf and low_perf[0] >= 3:
            triggered.append({"trigger": "content_low_performance", "name": TRIGGERS["content_low_performance"]["name"],
                              "count": low_perf[0], "severity": "medium",
                              "message": f"{low_perf[0]} 个内容活动互动率低于1%"})
            alerts.append({"type": "content", "severity": "medium", "count": low_perf[0],
                           "action": "优化低互动率内容标题和发布时间"})

        # 6. 异常检测（委托 smart_analytics，不重复实现）
        try:
            import smart_analytics
            scan = smart_analytics.full_anomaly_scan(period_days=7, threshold=2.0)
            for anomaly in scan.get("content_anomalies", [])[:3]:
                if anomaly.get("severity") in ("critical", "high"):
                    triggered.append({"trigger": "content_anomaly", "name": "内容异常波动",
                                      "count": 1, "severity": anomaly["severity"],
                                      "message": f"内容异常：{anomaly.get('suggestion', anomaly.get('type'))}"})
                    alerts.append({"type": "content_anomaly", "severity": anomaly["severity"],
                                   "count": 1, "action": anomaly.get("suggestion", "")})
            for anomaly in scan.get("patient_anomalies", [])[:3]:
                if anomaly.get("severity") in ("critical", "high"):
                    triggered.append({"trigger": "patient_anomaly", "name": "患者活跃度异常",
                                      "count": 1, "severity": anomaly["severity"],
                                      "message": f"患者异常：{anomaly.get('suggestion', anomaly.get('type'))}"})
                    alerts.append({"type": "patient_anomaly", "severity": anomaly["severity"],
                                   "count": 1, "action": anomaly.get("suggestion", "")})
            for anomaly in scan.get("inventory_anomalies", [])[:3]:
                if anomaly.get("severity") in ("critical", "high"):
                    triggered.append({"trigger": "inventory_anomaly", "name": "库存异常",
                                      "count": 1, "severity": anomaly["severity"],
                                      "message": f"库存异常：{anomaly.get('suggestion', anomaly.get('type'))}"})
                    alerts.append({"type": "inventory_anomaly", "severity": anomaly["severity"],
                                   "count": 1, "action": anomaly.get("suggestion", "")})
        except Exception:
            pass  # smart_analytics 不可用时降级

        _update_trigger_history(conn, triggered)

        return {
            "checked_at": datetime.now().isoformat(),
            "triggered_count": len(triggered),
            "alerts": alerts,
            "triggered": triggered,
            "severity_summary": {
                "critical": len([a for a in alerts if a["severity"] == "critical"]),
                "high": len([a for a in alerts if a["severity"] == "high"]),
                "medium": len([a for a in alerts if a["severity"] == "medium"]),
            },
            "overall_status": ("critical" if any(a["severity"] == "critical" for a in alerts)
                              else "warning" if any(a["severity"] == "high" for a in alerts)
                              else "ok"),
        }
    finally:
        close_conn(conn)


def _update_trigger_history(conn, triggered: list, is_sqlite: bool = False):
    """更新触发历史"""
    now = datetime.now().isoformat()
    for t in triggered:
        trigger_name = t.get("trigger", "")
        try:
            if is_sqlite:
                conn.execute("""
                    INSERT INTO trigger_history (trigger_name, last_triggered_at, trigger_count, is_active)
                    VALUES (?, ?, 1, 1)
                    ON CONFLICT(trigger_name) DO UPDATE SET
                        last_triggered_at = excluded.last_triggered_at,
                        trigger_count = trigger_count + 1,
                        is_active = 1
                """, (trigger_name, now))
            else:
                conn.execute("""
                    INSERT INTO trigger_history (trigger_name, last_triggered_at, trigger_count, is_active)
                    VALUES (%s, %s, 1, 1)
                    ON DUPLICATE KEY UPDATE
                        last_triggered_at = VALUES(last_triggered_at),
                        trigger_count = trigger_count + 1,
                        is_active = 1
                """, (trigger_name, now))
        except Exception:
            pass
    conn.commit()


def list_triggers() -> dict:
    """列出所有触发器"""
    return {
        "triggers": [
            {
                "name": name,
                "description": t.get("name", ""),
                "type": t.get("type", ""),
                "severity": t.get("severity", "medium"),
                "condition": t.get("condition", ""),
            }
            for name, t in TRIGGERS.items()
        ]
    }


def get_trigger_history(conn, trigger_name: str = None, limit: int = 20) -> list:
    """获取触发历史"""
    query = "SELECT * FROM trigger_history"
    params = []
    if trigger_name:
        query += " WHERE trigger_name = ?"
        params.append(trigger_name)
    query += " ORDER BY last_triggered_at DESC LIMIT ?"
    params.append(limit)

    rows = conn.execute(query, params).fetchall()
    cols = [d[0] for d in conn.execute("SELECT * FROM trigger_history LIMIT 0").description]
    return [dict(zip(cols, r)) for r in rows]


def fire_trigger(trigger_name: str, params: dict = None) -> dict:
    """手动触发一个触发器"""
    trigger = TRIGGERS.get(trigger_name)
    if not trigger:
        return {"error": f"Trigger '{trigger_name}' not found", "available": list(TRIGGERS.keys())}

    conn, is_sqlite = _get_conn()

    try:
        _update_trigger_history(conn, [{
            "trigger": trigger_name,
            "name": trigger.get("name", ""),
            "count": 1,
            "severity": trigger.get("severity", "medium"),
            "message": f"手动触发: {trigger.get('name', '')}",
        }])

        result = check_all_triggers()
        triggered = [t for t in result.get("triggered", []) if t.get("trigger") == trigger_name]

        return {
            "trigger": trigger_name,
            "name": trigger.get("name", ""),
            "fired": len(triggered) > 0,
            "details": triggered[0] if triggered else None,
            "params": params or {},
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
    action = args.get("action", "check")
    trigger_name = args.get("trigger_name")
    params = args.get("params", {})

    if action == "check":
        result = check_all_triggers()
    elif action == "list":
        result = list_triggers()
    elif action == "trigger":
        result = fire_trigger(trigger_name, params) if trigger_name else {"error": "trigger_name required"}
    elif action == "history":
        conn, is_sqlite = _get_conn()
        result = {"history": get_trigger_history(conn, trigger_name)}
        close_conn(conn)
    else:
        result = {"error": f"Unknown action: {action}"}

    print(json.dumps(result, ensure_ascii=False, indent=2))
