#!/usr/bin/env python3
"""
DigitalSalesClaw - kol_matching.py
KOL智能匹配引擎
基于内容类型 + 目标受众 + 平台特性 + KOL画像 智能匹配

输入: {"action": "match|list|analyze", "content_type": "...", "target_audience": "...", "platform": "...", "budget": 50000}
输出: {"matched_kols: [{kol, score, reason, estimated_reach}], ...}
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent


# KOL分级标准
KOL_TIERS = {
    "top": {"min_fans": 100000, "description": "头部KOL", "weight": 1.0},
    "mid": {"min_fans": 10000, "description": "腰部KOL", "weight": 0.7},
    "nano": {"min_fans": 1000, "description": "尾部KOL", "weight": 0.4},
}

# 内容类型 → 适合的KOL类型
CONTENT_KOL_MAP = {
    "科普": ["medical_expert", "health_blogger"],
    "用药指导": ["pharmacist", "doctor"],
    "患者故事": ["patient_influencer", "health_blogger"],
    "产品评测": ["product_reviewer", "lifestyle_influencer"],
    "健康生活": ["lifestyle_influencer", "fitness_influencer"],
    "医生学术": ["medical_expert", "doctor"],
}

# 平台特点
PLATFORM_TIERS = {
    "douyin": ["video", "live"],
    "xiaohongshu": ["note", "video"],
    "wechat": ["article"],
    "weibo": ["post", "article"],
}


def list_kols(conn, platform: str = None, tier: str = None, limit: int = 50) -> list[dict]:
    """获取KOL列表"""
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

    if tier:
        tier_config = KOL_TIERS.get(tier, {})
        min_fans = tier_config.get("min_fans", 0)
        kols = [k for k in kols if k.get("fans_count", 0) >= min_fans]

    return kols


def calculate_match_score(kol: dict, content_type: str, target_audience: str, platform: str) -> dict:
    """计算单个KOL的匹配度"""
    score = 50  # 基础分
    reasons = []

    fans = kol.get("fans_count", 0)

    # 粉丝数量评分
    if fans >= 100000:
        score += 15
        reasons.append(f"头部KOL，粉丝{fans:,}")
    elif fans >= 10000:
        score += 10
        reasons.append(f"腰部KOL，粉丝{fans:,}")
    elif fans >= 1000:
        score += 5
        reasons.append(f"尾部KOL，粉丝{fans:,}")

    # 平台匹配
    kol_platform = kol.get("platform", "")
    if kol_platform == platform:
        score += 10
        reasons.append(f"主要平台匹配（{platform}）")
    else:
        score -= 5

    # 合作率
    coop_rate = kol.get("cooperation_rate", 0.5)
    score += coop_rate * 10
    reasons.append(f"合作率 {coop_rate:.0%}")

    # 标签匹配
    kol_tags = kol.get("tags", "") or ""
    kol_category = kol.get("category", "") or ""

    if content_type in ["科普", "用药指导", "医生学术"]:
        if any(kw in kol_tags or kw in kol_category for kw in ["医学", "健康", "科普", "医药", "医生"]):
            score += 15
            reasons.append("医药健康领域专业KOL")
    elif content_type in ["患者故事", "健康生活"]:
        if any(kw in kol_tags or kw in kol_category for kw in ["生活", "健康", "养生", "患者"]):
            score += 12
            reasons.append("生活健康类KOL")

    # 估算触达
    estimated_reach = int(fans * 0.1 * coop_rate)  # 假设10%触达率 * 合作率

    return {
        "kol_id": kol.get("kol_id"),
        "username": kol.get("username"),
        "platform": kol_platform,
        "fans_count": fans,
        "level": kol.get("level"),
        "category": kol_category,
        "tags": kol_tags,
        "cooperation_rate": coop_rate,
        "match_score": min(100, max(0, score)),
        "reasons": reasons,
        "estimated_reach": estimated_reach,
    }


def match_kols(content_type: str = None, target_audience: str = None,
               platform: str = None, budget: float = None, limit: int = 10) -> dict:
    """匹配KOL"""
    conn = get_conn()
    
    try:
        # 获取KOL列表
        kols = list_kols(conn, platform)

        if not kols:
            return {"error": "No KOLs found", "matched_count": 0}

        # 计算匹配分
        scored_kols = []
        for kol in kols:
            score_result = calculate_match_score(kol, content_type or "", target_audience or "", platform or "douyin")
            score_result["match_score"] = min(100, max(0, score_result["match_score"]))
            scored_kols.append(score_result)

        # 排序
        scored_kols.sort(key=lambda x: -x["match_score"])

        # 按预算分组推荐
        total_estimated = 0
        selected = []
        remaining_budget = budget

        for kol in scored_kols:
            # 估算合作费用（按粉丝量级）
            fans = kol["fans_count"]
            if fans >= 100000:
                estimated_cost = 50000
            elif fans >= 50000:
                estimated_cost = 20000
            elif fans >= 10000:
                estimated_cost = 5000
            else:
                estimated_cost = 1000

            kol["estimated_cost"] = estimated_cost

            if budget is None or remaining_budget >= estimated_cost:
                selected.append(kol)
                if budget is not None:
                    remaining_budget -= estimated_cost

            if len(selected) >= limit:
                break

        # 估算总触达
        total_reach = sum(k["estimated_reach"] for k in selected)

        return {
            "content_type": content_type,
            "target_audience": target_audience,
            "platform": platform,
            "budget": budget,
            "budget_remaining": remaining_budget if budget else None,
            "matched_count": len(selected),
            "total_estimated_reach": total_reach,
            "matched_kols": selected,
            "all_scored_count": len(scored_kols),
        }
    finally:
        close_conn(conn)


def analyze_kol_performance(kol_id: str = None, conn=None) -> dict:
    """分析KOL历史表现"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        # 获取KOL信息
        kol = conn.execute("SELECT * FROM kol_profiles WHERE kol_id = ?", (kol_id,)).fetchone()
        if not kol:
            return {"error": f"KOL {kol_id} not found"}

        cols = [d[0] for d in conn.execute("SELECT * FROM kol_profiles LIMIT 0").description]
        kol_data = dict(zip(cols, kol))

        # 获取历史合同
        contracts = conn.execute("""
            SELECT * FROM kol_contracts WHERE kol_id = ? ORDER BY created_at DESC LIMIT 10
        """, (kol_id,)).fetchall()

        c_cols = [d[0] for d in conn.execute("SELECT * FROM kol_contracts LIMIT 0").description]
        contract_list = [dict(zip(c_cols, c)) for c in contracts]

        # 计算平均合作费用
        budgets = [c.get("budget", 0) for c in contract_list if c.get("budget")]
        avg_budget = sum(budgets) / max(len(budgets), 1)

        # 效果指标（如果有归因数据）
        attributed = conn.execute("""
            SELECT SUM(conversions_attributed) as total_conversions, SUM(revenue_attributed) as total_revenue
            FROM content_attribution
            WHERE kol_id = ?
        """, (kol_id,)).fetchone()

        return {
            "kol": {
                "kol_id": kol_data.get("kol_id"),
                "username": kol_data.get("username"),
                "platform": kol_data.get("platform"),
                "fans_count": kol_data.get("fans_count"),
                "category": kol_data.get("category"),
                "cooperation_rate": kol_data.get("cooperation_rate"),
            },
            "contract_count": len(contract_list),
            "avg_contract_budget": round(avg_budget, 2),
            "total_conversions": attributed[0] if attributed else 0,
            "total_revenue_attributed": attributed[1] if attributed else 0,
            "recent_contracts": contract_list[:3],
        }
    finally:
        if own_conn:
            conn.close()


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
    action = args.get("action", "match")
    content_type = args.get("content_type")
    target_audience = args.get("target_audience")
    platform = args.get("platform")
    budget = args.get("budget")
    kol_id = args.get("kol_id")
    limit = args.get("limit", 10)

    if action == "match":
        result = match_kols(content_type, target_audience, platform, budget, limit)
    elif action == "list":
        conn = get_conn()
        kols = list_kols(conn, platform, limit=limit)
        close_conn(conn)
        result = {"platform": platform, "count": len(kols), "kols": kols}
    elif action == "analyze":
        result = analyze_kol_performance(kol_id)
    else:
        result = {"error": f"Unknown action: {action}"}

    print(json.dumps(result, ensure_ascii=False, indent=2))
