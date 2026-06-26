#!/usr/bin/env python3
"""
DigitalSalesClaw - ad_optimization.py
广告投放优化工具

功能:
- 关键词出价建议（基于效果数据动态调整）
- 投放预算分配（ROI 最优化）
- 投放效果分析（ACOS、PACOS、ROAS）
- 关键词扩展建议

输入: {"action": "bid_suggest|budget_allocate|analyze|expand_keywords", "campaign_id": "...", "keyword": "..."}
输出: {"suggestions, bids, budget_allocation, analysis}
"""

import sys
import json
import math
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent


def ensure_ad_tables(conn):
    """确保广告分析表存在"""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ad_keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            campaign_id TEXT,
            max_bid REAL DEFAULT 1.0,
            current_bid REAL DEFAULT 1.0,
            impressions INTEGER DEFAULT 0,
            clicks INTEGER DEFAULT 0,
            spend REAL DEFAULT 0,
            conversions INTEGER DEFAULT 0,
            revenue REAL DEFAULT 0,
            status TEXT DEFAULT 'active',
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ad_budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id TEXT UNIQUE NOT NULL,
            total_budget REAL,
            daily_budget REAL,
            spent_today REAL DEFAULT 0,
            spent_total REAL DEFAULT 0,
            start_date TEXT,
            end_date TEXT,
            status TEXT DEFAULT 'active',
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()


def compute_ad_metrics(keyword_data):
    """计算单个关键词的广告效果指标"""
    impressions = keyword_data.get("impressions") or 0
    clicks = keyword_data.get("clicks") or 0
    spend = keyword_data.get("spend") or 0
    conversions = keyword_data.get("conversions") or 0
    revenue = keyword_data.get("revenue") or 0

    ctr = (clicks / impressions * 100) if impressions > 0 else 0
    cpc = (spend / clicks) if clicks > 0 else 0
    acos = (spend / revenue * 100) if revenue > 0 else None
    roas = (revenue / spend) if spend > 0 else 0
    cvr = (conversions / clicks * 100) if clicks > 0 else 0

    return {
        "ctr": round(ctr, 2),
        "cpc": round(cpc, 2),
        "acos": round(acos, 2) if acos is not None else None,
        "roas": round(roas, 2),
        "cvr": round(cvr, 2),
        "impressions": impressions,
        "clicks": clicks,
        "spend": round(spend, 2),
        "conversions": conversions,
        "revenue": round(revenue, 2),
    }


