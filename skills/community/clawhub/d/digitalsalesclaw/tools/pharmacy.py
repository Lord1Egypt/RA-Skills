#!/usr/bin/env python3
"""
DigitalSalesClaw - pharmacy.py
药房库存管理工具

输入: {"action": "status|low_stock|restock_plan|forecast", "pharmacy": "..."}
输出: {"inventory, low_stock, restock_plan, ...}
"""
import sys
import json
from pathlib import Path
from datetime import datetime, date, timedelta
from decimal import Decimal
from db import get_conn, close_conn, query_all, query_one


def _json_serial(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def get_status(conn, pharmacy: str = None) -> dict:
    """库存状态"""
    if pharmacy:
        rows = query_all("""
            SELECT id, product_id, product_name, quantity, reorder_point,
                   pharmacy, status, last_restocked, created_at
            FROM pharmacy_inventory
            WHERE pharmacy LIKE %s
            ORDER BY status = 'out' DESC, quantity ASC
        """, (f"%{pharmacy}%",))
    else:
        rows = query_all("""
            SELECT id, product_id, product_name, quantity, reorder_point,
                   pharmacy, status, last_restocked, created_at
            FROM pharmacy_inventory
            ORDER BY status = 'out' DESC, quantity ASC
        """)

    status_dist = {"ok": 0, "low": 0, "out": 0}
    total_quantity = sum(i.get("quantity", 0) for i in rows)

    for item in rows:
        s = item.get("status", "ok")
        status_dist[s] = status_dist.get(s, 0) + 1

    return {
        "total_items": len(rows),
        "total_quantity": total_quantity,
        "status_distribution": status_dist,
        "items": rows[:20],
        "pharmacy": pharmacy,
        "suggestions": [
            f"库存品种 {len(rows)} 个，状态分布：正常 {status_dist['ok']}，不足 {status_dist['low']}，售罄 {status_dist['out']}"
        ]
    }


def get_low_stock(conn, threshold: float = 1.5) -> dict:
    """低库存预警"""
    rows = query_all("""
        SELECT id, product_id, product_name, quantity, reorder_point,
               pharmacy, status, last_restocked
        FROM pharmacy_inventory
        WHERE status IN ('low', 'out')
           OR quantity / NULLIF(reorder_point, 0) <= %s
        ORDER BY status = 'out' DESC, quantity ASC
    """, (threshold,))

    urgent = [i for i in rows if i.get("status") == "out"]
    warning = [i for i in rows if i.get("status") == "low"]

    return {
        "low_stock_count": len(rows),
        "urgent_count": len(urgent),
        "warning_count": len(warning),
        "urgent_items": urgent[:10],
        "warning_items": warning[:10],
        "all_low_stock": rows[:20],
        "suggestions": [
            f"紧急补货 {len(urgent)} 个品种（已售罄）",
            f"库存预警 {len(warning)} 个品种（低于阈值）",
            "建议优先处理 urgent 列表"
        ]
    }


def generate_restock_plan(conn, pharmacy: str = None) -> dict:
    """生成补货计划"""
    low = get_low_stock(conn, 2.0)
    items = low.get("all_low_stock", [])

    plan = []
    for item in items:
        current_qty = item.get("quantity", 0)
        reorder_point = item.get("reorder_point", 10) or 10
        suggested_order = max(reorder_point * 2 - current_qty, reorder_point)
        urgency = "critical" if item.get("status") == "out" else "high" if current_qty < reorder_point else "medium"

        plan.append({
            "product_id": item.get("product_id"),
            "product_name": item.get("product_name"),
            "current_quantity": current_qty,
            "reorder_point": reorder_point,
            "suggested_order_quantity": max(suggested_order, 0),
            "urgency": urgency,
            "pharmacy": item.get("pharmacy")
        })

    plan.sort(key=lambda x: {"critical": 0, "high": 1, "medium": 2}.get(x["urgency"], 3))

    total_order = sum(p["suggested_order_quantity"] for p in plan)

    return {
        "plan_items": len(plan),
        "total_order_quantity": total_order,
        "critical_items": len([p for p in plan if p["urgency"] == "critical"]),
        "restock_plan": plan[:20],
        "suggestions": [
            f"建议补货 {len(plan)} 个品种，总计 {total_order} 件",
            f"其中 {len([p for p in plan if p['urgency']=='critical'])} 个紧急品种",
            "补货计划已按紧急程度排序"
        ]
    }


def forecast(conn, product_id: str = None) -> dict:
    """销售预测"""
    if product_id:
        rows = query_all("""
            SELECT sf.product_id, sf.forecast_date, sf.predicted_sales, sf.confidence,
                   pi.product_name, pi.quantity as current_stock
            FROM sales_forecast sf
            LEFT JOIN pharmacy_inventory pi ON pi.product_id = sf.product_id
            WHERE sf.product_id = %s
            ORDER BY sf.forecast_date DESC LIMIT 50
        """, (product_id,))
    else:
        rows = query_all("""
            SELECT sf.product_id, sf.forecast_date, sf.predicted_sales, sf.confidence,
                   pi.product_name, pi.quantity as current_stock
            FROM sales_forecast sf
            LEFT JOIN pharmacy_inventory pi ON pi.product_id = sf.product_id
            ORDER BY sf.forecast_date DESC LIMIT 50
        """)

    return {
        "forecast_count": len(rows),
        "forecasts": rows[:10],
        "suggestions": [
            f"当前有 {len(rows)} 条销售预测",
            "基于历史数据预测未来销量",
            "建议结合库存情况制定补货计划"
        ]
    }


def _parse_args():
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError:
            return {"action": "status"}
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
    action = args.get("action", "status")
    pharmacy = args.get("pharmacy")
    product_id = args.get("product_id")
    threshold = args.get("threshold", 1.5)

    conn = get_conn()

    try:
        if action == "status":
            result = get_status(conn, pharmacy)
        elif action == "low_stock":
            result = get_low_stock(conn, threshold)
        elif action == "restock_plan":
            result = generate_restock_plan(conn, pharmacy)
        elif action == "forecast":
            result = forecast(conn, product_id)
        else:
            result = {"error": f"Unknown action: {action}"}
    finally:
        close_conn(conn)

    print(json.dumps(result, ensure_ascii=False, indent=2, default=_json_serial))