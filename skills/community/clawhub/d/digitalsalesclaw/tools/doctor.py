#!/usr/bin/env python3
"""
DigitalSalesClaw - doctor.py
医生触达与KOL管理工具

输入: {"action": "list|visits|plan|kol_list", "doctor_id": "...", "hospital": "..."}
输出: {"doctors, visits, kols, ...}
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent


def list_doctors(conn, hospital: str = None, specialty: str = None, limit: int = 50) -> dict:
    """医生列表"""
    query = "SELECT * FROM doctor_profiles WHERE 1=1"
    params = []
    if hospital:
        query += " AND hospital LIKE ?"
        params.append(f"%{hospital}%")
    if specialty:
        query += " AND specialty LIKE ?"
        params.append(f"%{specialty}%")
    query += " ORDER BY influence_score DESC LIMIT ?"
    params.append(limit)

    rows = conn.execute(query, params).fetchall()
    cols = [d[0] for d in conn.execute("SELECT * FROM doctor_profiles LIMIT 0").description]
    doctors = [dict(zip(cols, r)) for r in rows]

    # 分级统计
    high_influence = [d for d in doctors if d.get("influence_score", 0) >= 8]
    medium_influence = [d for d in doctors if 5 <= d.get("influence_score", 0) < 8]
    low_influence = [d for d in doctors if d.get("influence_score", 0) < 5]

    return {
        "total_count": len(doctors),
        "influence_distribution": {
            "high": len(high_influence),
            "medium": len(medium_influence),
            "low": len(low_influence),
        },
        "top_doctors": doctors[:10],
        "suggestions": [
            f"管理 {len(doctors)} 位医生",
            f"高影响力医生 {len(high_influence)} 位",
            "建议优先维护高影响力医生关系"
        ]
    }


def get_visits(conn, doctor_id: str = None, limit: int = 20) -> dict:
    """拜访记录"""
    query = """
        SELECT dv.*, dp.name as doctor_name, dp.hospital, dp.department
        FROM doctor_visits dv
        LEFT JOIN doctor_profiles dp ON dp.doctor_id = dv.doctor_id
        WHERE 1=1
    """
    params = []
    if doctor_id:
        query += " AND dv.doctor_id = ?"
        params.append(doctor_id)
    query += " ORDER BY dv.created_at DESC LIMIT ?"
    params.append(limit)

    rows = conn.execute(query, params).fetchall()
    cols = [d[0] for d in conn.execute("SELECT * FROM doctor_visits LIMIT 0").description]
    visits = [dict(zip(cols, r)) for r in rows]

    # 按类型分组
    by_type = {}
    for v in visits:
        t = v.get("visit_type", "unknown")
        by_type[t] = by_type.get(t, 0) + 1

    return {
        "total_visits": len(visits),
        "by_visit_type": by_type,
        "recent_visits": visits[:10],
        "suggestions": [
            f"共 {len(visits)} 次拜访记录",
            f"拜访类型分布：{by_type}",
            "建议保持规律拜访节奏"
        ]
    }


def generate_outreach_plan(conn, doctor_id: str = None, rep_id: str = None) -> dict:
    """生成拜访计划"""
    doctors = []
    if doctor_id:
        d = conn.execute("SELECT * FROM doctor_profiles WHERE doctor_id = ?", (doctor_id,)).fetchone()
        if d:
            cols = [desc[0] for desc in conn.execute("SELECT * FROM doctor_profiles LIMIT 0").description]
            doctors.append(dict(zip(cols, d)))
    else:
        rows = conn.execute("""
            SELECT * FROM doctor_profiles
            ORDER BY influence_score DESC, compliance_score ASC
            LIMIT 20
        """).fetchall()
        cols = [desc[0] for desc in conn.execute("SELECT * FROM doctor_profiles LIMIT 0").description]
        doctors = [dict(zip(cols, r)) for r in rows]

    plan = []
    for d in doctors:
        influence = d.get("influence_score", 5)
        compliance = d.get("compliance_score", 5)

        # 优先级：高影响力 + 低合规得分 = 高优先级
        priority_score = influence * 0.7 + (10 - compliance) * 0.3
        priority = "high" if priority_score >= 8 else "medium" if priority_score >= 5 else "low"

        # 建议拜访频率
        if priority == "high":
            freq = "每周1次"
            next_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        elif priority == "medium":
            freq = "每两周1次"
            next_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        else:
            freq = "每月1次"
            next_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

        plan.append({
            "doctor_id": d.get("doctor_id"),
            "doctor_name": d.get("name"),
            "hospital": d.get("hospital"),
            "department": d.get("department"),
            "influence_score": influence,
            "priority": priority,
            "suggested_frequency": freq,
            "next_visit_date": next_date,
            "suggested_topics": ["学术内容推送", "产品信息更新", "患者案例分享"]
        })

    plan.sort(key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x["priority"], 3))

    return {
        "plan_count": len(plan),
        "high_priority_count": len([p for p in plan if p["priority"] == "high"]),
        "outreach_plan": plan[:15],
        "suggestions": [
            f"生成了 {len(plan)} 位医生的拜访计划",
            f"高优先级 {len([p for p in plan if p['priority']=='high'])} 位",
            "建议本周内完成高优先级拜访"
        ]
    }


def list_kols(conn, platform: str = None, limit: int = 50) -> dict:
    """KOL列表"""
    query = "SELECT * FROM kol_profiles WHERE status = 'active'"
    params = []
    if platform:
        query += " AND platform = ?"
        params.append(platform)
    query += " ORDER BY fans_count DESC LIMIT ?"
    params.append(limit)

    rows = conn.execute(query, params).fetchall()
    cols = [d[0] for d in conn.execute("SELECT * FROM kol_profiles LIMIT 0").description]
    kols = [dict(zip(cols, r)) for r in rows]

    # 分级
    top_kols = [k for k in kols if k.get("fans_count", 0) >= 100000]
    mid_kols = [k for k in kols if 10000 <= k.get("fans_count", 0) < 100000]
    nano_kols = [k for k in kols if k.get("fans_count", 0) < 10000]

    contracts = conn.execute("""
        SELECT COUNT(*) FROM kol_contracts WHERE status = 'active'
    """).fetchone()[0]

    return {
        "total_kols": len(kols),
        "tier_distribution": {
            "top": len(top_kols),
            "mid": len(mid_kols),
            "nano": len(nano_kols),
        },
        "active_contracts": contracts,
        "top_kols": kols[:10],
        "suggestions": [
            f"活跃KOL {len(kols)} 位",
            f"头部 {len(top_kols)}，腰部 {len(mid_kols)}，尾部 {len(nano_kols)}",
            f"当前 {contracts} 个活跃合作"
        ]
    }


def _parse_args():
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError:
            return {"action": "list"}
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
    action = args.get("action", "list")
    doctor_id = args.get("doctor_id")
    hospital = args.get("hospital")
    specialty = args.get("specialty")
    platform = args.get("platform")

    conn = get_conn()
    
    try:
        if action == "list":
            result = list_doctors(conn, hospital, specialty)
        elif action == "visits":
            result = get_visits(conn, doctor_id)
        elif action == "plan":
            result = generate_outreach_plan(conn, doctor_id)
        elif action == "kol_list":
            result = list_kols(conn, platform)
        else:
            result = {"error": f"Unknown action: {action}"}
    finally:
        close_conn(conn)

    print(json.dumps(result, ensure_ascii=False, indent=2))
