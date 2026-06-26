#!/usr/bin/env python3
"""
DigitalSalesClaw - competitor.py
竞品分析工具

输入: {"action": "list|analyze|monitor|price_alert", "competitor": "...", "product_id": "..."}
输出: {"products, analysis, alerts, ...}
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent


def list_competitors(conn, platform: str = None) -> dict:
    """竞品列表"""
    query = """
        SELECT dp.id, dp.product_id, dp.name, dp.platform, dp.price, dp.cost,
               dp.category, dp.rating, dp.reviews_count, dp.sales_trend, dp.profit_margin,
               (SELECT COUNT(*) FROM competitor_analysis ca WHERE ca.product_id = dp.product_id) as analysis_count
        FROM drug_products dp
        WHERE 1=1
    """
    params = []
    if platform:
        query += " AND dp.platform = ?"
        params.append(platform)
    query += " ORDER BY dp.reviews_count DESC"

    rows = conn.execute(query, params).fetchall()
    cols = [d[0] for d in conn.execute("SELECT * FROM drug_products LIMIT 0").description]
    products = [dict(zip(cols, r)) for r in rows]

    return {
        "total_competitors": len(products),
        "products": products[:20],
        "suggestions": [
            f"追踪 {len(products)} 个竞品",
            "按评价数量排序，关注高热度竞品",
            "可查看具体竞品的价格和评分变化"
        ]
    }


def analyze_competitor(conn, competitor_name: str = None, product_id: str = None) -> dict:
    """竞品详细分析"""
    if product_id:
        analysis = conn.execute("""
            SELECT ca.*, dp.name as product_name
            FROM competitor_analysis ca
            JOIN drug_products dp ON dp.product_id = ca.product_id
            WHERE ca.product_id = ?
            ORDER BY ca.analysis_date DESC LIMIT 20
        """, (product_id,)).fetchall()
    elif competitor_name:
        analysis = conn.execute("""
            SELECT ca.*, dp.name as product_name
            FROM competitor_analysis ca
            JOIN drug_products dp ON dp.product_id = ca.product_id
            WHERE ca.competitor_name LIKE ?
            ORDER BY ca.analysis_date DESC LIMIT 20
        """, (f"%{competitor_name}%",)).fetchall()
    else:
        analysis = conn.execute("""
            SELECT ca.*, dp.name as product_name
            FROM competitor_analysis ca
            JOIN drug_products dp ON dp.product_id = ca.product_id
            ORDER BY ca.analysis_date DESC LIMIT 20
        """).fetchall()

    cols = [d[0] for d in conn.execute("SELECT * FROM competitor_analysis LIMIT 0").description]
    analysis_list = [dict(zip(cols, r)) for r in analysis]

    # 价格波动分析
    price_changes = []
    for a in analysis_list:
        if a.get("competitor_price"):
            price_changes.append({
                "competitor_name": a.get("competitor_name"),
                "price": a.get("competitor_price"),
                "date": a.get("analysis_date")
            })

    return {
        "analysis_count": len(analysis_list),
        "latest_analysis": analysis_list[:5] if analysis_list else [],
        "price_history": price_changes[-10:] if price_changes else [],
        "suggestions": [
            f"共 {len(analysis_list)} 条分析记录",
            f"最近分析：{analysis_list[0].get('analysis_date', 'N/A') if analysis_list else 'N/A'}",
            "关注价格和评分的变化趋势"
        ]
    }


def get_metrics(conn, competitor_name: str = None) -> dict:
    """竞品指标监控"""
    query = "SELECT * FROM competitor_metrics WHERE 1=1"
    params = []
    if competitor_name:
        query += " AND competitor_name LIKE ?"
        params.append(f"%{competitor_name}%")
    query += " ORDER BY record_date DESC LIMIT 50"

    rows = conn.execute(query, params).fetchall()
    cols = [d[0] for d in conn.execute("SELECT * FROM competitor_metrics LIMIT 0").description]
    metrics = [dict(zip(cols, r)) for r in rows]

    # 按类型分组
    by_type = {}
    for m in metrics:
        t = m.get("metric_type", "unknown")
        if t not in by_type:
            by_type[t] = []
        by_type[t].append(m)

    return {
        "total_metrics": len(metrics),
        "metric_types": list(by_type.keys()),
        "recent_metrics": metrics[:10],
        "suggestions": [
            f"追踪 {len(by_type)} 种指标类型",
            f"共 {len(metrics)} 条指标记录",
            "可用于监控竞品动态和市场份额变化"
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
    competitor = args.get("competitor")
    product_id = args.get("product_id")
    platform = args.get("platform")

    conn = get_conn()
    
    try:
        if action == "list":
            result = list_competitors(conn, platform)
        elif action == "analyze":
            result = analyze_competitor(conn, competitor, product_id)
        elif action == "metrics":
            result = get_metrics(conn, competitor)
        else:
            result = {"error": f"Unknown action: {action}"}
    finally:
        close_conn(conn)

    print(json.dumps(result, ensure_ascii=False, indent=2))
