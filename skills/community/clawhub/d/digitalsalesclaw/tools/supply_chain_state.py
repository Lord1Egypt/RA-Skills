#!/usr/bin/env python3
"""
Phase 3.2 - 供应链状态机

在 supply_chain.py 基础上增强：
  1. 采购订单状态机（pending → approved → ordered → shipped → received → stocked）
  2. 库存状态机（normal → low_stock → critical → out_of_stock）
  3. 状态流转审计日志
  4. 自动库存更新（收货时）
  5. 库存预警触发补货建议

状态机:
  PROCUREMENT: pending → approved → [rejected，终态] → ordered → shipped → received → stocked
  INVENTORY:   normal ↔ low_stock ↔ critical ↔ out_of_stock
"""

import sys
import json
import uuid
from pathlib import Path
from datetime import datetime
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent


# ─────────────────────────────────────────
# 采购订单状态机
# ─────────────────────────────────────────

class ProcurementState:
    PENDING    = "pending"      # 待审批
    APPROVED   = "approved"     # 已审批
    REJECTED   = "rejected"     # 已驳回（终态）
    ORDERED    = "ordered"      # 已下单
    SHIPPED    = "shipped"      # 已发货
    RECEIVED   = "received"     # 已到货
    STOCKED    = "stocked"      # 已入库


PROCUREMENT_TRANSITIONS = {
    ProcurementState.PENDING:   {ProcurementState.APPROVED, ProcurementState.REJECTED},
    ProcurementState.APPROVED:  {ProcurementState.ORDERED, ProcurementState.REJECTED},
    ProcurementState.REJECTED:   set(),   # 终态
    ProcurementState.ORDERED:    {ProcurementState.SHIPPED},
    ProcurementState.SHIPPED:    {ProcurementState.RECEIVED},
    ProcurementState.RECEIVED:   {ProcurementState.STOCKED},
    ProcurementState.STOCKED:     set(),   # 终态
}


# ─────────────────────────────────────────
# 库存状态机
# ─────────────────────────────────────────

class InventoryState:
    NORMAL      = "normal"       # 正常
    LOW_STOCK   = "low_stock"    # 库存不足
    CRITICAL    = "critical"     # 严重不足
    OUT_OF_STOCK = "out_of_stock" # 缺货


# stock_ratio = current_stock / reorder_point
INVENTORY_THRESHOLDS = {
    InventoryState.OUT_OF_STOCK: 0.0,
    InventoryState.CRITICAL:      0.5,
    InventoryState.LOW_STOCK:     1.0,
    InventoryState.NORMAL:        2.0,
}


def compute_inventory_state(current_stock: float, reorder_point: float) -> str:
    if reorder_point <= 0:
        return InventoryState.NORMAL
    ratio = current_stock / reorder_point
    if ratio <= 0:
        return InventoryState.OUT_OF_STOCK
    elif ratio < 0.5:
        return InventoryState.CRITICAL
    elif ratio < 1.0:
        return InventoryState.LOW_STOCK
    elif ratio < 2.0:
        return InventoryState.NORMAL  # above reorder but below safety
    else:
        return InventoryState.NORMAL


# ─────────────────────────────────────────
# 数据库初始化
# ─────────────────────────────────────────

