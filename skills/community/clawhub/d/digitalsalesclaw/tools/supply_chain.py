#!/usr/bin/env python3
"""
DigitalSalesClaw - supply_chain.py
供应链管理工具

功能:
- 采购订单管理（创建/审批/跟踪）
- 库存状态监控
- 补货计划生成
- 物流跟踪

输入: {"action": "create_order|approve|reject|track|restock_plan|status", ...}
输出: {"order, status, items, suggestions}
"""

import sys
import json
import uuid
from pathlib import Path
from datetime import datetime, timedelta
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent


def ensure_order_table(conn):
    """确保采购订单表存在"""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS supply_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT UNIQUE NOT NULL,
            product_id TEXT NOT NULL,
            product_name TEXT,
            quantity INTEGER NOT NULL,
            unit_price REAL,
            total_amount REAL,
            supplier TEXT,
            status TEXT DEFAULT 'pending',
            priority TEXT DEFAULT 'normal',
            ordered_by TEXT,
            approved_by TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            approved_at DATETIME,
            shipped_at DATETIME,
            delivered_at DATETIME,
            notes TEXT
        )
    """)


def ensure_shipment_table(conn):
    """确保物流跟踪表存在"""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS supply_shipments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shipment_id TEXT UNIQUE NOT NULL,
            order_id TEXT NOT NULL,
            carrier TEXT,
            tracking_number TEXT,
            status TEXT DEFAULT 'in_transit',
            estimated_delivery DATETIME,
            actual_delivery DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)


def create_order(product_id, quantity, unit_price=None,
                 supplier=None, priority="normal",
                 ordered_by="ai", notes=None, conn=None):
    """创建采购订单"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_order_table(conn)

        product_name = product_id
        if unit_price is None:
            inv = conn.execute(
                "SELECT product_name FROM pharmacy_inventory WHERE product_id = ?",
                (product_id,)
            ).fetchone()
            if inv:
                product_name = inv[0]

        order_id = f"PO-{datetime.now().strftime('%Y%m%d')}-{product_id[-6:]}"
        total_amount = (unit_price or 0) * quantity

        conn.execute("""
            INSERT INTO supply_orders (order_id, product_id, product_name, quantity, unit_price, total_amount, supplier, priority, ordered_by, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (order_id, product_id, product_name, quantity, unit_price, total_amount, supplier, priority, ordered_by, notes))
        conn.commit()

        return {
            "order_id": order_id,
            "product_id": product_id,
            "product_name": product_name,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_amount": total_amount,
            "status": "pending",
            "priority": priority,
            "suggestions": [
                f"采购订单 {order_id} 已创建，等待审批",
                f"订单金额: ¥{total_amount:.2f}" if total_amount else "价格待确认",
                "请等待管理员审批后执行采购"
            ]
        }
    finally:
        if own_conn:
            conn.close()


def approve_order(order_id, approved_by="admin", conn=None):
    """审批采购订单"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_order_table(conn)
        order = conn.execute("SELECT * FROM supply_orders WHERE order_id = ?", (order_id,)).fetchone()
        if not order:
            return {"error": f"Order {order_id} not found"}
        if order["status"] != "pending":
            return {"error": f"Order {order_id} is not pending (current: {order['status']})"}

        conn.execute("""
            UPDATE supply_orders SET status = 'approved', approved_by = ?, approved_at = ?
            WHERE order_id = ?
        """, (approved_by, datetime.now().isoformat(), order_id))
        conn.commit()

        updated = conn.execute("SELECT * FROM supply_orders WHERE order_id = ?", (order_id,)).fetchone()
        cols = [d[0] for d in conn.execute("SELECT * FROM supply_orders LIMIT 0").description]
        order_dict = dict(zip(cols, updated)) if updated else {}

        return {
            "order_id": order_id,
            "status": "approved",
            "approved_by": approved_by,
            "approved_at": order_dict.get("approved_at"),
            "suggestions": [
                f"订单 {order_id} 已审批通过",
                f"可执行采购，供应商: {order_dict.get('supplier', '待定')}",
                "订单状态变更为 approved，等待发货"
            ]
        }
    finally:
        if own_conn:
            conn.close()


def reject_order(order_id, rejected_by="admin", reason=None, conn=None):
    """拒绝采购订单"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_order_table(conn)
        order = conn.execute("SELECT * FROM supply_orders WHERE order_id = ?", (order_id,)).fetchone()
        if not order:
            return {"error": f"Order {order_id} not found"}

        conn.execute("""
            UPDATE supply_orders
            SET status = 'rejected', notes = COALESCE(notes, '') || ' | Rejected: ' || ?
            WHERE order_id = ?
        """, (reason or "No reason provided", order_id))
        conn.commit()

        return {
            "order_id": order_id,
            "status": "rejected",
            "rejected_by": rejected_by,
            "reason": reason,
            "suggestions": [f"订单 {order_id} 已拒绝: {reason or '无'}"]
        }
    finally:
        if own_conn:
            conn.close()


def ship_order(order_id, carrier=None, tracking_number=None,
               estimated_delivery_days=3, conn=None):
    """订单发货"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_order_table(conn)
        ensure_shipment_table(conn)

        order = conn.execute("SELECT * FROM supply_orders WHERE order_id = ?", (order_id,)).fetchone()
        if not order:
            return {"error": f"Order {order_id} not found"}
        if order["status"] not in ("approved", "shipped"):
            return {"error": f"Order {order_id} cannot be shipped from status: {order['status']}"}

        shipment_id = f"SH-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        estimated = datetime.now() + timedelta(days=estimated_delivery_days)

        conn.execute("""
            INSERT INTO supply_shipments (shipment_id, order_id, carrier, tracking_number, estimated_delivery)
            VALUES (?, ?, ?, ?, ?)
        """, (shipment_id, order_id, carrier, tracking_number, estimated.isoformat()))
        conn.execute(
            "UPDATE supply_orders SET status = 'shipped', shipped_at = ? WHERE order_id = ?",
            (datetime.now().isoformat(), order_id)
        )
        conn.commit()

        return {
            "order_id": order_id,
            "shipment_id": shipment_id,
            "carrier": carrier,
            "tracking_number": tracking_number,
            "status": "shipped",
            "estimated_delivery": estimated.strftime("%Y-%m-%d"),
            "suggestions": [
                f"订单 {order_id} 已发货",
                f"物流单号: {tracking_number or '待填写'}",
                f"预计 {estimated.strftime('%Y-%m-%d')} 送达"
            ]
        }
    finally:
        if own_conn:
            conn.close()


def track_shipment(order_id=None, conn=None):
    """查询物流状态"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_shipment_table(conn)
        sql = "SELECT * FROM supply_shipments WHERE 1=1"
        params = []
        if order_id:
            sql += " AND order_id = ?"
            params.append(order_id)
        sql += " ORDER BY created_at DESC LIMIT 20"

        rows = conn.execute(sql, params).fetchall()
        cols = [d[0] for d in conn.execute("SELECT * FROM supply_shipments LIMIT 0").description]
        shipments = [dict(zip(cols, r)) for r in rows]

        in_transit = [s for s in shipments if s.get("status") == "in_transit"]
        delivered = [s for s in shipments if s.get("status") == "delivered"]

        return {
            "total_shipments": len(shipments),
            "in_transit": len(in_transit),
            "delivered": len(delivered),
            "shipments": shipments,
            "suggestions": [
                f"{len(in_transit)} 个包裹在途，{len(delivered)} 个已送达",
                "如物流异常请检查承运商系统"
            ]
        }
    finally:
        if own_conn:
            conn.close()


def list_orders(status=None, conn=None):
    """查询采购订单列表"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_order_table(conn)
        sql = "SELECT * FROM supply_orders WHERE 1=1"
        params = []
        if status:
            sql += " AND status = ?"
            params.append(status)
        sql += " ORDER BY created_at DESC LIMIT 50"

        rows = conn.execute(sql, params).fetchall()
        cols = [d[0] for d in conn.execute("SELECT * FROM supply_orders LIMIT 0").description]
        orders = [dict(zip(cols, r)) for r in rows]

        by_status = defaultdict(list)
        for o in orders:
            by_status[o.get("status", "unknown")].append(o)

        return {
            "total": len(orders),
            "by_status": dict(by_status),
            "orders": orders,
            "suggestions": [
                f"共 {len(orders)} 个采购订单",
                f"待审批: {len(by_status.get('pending', []))}",
                f"已发货: {len(by_status.get('shipped', []))}"
            ]
        }
    finally:
        if own_conn:
            conn.close()


def restock_plan(conn=None):
    """根据库存情况生成补货计划"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_order_table(conn)
        items = conn.execute("""
            SELECT product_id, product_name, quantity, reorder_point, pharmacy, last_restocked
            FROM pharmacy_inventory
            WHERE CAST(quantity AS REAL) / NULLIF(reorder_point, 0) < 1.5
            ORDER BY (CAST(quantity AS REAL) / NULLIF(reorder_point, 0)) ASC
        """).fetchall()

        cols = [d[0] for d in conn.execute("SELECT * FROM pharmacy_inventory LIMIT 0").description]
        inventory = [dict(zip(cols, r)) for r in items]

        plan_items = []
        for item in inventory:
            qty = item.get("quantity") or 0
            reorder = item.get("reorder_point") or 10
            suggested_order = max(reorder * 2 - qty, reorder)

            existing = conn.execute("""
                SELECT COUNT(*) FROM supply_orders
                WHERE product_id = ? AND status IN ('pending', 'approved')
            """, (item.get("product_id"),)).fetchone()[0]

            if existing > 0:
                continue

            plan_items.append({
                "product_id": item.get("product_id"),
                "product_name": item.get("product_name"),
                "current_stock": qty,
                "reorder_point": reorder,
                "suggested_order_qty": suggested_order,
                "pharmacy": item.get("pharmacy"),
                "last_restocked": item.get("last_restocked"),
                "priority": "urgent" if qty == 0 else "normal",
            })

        return {
            "plan_items": plan_items,
            "total_items_to_restock": len(plan_items),
            "urgent_count": len([p for p in plan_items if p["priority"] == "urgent"]),
            "suggestions": [
                f"建议补货 {len(plan_items)} 个品种",
                f"其中 {len([p for p in plan_items if p['priority'] == 'urgent'])} 个紧急",
                "可使用 create_order 批量创建采购单"
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
    action = args.get("action", "status")

    if action == "create_order":
        result = create_order(
            product_id=args.get("product_id", ""),
            quantity=args.get("quantity", 0),
            unit_price=args.get("unit_price"),
            supplier=args.get("supplier"),
            priority=args.get("priority", "normal"),
            ordered_by=args.get("ordered_by", "ai"),
            notes=args.get("notes"),
        )
    elif action == "approve":
        result = approve_order(args.get("order_id", ""), args.get("approved_by", "admin"))
    elif action == "reject":
        result = reject_order(args.get("order_id", ""), args.get("rejected_by", "admin"), args.get("reason"))
    elif action == "ship":
        result = ship_order(
            args.get("order_id", ""),
            args.get("carrier"),
            args.get("tracking_number"),
            args.get("estimated_delivery_days", 3)
        )
    elif action == "track":
        result = track_shipment(args.get("order_id"))
    elif action == "list_orders":
        result = list_orders(args.get("status"))
    elif action == "restock_plan":
        result = restock_plan()
    elif action == "status":
        result = list_orders()
    else:
        result = {"error": f"Unknown action: {action}"}

    print(json.dumps(result, ensure_ascii=False, indent=2))