def suggest_bids(campaign_id=None, conn=None):
    """
    基于关键词效果数据，生成智能出价建议
    - CTR 高 + CVR 高 -> 提价（爆量）
    - CTR 高 + CVR 低 -> 降价格局（控制无效点击）
    - CTR 低 + CVR 高 -> 优化素材（ctr 潜力大）
    - CTR 低 + CVR 低 -> 降价或暂停
    """
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_ad_tables(conn)
        sql = "SELECT * FROM ad_keywords WHERE 1=1"
        params = []
        if campaign_id:
            sql += " AND campaign_id = ?"
            params.append(campaign_id)
        sql += " ORDER BY impressions DESC"

        rows = conn.execute(sql, params).fetchall()
        cols = [d[0] for d in conn.execute("SELECT * FROM ad_keywords LIMIT 0").description]
        keywords = [dict(zip(cols, r)) for r in rows]

        if not keywords:
            return {
                "campaign_id": campaign_id or "all",
                "mode": "fallback_simulation",
                "message": "广告关键词数据不足，基于内容营销数据模拟建议",
                "suggestions": _generate_fallback_suggestions(conn, campaign_id),
            }

        bid_suggestions = []
        for kw in keywords:
            metrics = compute_ad_metrics(kw)
            current_bid = kw.get("current_bid") or 1.0
            ctr = metrics["ctr"]
            cvr = metrics["cvr"]

            if ctr > 5 and cvr > 3:
                action = "increase"
                new_bid = round(current_bid * 1.2, 2)
                reason = "CTR和转化率双高，提价扩量"
                priority = "high"
            elif ctr > 5 and cvr <= 1:
                action = "decrease"
                new_bid = round(current_bid * 0.7, 2)
                reason = "CTR高但转化低，控制无效点击成本"
                priority = "medium"
            elif ctr < 1 and cvr > 3:
                action = "increase"
                new_bid = round(current_bid * 1.15, 2)
                reason = "转化率高但CTR低，素材优化后有提价空间"
                priority = "medium"
            elif ctr < 1 and cvr < 1:
                action = "decrease"
                new_bid = round(current_bid * 0.5, 2)
                reason = "CTR和转化率均低，建议暂停或大幅降价"
                priority = "high"
            elif metrics["impressions"] < 100:
                action = "test"
                new_bid = round(current_bid * 1.1, 2)
                reason = "曝光不足，适当提价测试"
                priority = "low"
            else:
                action = "maintain"
                new_bid = current_bid
                reason = "效果稳定，维持当前出价"
                priority = "low"

            if metrics["acos"] is not None:
                if metrics["acos"] > 50:
                    reason += " | ACOS过高，注意盈利平衡"
                elif metrics["acos"] < 15:
                    reason += " | ACOS优秀，可适当提价"

            bid_suggestions.append({
                "keyword": kw.get("keyword"),
                "campaign_id": kw.get("campaign_id"),
                "current_bid": current_bid,
                "suggested_bid": max(new_bid, 0.1),
                "action": action,
                "priority": priority,
                "reason": reason,
                "metrics": metrics,
            })

        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        bid_suggestions.sort(key=lambda x: priority_order.get(x["priority"], 9))

        increase = [b for b in bid_suggestions if b["action"] == "increase"]
        decrease = [b for b in bid_suggestions if b["action"] == "decrease"]
        maintain = [b for b in bid_suggestions if b["action"] == "maintain"]

        return {
            "campaign_id": campaign_id or "all",
            "total_keywords": len(keywords),
            "bid_suggestions": bid_suggestions,
            "summary": {
                "increase_count": len(increase),
                "decrease_count": len(decrease),
                "maintain_count": len(maintain),
            },
            "suggestions": [
                f"建议提价 {len(increase)} 个关键词扩量",
                f"建议降价 {len(decrease)} 个关键词控成本",
                "高优先级建议立即执行"
            ]
        }
    finally:
        if own_conn:
            conn.close()


def _generate_fallback_suggestions(conn, campaign_id):
    """基于 content_metrics 生成模拟出价建议"""
    rows = conn.execute("""
        SELECT campaign_id, SUM(spend) as total_spend, SUM(clicks) as total_clicks,
               SUM(impressions) as total_imp, SUM(conversions) as total_conv
        FROM content_metrics
        WHERE campaign_id IS NOT NULL
        GROUP BY campaign_id
        LIMIT 20
    """).fetchall()

    suggestions = []
    for row in rows:
        cid, spend, clicks, imp, conv = row
        if imp and imp > 0 and clicks and clicks > 0:
            ctr = (clicks / imp) * 100
            cpc = spend / clicks if clicks > 0 else 0
            suggestions.append({
                "campaign_id": cid,
                "avg_ctr": round(ctr, 2),
                "avg_cpc": round(cpc, 2),
                "total_conversions": conv or 0,
                "suggested_action": "increase_budget" if ctr > 2 and conv and conv > 0 else "optimize_content",
            })
    return suggestions[:10]


