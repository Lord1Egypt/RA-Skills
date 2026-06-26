#!/usr/bin/env python3
"""
DigitalSalesClaw - patient_segmentation.py
患者智能分群引擎
基于行为数据 + 风险评估 + 互动强度 多维度分群

输入: {"action": "segment|trends|interventions", "segment": "all|high_risk|medium_risk|low_risk"}
输出: {"segments: [{name, count, patients, characteristics}], ...}
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent


def get_patient_sessions(conn) -> list[dict]:
    """获取所有患者会话"""
    rows = conn.execute("""
        SELECT ps.*,
               (SELECT COUNT(*) FROM patient_messages pm WHERE pm.session_id = ps.session_id) as message_count,
               (SELECT COUNT(*) FROM patient_messages pm WHERE pm.session_id = ps.session_id AND pm.sent = 0) as pending_count,
               (SELECT MAX(created_at) FROM patient_messages pm WHERE pm.session_id = ps.session_id) as last_message_at
        FROM patient_sessions ps
        ORDER BY ps.created_at DESC
    """).fetchall()

    cols = [d[0] for d in conn.execute("SELECT * FROM patient_sessions LIMIT 0").description]
    sessions = [dict(zip(cols, r)) for r in rows]

    # message_count and pending_count already included in SQL query result

    return sessions


def get_patient_messages(conn, session_id: str) -> list[dict]:
    """获取患者消息"""
    rows = conn.execute("""
        SELECT * FROM patient_messages
        WHERE session_id = ?
        ORDER BY created_at ASC
    """, (session_id,)).fetchall()

    cols = [d[0] for d in conn.execute("SELECT * FROM patient_messages LIMIT 0").description]
    return [dict(zip(cols, r)) for r in rows]


def get_patient_touchpoints(conn, patient_id: str) -> list[dict]:
    """获取患者触点"""
    rows = conn.execute("""
        SELECT * FROM patient_touchpoints
        WHERE patient_id = ?
        ORDER BY timestamp DESC
    """, (patient_id,)).fetchall()

    cols = [d[0] for d in conn.execute("SELECT * FROM patient_touchpoints LIMIT 0").description]
    return [dict(zip(cols, r)) for r in rows]


def get_conversion_events(conn, patient_id: str = None) -> list[dict]:
    """获取转化事件"""
    query = "SELECT * FROM conversion_events WHERE 1=1"
    params = []
    if patient_id:
        query += " AND patient_id = ?"
        params.append(patient_id)
    query += " ORDER BY timestamp DESC"

    rows = conn.execute(query, params).fetchall()
    cols = [d[0] for d in conn.execute("SELECT * FROM conversion_events LIMIT 0").description]
    return [dict(zip(cols, r)) for r in rows]


def calculate_risk_score(session: dict, messages: list[dict], touchpoints: list[dict]) -> dict:
    """计算患者风险评分"""
    score = 50  # 基础分
    factors = []
    risk_level = "medium"

    # 消息数量分析
    msg_count = len(messages)
    if msg_count >= 20:
        score -= 10
        factors.append("消息量大（可能有问题未解决）")
    elif msg_count <= 2:
        score += 5
        factors.append("新患者，暂无风险")

    # 待回复消息
    pending = sum(1 for m in messages if not m.get("sent") and m.get("role") == "user")
    if pending >= 3:
        score -= 15
        factors.append(f"待回复消息 {pending} 条")
    elif pending >= 1:
        score -= 5

    # 情感分析
    sentiments = defaultdict(int)
    for m in messages:
        s = m.get("sentiment", "neutral")
        sentiments[s] += 1

    if sentiments.get("negative", 0) >= 3:
        score -= 15
        factors.append("多次负面情感表达")
    elif sentiments.get("negative", 0) >= 1:
        score -= 5

    # 会话时长
    created = session.get("created_at", "")
    if created:
        try:
            created_dt = datetime.strptime(created[:19], "%Y-%m-%d %H:%M:%S")
            hours_old = (datetime.now() - created_dt).total_seconds() / 3600
            if hours_old > 72 and pending > 0:
                score -= 10
                factors.append(f"超过72小时未回复")
        except Exception:
            pass

    # 触点数量（太少可能依从性差）
    if len(touchpoints) < 2:
        score -= 5
        factors.append("触点稀少，依从性可能较差")

    # 状态
    if session.get("status") == "pending":
        score -= 5

    # 判定风险等级
    if score >= 70:
        risk_level = "low"
    elif score >= 40:
        risk_level = "medium"
    else:
        risk_level = "high"

    return {
        "risk_score": max(0, min(100, score)),
        "risk_level": risk_level,
        "factors": factors,
        "message_count": msg_count,
        "pending_count": pending,
        "sentiment_distribution": dict(sentiments),
    }


def segment_patients(conn) -> dict:
    """患者分群"""
    sessions = get_patient_sessions(conn)

    segments = {
        "high_risk": [],
        "medium_risk": [],
        "low_risk": [],
    }

    for session in sessions:
        session_id = session.get("session_id", "")
        messages = get_patient_messages(conn, session_id)
        touchpoints = get_patient_touchpoints(conn, session.get("patient_id", ""))

        risk = calculate_risk_score(session, messages, touchpoints)
        session["risk"] = risk

        risk_lv = risk["risk_level"]
        key = {"high": "high_risk", "medium": "medium_risk", "low": "low_risk"}.get(risk_lv, "medium_risk")
        segments[key].append(session)

    # 统计
    segment_stats = {
        name: {
            "count": len(items),
            "pct": round(len(items) / max(len(sessions), 1) * 100, 1),
        }
        for name, items in segments.items()
    }

    # 各分群特征
    characteristics = {
        "high_risk": {
            "name": "高风险",
            "description": "依从性差、情绪负面、待回复多、需要优先干预",
            "recommended_action": "优先电话/视频随访，48小时内必须接触",
        },
        "medium_risk": {
            "name": "中风险",
            "description": "有部分风险因素、需要关注",
            "recommended_action": "定期微信跟进，一周内接触",
        },
        "low_risk": {
            "name": "低风险",
            "description": "状态稳定，依从性好",
            "recommended_action": "常规维护，自动消息即可",
        },
    }

    # 高风险患者详情
    high_risk_detail = []
    for s in segments["high_risk"][:10]:
        risk = s.get("risk", {})
        high_risk_detail.append({
            "session_id": s.get("session_id"),
            "patient_name": s.get("patient_name"),
            "status": s.get("status"),
            "risk_score": risk.get("risk_score"),
            "pending_count": risk.get("pending_count"),
            "factors": risk.get("factors", []),
        })

    return {
        "total_patients": len(sessions),
        "segments": segment_stats,
        "characteristics": characteristics,
        "high_risk_patients": high_risk_detail,
        "suggestions": [
            f"高风险 {len(segments['high_risk'])} 人需立即干预",
            f"中风险 {len(segments['medium_risk'])} 人需持续关注",
            f"低风险 {len(segments['low_risk'])} 人可常规维护",
        ]
    }


def get_segment_trends(conn, period_days: int = 30) -> dict:
    """分群趋势分析"""
    rows = conn.execute(f"""
        SELECT
            DATE(created_at) as date,
            COUNT(*) as total,
            SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active,
            SUM(CASE WHEN status = 'resolved' THEN 1 ELSE 0 END) as resolved
        FROM patient_sessions
        WHERE created_at >= datetime('now', '-{period_days} days')
        GROUP BY DATE(created_at)
        ORDER BY date ASC
    """).fetchall()

    trend = [{"date": r[0], "total": r[1], "active": r[2], "resolved": r[3]} for r in rows]

    # 计算平均值
    if trend:
        avg_active = sum(t["active"] for t in trend) / len(trend)
        avg_resolved = sum(t["resolved"] for t in trend) / len(trend)
    else:
        avg_active = avg_resolved = 0

    return {
        "period_days": period_days,
        "trend": trend,
        "avg_active_daily": round(avg_active, 1),
        "avg_resolved_daily": round(avg_resolved, 1),
    }


def generate_intervention_plan(conn, patient_id: str = None, session_id: str = None) -> dict:
    """生成干预计划"""
    if session_id:
        session = conn.execute("SELECT * FROM patient_sessions WHERE session_id = ?", (session_id,)).fetchone()
    elif patient_id:
        session = conn.execute("SELECT * FROM patient_sessions WHERE patient_id = ?", (patient_id,)).fetchone()
    else:
        return {"error": "patient_id or session_id required"}

    if not session:
        return {"error": "Patient not found"}

    cols = [d[0] for d in conn.execute("SELECT * FROM patient_sessions LIMIT 0").description]
    session_data = dict(zip(cols, session))

    session_id_val = session_data.get("session_id", "")
    messages = get_patient_messages(conn, session_id_val)
    touchpoints = get_patient_touchpoints(conn, session_data.get("patient_id", ""))

    risk = calculate_risk_score(session_data, messages, touchpoints)

    # 根据风险等级生成干预计划
    if risk["risk_level"] == "high":
        plan = [
            {"day": 0, "action": "立即电话联系", "priority": "critical", "method": "电话"},
            {"day": 0, "action": "确认未回复原因", "priority": "critical", "method": "电话"},
            {"day": 1, "action": "发送关怀消息+用药提醒", "priority": "high", "method": "微信/短信"},
            {"day": 3, "action": "复诊提醒", "priority": "high", "method": "短信"},
            {"day": 7, "action": "一周随访评估", "priority": "medium", "method": "电话"},
        ]
    elif risk["risk_level"] == "medium":
        plan = [
            {"day": 0, "action": "发送消息确认状态", "priority": "high", "method": "微信"},
            {"day": 3, "action": "跟进回复情况", "priority": "medium", "method": "微信"},
            {"day": 7, "action": "定期关怀", "priority": "low", "method": "自动消息"},
        ]
    else:
        plan = [
            {"day": 7, "action": "定期健康提醒", "priority": "low", "method": "自动消息"},
            {"day": 30, "action": "月度回访", "priority": "low", "method": "自动消息"},
        ]

    return {
        "patient_name": session_data.get("patient_name"),
        "session_id": session_id_val,
        "risk_level": risk["risk_level"],
        "risk_score": risk["risk_score"],
        "risk_factors": risk.get("factors", []),
        "intervention_plan": plan,
        "suggestions": [f"优先处理{risk['risk_level']}风险患者"]
    }


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
    action = args.get("action", "segment")
    segment = args.get("segment", "all")
    patient_id = args.get("patient_id")
    session_id = args.get("session_id")
    period_days = args.get("period_days", 30)

    conn = get_conn()
    
    try:
        if action == "segment":
            result = segment_patients(conn)
        elif action == "trends":
            result = get_segment_trends(conn, period_days)
        elif action == "interventions":
            result = generate_intervention_plan(conn, patient_id, session_id)
        else:
            result = {"error": f"Unknown action: {action}"}
    finally:
        close_conn(conn)

    print(json.dumps(result, ensure_ascii=False, indent=2))