def ensure_tables(conn):
    """创建/确保状态机相关表"""
    # 状态流转日志
    conn.execute("""
        CREATE TABLE IF NOT EXISTS procurement_state_log (
            log_id      TEXT PRIMARY KEY,
            order_id    TEXT NOT NULL,
            from_state  TEXT,
            to_state    TEXT NOT NULL,
            actor       TEXT,
            reason      TEXT,
            metadata    TEXT DEFAULT '{}',
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 库存状态快照（定期更新）
    conn.execute("""
        CREATE TABLE IF NOT EXISTS inventory_state_snapshots (
            snapshot_id TEXT PRIMARY KEY,
            product_id  TEXT NOT NULL,
            state       TEXT NOT NULL,
            stock_ratio REAL,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_proc_log_order ON procurement_state_log(order_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_inv_snap_product ON inventory_state_snapshots(product_id)")


# ─────────────────────────────────────────
# 采购订单状态机
# ─────────────────────────────────────────

def procurement_transition(
    order_id: str,
    to_state: str,
    actor: str = "system",
    reason: str = None,
    conn=None,
) -> dict:
    """采购订单状态流转"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_tables(conn)
        conn.commit()

        # 获取当前状态
        row = conn.execute(
            "SELECT * FROM supply_orders WHERE order_id = ?", (order_id,)
        ).fetchone()
        if not row:
            return {"error": f"Order not found: {order_id}"}

        from_state = row["status"]

        if to_state not in PROCUREMENT_TRANSITIONS.get(from_state, set()):
            return {
                "error": f"Invalid transition: {from_state} → {to_state}",
                "order_id": order_id,
                "from_state": from_state,
                "available": list(PROCUREMENT_TRANSITIONS.get(from_state, set())),
            }

        now = datetime.now().isoformat()
        updates = {"status": to_state}
        if to_state == ProcurementState.APPROVED:
            updates["approved_at"] = now
        elif to_state == ProcurementState.SHIPPED:
            updates["shipped_at"] = now
        elif to_state == ProcurementState.RECEIVED:
            updates["delivered_at"] = now

        set_clause = ", ".join(f"{k} = ?" for k in updates)
        conn.execute(
            f"UPDATE supply_orders SET {set_clause} WHERE order_id = ?",
            (*updates.values(), order_id)
        )

        # 记录日志
        log_id = f"LOG-{uuid.uuid4().hex[:10].upper()}"
        conn.execute("""
            INSERT INTO procurement_state_log
            (log_id, order_id, from_state, to_state, actor, reason, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (log_id, order_id, from_state, to_state, actor,
              reason or f"{from_state} → {to_state}", now))

        conn.commit()

        # 如果是收货，自动更新库存
        auto_stock_update = None
        if to_state == ProcurementState.RECEIVED:
            auto_stock_update = _auto_add_stock(order_id, conn)

        return {
            "order_id": order_id,
            "from_state": from_state,
            "to_state": to_state,
            "actor": actor,
            "message": f"✅ 订单 {order_id}: {from_state} → {to_state}",
            "auto_stock_update": auto_stock_update,
            "available_transitions": list(PROCUREMENT_TRANSITIONS.get(to_state, set())),
        }

    finally:
        if own_conn:
            conn.close()


def _auto_add_stock(order_id: str, conn) -> dict:
    """收货时自动增加库存"""
    row = conn.execute(
        "SELECT product_id, quantity FROM supply_orders WHERE order_id = ?", (order_id,)
    ).fetchone()
    if not row:
        return None

    product_id = row["product_id"]
    qty = row["quantity"]

    # 更新库存
    conn.execute("""
        UPDATE pharmacy_inventory
        SET quantity = quantity + ?
        WHERE product_id = ?
    """, (qty, product_id))

    # 记录新库存状态
    new_stock = conn.execute(
        "SELECT quantity FROM pharmacy_inventory WHERE product_id = ?", (product_id,)
    ).fetchone()

    new_qty = new_stock["quantity"] if new_stock else qty

    return {
        "product_id": product_id,
        "added_quantity": qty,
        "new_stock": new_qty,
        "message": f"库存已更新: {product_id} +{qty} → {new_qty}",
    }


def create_procurement_order(
    product_id: str,
    quantity: int,
    unit_price: float = None,
    supplier: str = None,
    priority: str = "normal",
    ordered_by: str = "ai",
    notes: str = None,
    conn=None,
) -> dict:
    """创建采购订单（自动使用状态机）"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_tables(conn)
        conn.commit()

        order_id = f"PO-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

        total = (unit_price * quantity) if unit_price else 0

        conn.execute("""
            INSERT INTO supply_orders
            (order_id, product_id, quantity, unit_price, total_amount,
             supplier, status, priority, ordered_by, notes,
             created_at, approved_at, shipped_at, delivered_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order_id, product_id, quantity, unit_price, total,
            supplier, ProcurementState.PENDING, priority, ordered_by, notes,
            datetime.now().isoformat(), None, None, None
        ))

        # 记录初始状态
        log_id = f"LOG-{uuid.uuid4().hex[:10].upper()}"
        conn.execute("""
            INSERT INTO procurement_state_log
            (log_id, order_id, from_state, to_state, actor, reason, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (log_id, order_id, None, ProcurementState.PENDING, ordered_by,
              "订单创建", datetime.now().isoformat()))

        conn.commit()

        return {
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_amount": total,
            "status": ProcurementState.PENDING,
            "priority": priority,
            "available_transitions": list(PROCUREMENT_TRANSITIONS[ProcurementState.PENDING]),
            "suggestions": [f"订单 {order_id} 已创建，等待审批"],
        }

    finally:
        if own_conn:
            conn.close()


# ─────────────────────────────────────────
# 库存状态监控
# ─────────────────────────────────────────

def refresh_inventory_states(conn=None) -> dict:
    """
    扫描所有库存，更新状态快照
    返回: {products: [{product_id, name, current_stock, reorder_point, state, stock_ratio}]}
    """
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        ensure_tables(conn)
        conn.commit()

        rows = conn.execute("""
            SELECT product_id, product_name, quantity, reorder_point
            FROM pharmacy_inventory
        """).fetchall()

        updated = []
        alerts = []

        for r in rows:
            product_id = r["product_id"]
            current = r["quantity"] or 0
            reorder = r["reorder_point"] or 0
            state = compute_inventory_state(current, reorder)
            ratio = (current / reorder) if reorder > 0 else 999

            # 更新快照
            snap_id = f"SNAP-{product_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            conn.execute("""
                INSERT OR REPLACE INTO inventory_state_snapshots
                (snapshot_id, product_id, state, stock_ratio, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (snap_id, product_id, state, round(ratio, 2), datetime.now().isoformat()))

            updated.append({
                "product_id": product_id,
                "product_name": r["product_name"],
                "current_stock": current,
                "reorder_point": reorder,
                "state": state,
                "stock_ratio": round(ratio, 2),
            })

            if state in {InventoryState.CRITICAL, InventoryState.OUT_OF_STOCK}:
                alerts.append({
                    "product_id": product_id,
                    "product_name": r["product_name"],
                    "state": state,
                    "current_stock": current,
                    "reorder_point": reorder,
                })

        conn.commit()

        return {
            "total_products": len(updated),
            "state_counts": _count_by_state(updated),
            "products": updated,
            "alerts": alerts,
            "suggestions": _generate_restock_suggestions(alerts, updated),
        }

    finally:
        if own_conn:
            conn.close()


def _count_by_state(products: list[dict]) -> dict:
    counts = {}
    for p in products:
        s = p["state"]
        counts[s] = counts.get(s, 0) + 1
    return counts


def _generate_restock_suggestions(alerts: list[dict], all_products: list[dict]) -> list[str]:
    if not alerts:
        return ["库存状态全部正常"]

    suggestions = []
    critical = [a for a in alerts if a["state"] == InventoryState.CRITICAL]
    out_of = [a for a in alerts if a["state"] == InventoryState.OUT_OF_STOCK]

    if out_of:
        suggestions.append(f"🚨 {len(out_of)} 个产品缺货，需要立即补货！")
        for a in out_of:
            suggestions.append(f"  - {a['product_name']} ({a['product_id']}): 库存 {a['current_stock']}")
    if critical:
        suggestions.append(f"⚠️  {len(critical)} 个产品库存严重不足")
        for a in critical:
            suggestions.append(f"  - {a['product_name']} ({a['product_id']}): {a['current_stock']}/{a['reorder_point']}")

    return suggestions


# ─────────────────────────────────────────
# 供应链仪表盘
# ─────────────────────────────────────────

def supply_chain_dashboard(conn=None) -> dict:
    """供应链全局状态"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        # 采购订单统计
        order_stats = conn.execute("""
            SELECT status, COUNT(*) as cnt, SUM(total_amount) as total
            FROM supply_orders
            GROUP BY status
        """).fetchall()

        # 库存状态
        inv_result = refresh_inventory_states(conn)
        inv_states = inv_result["state_counts"]

        # 待处理订单
        pending = conn.execute("""
            SELECT order_id, product_id, quantity, priority, created_at
            FROM supply_orders
            WHERE status IN ('pending', 'approved')
            ORDER BY
                CASE priority WHEN 'urgent' THEN 1 WHEN 'high' THEN 2 ELSE 3 END,
                created_at ASC
            LIMIT 10
        """).fetchall()

        return {
            "order_stats": [
                {"status": r["status"], "count": r["cnt"], "total_amount": r["total"] or 0}
                for r in order_stats
            ],
            "inventory_states": inv_states,
            "pending_orders": [dict(r) for r in pending],
            "alerts": inv_result["alerts"],
            "suggestions": inv_result["suggestions"],
        }

    finally:
        if own_conn:
            conn.close()


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
    action = args.get("action", "dashboard")

    conn = get_conn()

    try:
        ensure_tables(conn)
        conn.commit()

        if action == "create_order":
            result = create_procurement_order(
                product_id=args["product_id"],
                quantity=args["quantity"],
                unit_price=args.get("unit_price"),
                supplier=args.get("supplier"),
                priority=args.get("priority", "normal"),
                ordered_by=args.get("ordered_by", "ai"),
                notes=args.get("notes"),
            )

        elif action == "transition":
            result = procurement_transition(
                order_id=args["order_id"],
                to_state=args["to_state"],
                actor=args.get("actor", "system"),
                reason=args.get("reason"),
            )

        elif action == "inventory_states":
            result = refresh_inventory_states()

        elif action == "dashboard":
            result = supply_chain_dashboard()

        elif action == "transitions":
            state = args.get("state")
            result = {
                "state": state,
                "available": list(PROCUREMENT_TRANSITIONS.get(state, set())),
                "all_states": {
                    "procurement": ProcurementState.__dict__,
                    "inventory": InventoryState.__dict__,
                },
            }

        else:
            result = {"error": f"Unknown action: {action}"}

        print(json.dumps(result, ensure_ascii=False, indent=2))

    finally:
        close_conn(conn)