def allocate_budget(campaign_id=None, total_budget=10000, target_roas=3.0, conn=None):
    """基于 ROI 最优化的预算分配建议"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_ad_tables(conn)
        rows = conn.execute("""
            SELECT cm.campaign_id, cc.name as campaign_name,
                   SUM(cm.spend) as total_spend, SUM(cm.revenue) as total_revenue,
                   SUM(cm.conversions) as total_conv
            FROM content_metrics cm
            LEFT JOIN content_campaigns cc ON cc.id = cm.campaign_id
            WHERE cm.spend > 0
            GROUP BY cm.campaign_id
            ORDER BY total_revenue / NULLIF(total_spend, 0) DESC
            LIMIT 20
        """).fetchall()

        if not rows:
            return {
                "total_budget": total_budget,
                "error": "No campaign data available for budget allocation",
                "suggestions": ["请确保有足够的投放数据后再进行预算分配"]
            }

        campaigns = []
        total_score = 0
        for row in rows:
            cid, name, spend, revenue, conv = row
            roas = (revenue / spend) if spend and spend > 0 else 0
            score = roas
            campaigns.append({
                "campaign_id": cid,
                "campaign_name": name or cid,
                "roas": round(roas, 2),
                "total_spend": round(spend, 2) if spend else 0,
                "total_revenue": round(revenue, 2) if revenue else 0,
                "total_conversions": conv or 0,
                "raw_score": score,
            })
            total_score += score

        allocations = []
        for c in campaigns:
            weight = c["raw_score"] / total_score if total_score > 0 else 0
            allocated = total_budget * weight
            c["allocated_budget"] = round(allocated, 2)
            c["weight"] = round(weight, 4)

            if c["roas"] < target_roas * 0.5:
                adjustment = "reduce - ROAS 低于目标过多"
            elif c["roas"] > target_roas * 1.5:
                adjustment = "increase - ROAS 超预期，可追加"
            else:
                adjustment = "maintain - 符合预期"
            c["adjustment"] = adjustment
            allocations.append(c)

        allocations.sort(key=lambda x: -x["roas"])

        return {
            "total_budget": total_budget,
            "target_roas": target_roas,
            "campaign_count": len(allocations),
            "allocations": allocations,
            "suggestions": [
                f"总预算 ¥{total_budget:,.0f} 分配给 {len(allocations)} 个营销活动",
                "高 ROAS 活动获得更多预算分配",
                "建议每周复盘并动态调整"
            ]
        }
    finally:
        if own_conn:
            conn.close()


def analyze_ad_performance(campaign_id=None, period_days=30, conn=None):
    """综合投放效果分析（ACOS / PACOS / ROAS）"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_ad_tables(conn)
        sql = """
            SELECT cm.campaign_id, cc.name as campaign_name, cc.budget,
                   SUM(cm.spend) as total_spend, SUM(cm.revenue) as total_revenue,
                   SUM(cm.impressions) as total_imp, SUM(cm.clicks) as total_clicks,
                   SUM(cm.conversions) as total_conv
            FROM content_metrics cm
            LEFT JOIN content_campaigns cc ON cc.id = cm.campaign_id
            WHERE cm.date >= datetime('now', ?)
        """
        params = [f"-{period_days} days"]
        if campaign_id:
            sql += " AND cm.campaign_id = ?"
            params.append(campaign_id)
        sql += " GROUP BY cm.campaign_id ORDER BY total_spend DESC"

        rows = conn.execute(sql, params).fetchall()

        analyses = []
        for row in rows:
            cid, name, budget, spend, revenue, imp, clicks, conv = row
            spend = spend or 0
            revenue = revenue or 0
            ctr = (clicks / imp * 100) if imp and imp > 0 else 0
            cpc = (spend / clicks) if clicks and clicks > 0 else 0
            acos = (spend / revenue * 100) if revenue > 0 else 0
            roas = (revenue / spend) if spend > 0 else 0
            cvr = (conv / clicks * 100) if clicks and clicks > 0 else 0
            gross_margin = 0.6
            pacos = acos / gross_margin if acos else 0

            if roas >= 4:
                health = "excellent"
                health_tip = "ROAS 优秀，投放效率高"
            elif roas >= 2:
                health = "healthy"
                health_tip = "ROAS 健康，可持续投放"
            elif roas >= 1:
                health = "warning"
                health_tip = "ROAS 偏低，需优化"
            else:
                health = "critical"
                health_tip = "ROAS 亏损，建议暂停或大幅优化"

            analyses.append({
                "campaign_id": cid,
                "campaign_name": name or cid,
                "budget": budget or 0,
                "total_spend": round(spend, 2),
                "total_revenue": round(revenue, 2),
                "total_impressions": imp or 0,
                "total_clicks": clicks or 0,
                "total_conversions": conv or 0,
                "ctr": round(ctr, 2),
                "cpc": round(cpc, 2),
                "acos": round(acos, 2),
                "pacos": round(pacos, 2),
                "roas": round(roas, 2),
                "cvr": round(cvr, 2),
                "health": health,
                "health_tip": health_tip,
            })

        analyses.sort(key=lambda x: -x["roas"])
        total_spend = sum(a["total_spend"] for a in analyses)
        total_revenue = sum(a["total_revenue"] for a in analyses)
        overall_roas = total_revenue / total_spend if total_spend > 0 else 0

        return {
            "period_days": period_days,
            "campaign_count": len(analyses),
            "total_spend": round(total_spend, 2),
            "total_revenue": round(total_revenue, 2),
            "overall_roas": round(overall_roas, 2),
            "campaigns": analyses,
            "suggestions": [
                f"{len(analyses)} 个营销活动整体 ROAS: {round(overall_roas, 2)}",
                f"总花费 ¥{total_spend:,.0f}，总收益 ¥{total_revenue:,.0f}",
                "建议优先复盘 ROAS < 1 的活动"
            ]
        }
    finally:
        if own_conn:
            conn.close()


