#!/usr/bin/env python3
"""
DigitalSalesClaw - patient.py
患者全病程管理工具
"""
import sys
import json
from datetime import datetime


def json_dumps(obj, ensure_ascii=False, indent=2, default=None):
    """JSON serialize with datetime support."""
    def dt_default(o):
        if isinstance(o, datetime):
            return o.isoformat()
        if default:
            return default(o)
        raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")
    return json.dumps(obj, ensure_ascii=ensure_ascii, indent=indent, default=dt_default)
from db import query_all, query_one, execute


def list_segments() -> dict:
    sessions = query_all("""
        SELECT session_id, patient_name, patient_id, status, segment, created_at
        FROM patient_sessions ORDER BY created_at DESC LIMIT 200
    """)
    segments = {"active": [], "resolved": [], "pending": []}
    high_risk, medium_risk, low_risk = [], [], []
    for s in sessions:
        sid = s.get("session_id", "")
        r = query_one("SELECT COUNT(*) as c FROM patient_messages WHERE session_id = %s", (sid,))
        msg_count = r["c"] if r else 0
        r = query_one("SELECT COUNT(*) as c FROM patient_messages WHERE session_id = %s AND sent = 0", (sid,))
        unread = r["c"] if r else 0
        enriched = {**s, "message_count": msg_count, "unread_count": unread}
        st = s.get("status", "")
        if st == "active": segments["active"].append(enriched)
        elif st == "resolved": segments["resolved"].append(enriched)
        else: segments["pending"].append(enriched)
        seg = s.get("segment", "")
        if "high" in seg.lower(): high_risk.append(enriched)
        elif "medium" in seg.lower(): medium_risk.append(enriched)
        else: low_risk.append(enriched)
    return {
        "segments": segments, "high_risk": high_risk, "medium_risk": medium_risk,
        "low_risk": low_risk, "total": len(sessions),
        "active_count": len(segments["active"]),
        "risk_distribution": {"high_risk": len(high_risk), "medium_risk": len(medium_risk), "low_risk": len(low_risk)},
        "high_risk_patients": high_risk[:10],
        "suggestions": [f"高风险患者 {len(high_risk)} 人需优先处理", f"当前活跃会话 {len(segments['active'])} 个"]
    }


def get_session_summary(session_id: str) -> dict:
    session = query_one("SELECT * FROM patient_sessions WHERE session_id = %s", (session_id,))
    if not session:
        return {"error": f"Session {session_id} not found"}
    messages = query_all("SELECT role, content, sent, created_at FROM patient_messages WHERE session_id = %s ORDER BY created_at ASC", (session_id,))
    tickets = query_all("SELECT id, ticket_type, priority, status, created_at FROM patient_tickets WHERE session_id = %s ORDER BY created_at DESC", (session_id,))
    pending = [m for m in messages if m.get("role") == "user" and not m.get("sent")]
    last_msg = messages[-1] if messages else None
    last_age = None
    if last_msg and last_msg.get("created_at"):
        try:
            lm = last_msg["created_at"]
            if isinstance(lm, str): lm = datetime.fromisoformat(lm)
            last_age = (datetime.now() - lm.replace(tzinfo=None)).days
        except: pass
    return {
        "session": session, "message_count": len(messages), "pending_replies": len(pending),
        "last_message_age_days": last_age, "tickets": tickets,
        "recent_messages": messages[-5:],
        "suggestions": [f"共 {len(messages)} 条消息", f"待回复 {len(pending)} 条", f"最后消息 {last_age} 天前" if last_age else "暂无消息"]
    }


def create_ticket(session_id: str, patient_id: str = None, issue: str = None, priority: str = "normal", assigned_to: str = None) -> dict:
    try:
        if assigned_to:
            execute("INSERT INTO patient_tickets (session_id, ticket_type, priority, status, assigned_to) VALUES (%s, %s, %s, %s, %s)",
                (session_id, issue or "待跟进", priority, "open", assigned_to))
        else:
            execute("INSERT INTO patient_tickets (session_id, ticket_type, priority, status) VALUES (%s, %s, %s, %s)",
                (session_id, issue or "待跟进", priority, "open"))
        return {"status": "created", "session_id": session_id, "priority": priority, "assigned_to": assigned_to}
    except Exception as ex:
        return {"error": str(ex)}


def create_sop(segment: str) -> dict:
    sop = {
        "high_risk": [{"day": 1, "action": "发送随访消息", "channel": "自动"}, {"day": 3, "action": "未回复则提醒", "channel": "自动"}, {"day": 7, "action": "转人工跟进", "channel": "人工"}],
        "medium_risk": [{"day": 7, "action": "发送健康教育", "channel": "自动"}, {"day": 14, "action": "复诊提醒", "channel": "自动"}],
        "low_risk": [{"day": 14, "action": "发送健康资讯", "channel": "自动"}]
    }
    return {"segment": segment, "sop": sop.get(segment, sop["low_risk"]), "status": "ready"}


def add_followup(session_id: str, content: str, followup_type: str = "call") -> dict:
    try:
        execute("INSERT INTO patient_messages (session_id, role, content, sent, created_at) VALUES (%s, %s, %s, 1, %s)",
            (session_id, "assistant", content, datetime.now().isoformat()))
        return {"status": "added", "session_id": session_id}
    except Exception as ex:
        return {"error": str(ex)}


def patient(action: str, session_id: str = None, patient_id: str = None,
            segment: str = None, issue: str = None, priority: str = None,
            content: str = None, followup_type: str = None, assigned_to: str = None) -> dict:
    try:
        if action == "list_segments": return list_segments()
        elif action == "session_summary": return get_session_summary(session_id or "")
        elif action == "create_ticket": return create_ticket(session_id or "", patient_id, issue, priority or "normal", assigned_to)
        elif action == "create_sop": return create_sop(segment or "medium_risk")
        elif action == "add_followup": return add_followup(session_id or "", content or "", followup_type or "call")
        return {"error": f"Unknown action: {action}"}
    except Exception as e:
        return {"error": str(e)}


def _parse_args():
    if len(sys.argv) > 1:
        try: return json.loads(sys.argv[1])
        except: return {"action": sys.argv[1]}
    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data:
            try: return json.loads(data)
            except: return {"action": data}
    return {}


if __name__ == "__main__":
    args = _parse_args()
    print(json_dumps(patient(
        action=args.get("action", ""),
        session_id=args.get("session_id"),
        patient_id=args.get("patient_id"),
        segment=args.get("segment"),
        issue=args.get("issue"),
        priority=args.get("priority"),
        content=args.get("content"),
        followup_type=args.get("followup_type"),
    ), ensure_ascii=False, indent=2))