def expand_keywords(seed_keyword, top_n=20, conn=None):
    """基于种子关键词扩展相关关键词"""
    try:
        import jieba
        JIEBA = True
    except ImportError:
        JIEBA = False

    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_ad_tables(conn)
        rows = conn.execute("""
            SELECT keyword, impressions, clicks, conversions
            FROM ad_keywords
            WHERE keyword IS NOT NULL
            LIMIT 100
        """).fetchall()

        all_keywords = {r[0]: {"imp": r[1] or 0, "clk": r[2] or 0, "conv": r[3] or 0} for r in rows}

        tokens = list(jieba.cut(seed_keyword)) if JIEBA else [seed_keyword]

        prefixes = ["糖尿病", "高血压", "儿童", "维生素", "补钙", "护肝"]
        suffixes = ["管理", "治疗", "预防", "饮食", "用药", "指南"]

        seen = set()
        recommended = []
        for kw, data in all_keywords.items():
            if kw == seed_keyword:
                continue
            if seed_keyword in kw or kw in seed_keyword:
                if data["imp"] > 0:
                    ctr = (data["clk"] / data["imp"] * 100) if data["imp"] > 0 else 0
                    recommended.append({
                        "keyword": kw,
                        "impressions": data["imp"],
                        "clicks": data["clk"],
                        "conversions": data["conv"],
                        "ctr": round(ctr, 2),
                        "recommend": "high" if ctr > 3 else "medium" if ctr > 1 else "low",
                    })

        recommended.sort(key=lambda x: -x["ctr"])

        return {
            "seed_keyword": seed_keyword,
            "tokens": tokens,
            "total_found": len(recommended),
            "expanded_keywords": recommended[:top_n],
            "suggestions": [
                f"基于「{seed_keyword}」扩展出 {min(top_n, len(recommended))} 个相关关键词",
                "优先选择 CTR 高的关键词进行投放",
                "建议使用 jieba 词库扩充更多长尾词"
            ]
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
    action = args.get("action", "analyze")

    if action == "bid_suggest":
        result = suggest_bids(args.get("campaign_id"))
    elif action == "budget_allocate":
        result = allocate_budget(
            campaign_id=args.get("campaign_id"),
            total_budget=args.get("total_budget", 10000),
            target_roas=args.get("target_roas", 3.0),
        )
    elif action == "analyze":
        result = analyze_ad_performance(
            campaign_id=args.get("campaign_id"),
            period_days=args.get("period_days", 30),
        )
    elif action == "expand_keywords":
        result = expand_keywords(
            seed_keyword=args.get("keyword", ""),
            top_n=args.get("top_n", 20),
        )
    else:
        result = {"error": f"Unknown action: {action}"}

    print(json.dumps(result, ensure_ascii=False, indent=2))
