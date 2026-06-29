#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能保洁助手 - 数据库模块
SQLite 本地存储：保洁记录 / 用品库存 / 检查清单
"""

import sqlite3
import json
import sys
import os
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Optional

# Fix Windows GBK encoding for emoji output
import io
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SKILL_DIR = Path(__file__).parent.parent
DB_PATH = SKILL_DIR / "data" / "cleaning.db"

# ─── 房间分类 & 默认检查项 ───
ROOM_DEFAULTS = {
    "厨房":   ["台面擦拭","水槽清洗","灶台清洁","油烟机擦拭","地面拖洗","垃圾桶清理"],
    "卫生间": ["马桶刷洗","洗手台擦拭","镜面清洁","淋浴区清洁","地漏清理","换气扇除尘"],
    "客厅":   ["桌面整理","地面清扫拖洗","沙发吸尘","电视柜除尘","踢脚线清洁"],
    "卧室":   ["床铺整理","地面清扫","衣柜表面除尘","窗台擦拭","被褥晾晒"],
    "阳台":   ["地面清扫","晾衣架除尘","花盆整理","玻璃门擦拭"],
    "书房":   ["书桌整理","书架除尘","地面清扫","电子设备擦拭"],
    "玄关":   ["鞋柜整理","地面清扫","门垫清洁","大门擦拭"],
    "储物间": ["物品整理","地面清扫","货架除尘","过期物品清理"],
    "全屋":   ["窗户清洁","空调滤网清洗","踢脚线除尘","灯具除尘"],
}

ROOM_ALIASES = {
    "厕所": "卫生间", "洗手间": "卫生间", "wc": "卫生间", "bathroom": "卫生间",
    "主卧": "卧室", "次卧": "卧室", "儿童房": "卧室", "客房": "卧室",
    "起居室": "客厅", "livingroom": "客厅",
    "dining": "厨房", "kitchen": "厨房",
    "study": "书房", "办公室": "书房",
    "entry": "玄关", "门厅": "玄关",
    "储藏室": "储物间", "仓库": "储物间",
    "整体": "全屋", "全家": "全屋", "所有": "全屋",
}

DURATION_ESTIMATES = {
    "大扫除": 120, "彻底": 90, "深度": 60, "全面": 90,
    "常规": 30, "简单": 15, "快速": 10, "日常": 20,
    "拖地": 30, "扫地": 15, "吸尘": 20, "擦窗": 45,
    "擦灶台": 10, "刷马桶": 10, "整理": 20, "倒垃圾": 5,
}

SUPPLY_CATEGORIES = ["清洁剂", "工具", "耗材", "设备"]


def get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """初始化所有表"""
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS cleaning_records (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            date        TEXT NOT NULL,
            rooms       TEXT NOT NULL,
            items       TEXT,
            duration_min INTEGER NOT NULL DEFAULT 30,
            note        TEXT,
            created_at  TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS supplies (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT NOT NULL,
            category        TEXT NOT NULL,
            quantity        REAL NOT NULL DEFAULT 1,
            unit            TEXT NOT NULL DEFAULT '瓶',
            threshold       REAL NOT NULL DEFAULT 1,
            last_purchased  TEXT,
            note            TEXT,
            created_at      TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS checklists (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            room        TEXT NOT NULL,
            item        TEXT NOT NULL,
            frequency   TEXT NOT NULL DEFAULT 'weekly',
            priority    TEXT NOT NULL DEFAULT 'medium',
            enabled     INTEGER NOT NULL DEFAULT 1,
            created_at  TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE INDEX IF NOT EXISTS idx_records_date ON cleaning_records(date);
        CREATE INDEX IF NOT EXISTS idx_records_rooms ON cleaning_records(rooms);
        CREATE INDEX IF NOT EXISTS idx_supplies_cat ON supplies(category);
        CREATE INDEX IF NOT EXISTS idx_checklists_room ON checklists(room);
    """)
    conn.commit()
    conn.close()


# ─── 保洁记录 CRUD ───

def add_record(date_str: str, rooms: str, items: str, duration_min: int, note: str = "") -> int:
    """添加保洁记录，返回ID"""
    init_db()
    conn = get_conn()
    cur = conn.execute("""
        INSERT INTO cleaning_records (date, rooms, items, duration_min, note)
        VALUES (?, ?, ?, ?, ?)
    """, (date_str, rooms, items, duration_min, note))
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id


def delete_record(record_id: int) -> bool:
    """删除记录"""
    conn = get_conn()
    cur = conn.execute("DELETE FROM cleaning_records WHERE id=?", (record_id,))
    conn.commit()
    ok = cur.rowcount > 0
    conn.close()
    return ok


def list_records(year: int = None, month: int = None, room: str = None,
                 limit: int = 50, offset: int = 0) -> list:
    """查询保洁记录"""
    init_db()
    conn = get_conn()
    conditions = []
    params = []

    if year and month:
        conditions.append("date LIKE ?")
        params.append(f"{year:04d}-{month:02d}-%")
    elif year:
        conditions.append("date LIKE ?")
        params.append(f"{year:04d}-%")

    if room:
        conditions.append("rooms LIKE ?")
        params.append(f"%{room}%")

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    sql = f"SELECT * FROM cleaning_records {where} ORDER BY date DESC, id DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_recent(limit: int = 10) -> list:
    """最近N条记录"""
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM cleaning_records ORDER BY date DESC, id DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_summary(year: int = None, month: int = None) -> dict:
    """获取指定月份的保洁统计摘要"""
    init_db()
    conn = get_conn()

    if year is None:
        now = datetime.now()
        year, month = now.year, now.month

    date_filter = f"{year:04d}-{month:02d}-%" if month else f"{year:04d}-%"

    # 总览
    row = conn.execute("""
        SELECT COUNT(*) as total_count,
               SUM(duration_min) as total_duration,
               AVG(duration_min) as avg_duration
        FROM cleaning_records WHERE date LIKE ?
    """, (date_filter,)).fetchone()

    # 按日期统计
    daily = conn.execute("""
        SELECT date, COUNT(*) as cnt, SUM(duration_min) as dur
        FROM cleaning_records WHERE date LIKE ?
        GROUP BY date ORDER BY date
    """, (date_filter,)).fetchall()

    # 按房间统计
    rooms_count = {}
    all_records = conn.execute(
        "SELECT rooms, duration_min FROM cleaning_records WHERE date LIKE ?",
        (date_filter,)
    ).fetchall()
    for r in all_records:
        for room in r["rooms"].split(","):
            room = room.strip()
            if room:
                if room not in rooms_count:
                    rooms_count[room] = {"count": 0, "duration": 0}
                rooms_count[room]["count"] += 1
                rooms_count[room]["duration"] += r["duration_min"]

    # 活跃天数
    active_days = conn.execute("""
        SELECT COUNT(DISTINCT date) as days
        FROM cleaning_records WHERE date LIKE ?
    """, (date_filter,)).fetchone()["days"]

    conn.close()

    return {
        "year": year,
        "month": month,
        "total_count": row["total_count"] or 0,
        "total_duration": row["total_duration"] or 0,
        "avg_duration": round(row["avg_duration"] or 0, 1),
        "active_days": active_days or 0,
        "daily": [dict(d) for d in daily],
        "rooms": rooms_count,
    }


# ─── 保洁计划 ───

def ensure_checklists():
    """确保默认检查清单已录入"""
    init_db()
    conn = get_conn()
    for room, items in ROOM_DEFAULTS.items():
        for item in items:
            exists = conn.execute(
                "SELECT id FROM checklists WHERE room=? AND item=?", (room, item)
            ).fetchone()
            if not exists:
                freq = "daily" if room == "厨房" and item == "台面擦拭" else \
                       "daily" if room == "全屋" and item == "地面清扫" else \
                       "monthly" if "窗户" in item or "空调" in item or "灯具" in item or "窗帘" in item else \
                       "weekly"
                priority = "high" if "马桶" in item or "灶台" in item or "油烟机" in item else \
                           "medium"
                conn.execute(
                    "INSERT INTO checklists (room, item, frequency, priority) VALUES (?,?,?,?)",
                    (room, item, freq, priority)
                )
    conn.commit()
    conn.close()


def generate_plan(rooms: list = None) -> dict:
    """生成保洁计划"""
    ensure_checklists()
    conn = get_conn()

    query = "SELECT DISTINCT room, item, frequency, priority FROM checklists WHERE enabled=1"
    params = []
    if rooms:
        placeholders = ",".join("?" * len(rooms))
        query += f" AND room IN ({placeholders})"
        params = rooms
    query += " ORDER BY room, frequency, priority DESC"

    rows = conn.execute(query, params).fetchall()
    conn.close()

    plan = {"daily": [], "weekly": [], "monthly": [], "quarterly": []}
    for r in rows:
        room = r["room"]
        item = r["item"]
        freq = r["frequency"]
        plan[freq].append(f"{room}·{item}")

    return plan


# ─── 检查清单管理 ───

def checklist_add(room: str, item: str, frequency: str = "weekly", priority: str = "medium"):
    """添加检查项"""
    init_db()
    conn = get_conn()
    conn.execute(
        "INSERT INTO checklists (room, item, frequency, priority) VALUES (?,?,?,?)",
        (room, item, frequency, priority)
    )
    conn.commit()
    conn.close()
    return True


def checklist_list(room: str = None):
    """列出检查项"""
    init_db()
    conn = get_conn()
    if room:
        rows = conn.execute(
            "SELECT * FROM checklists WHERE room=? ORDER BY frequency, priority DESC",
            (room,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM checklists ORDER BY room, frequency, priority DESC"
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def checklist_delete(item_id: int):
    conn = get_conn()
    conn.execute("DELETE FROM checklists WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
    return True


# ─── 用品管理 ───

def supplies_list(category: str = None):
    """列出用品库存"""
    init_db()
    conn = get_conn()
    if category:
        rows = conn.execute(
            "SELECT * FROM supplies WHERE category=? ORDER BY name", (category,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM supplies ORDER BY category, name"
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def supplies_add(name: str, category: str, quantity: float = 1,
                 unit: str = "瓶", threshold: float = 1, note: str = ""):
    """添加或更新用品"""
    init_db()
    conn = get_conn()
    existing = conn.execute("SELECT id, quantity FROM supplies WHERE name=?", (name,)).fetchone()
    if existing:
        conn.execute(
            "UPDATE supplies SET quantity=quantity+?, last_purchased=date('now','localtime'), note=? WHERE id=?",
            (quantity, note, existing["id"])
        )
    else:
        conn.execute(
            "INSERT INTO supplies (name, category, quantity, unit, threshold, last_purchased, note) VALUES (?,?,?,?,?,date('now','localtime'),?)",
            (name, category, quantity, unit, threshold, note)
        )
    conn.commit()
    conn.close()
    return True


def supplies_use(name: str, amount: float = 1):
    """消耗用品"""
    init_db()
    conn = get_conn()
    # 模糊匹配
    row = conn.execute(
        "SELECT id, name, quantity, threshold FROM supplies WHERE name LIKE ?",
        (f"%{name}%",)
    ).fetchone()
    if not row:
        conn.close()
        return {"ok": False, "error": f"未找到用品: {name}"}
    new_qty = max(0, row["quantity"] - amount)
    threshold = row["threshold"]
    conn.execute("UPDATE supplies SET quantity=? WHERE id=?", (new_qty, row["id"]))
    conn.commit()
    conn.close()
    return {
        "ok": True,
        "name": row["name"],
        "old_quantity": row["quantity"],
        "new_quantity": new_qty,
        "low": new_qty <= threshold
    }


def supplies_alerts():
    """低库存提醒"""
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM supplies WHERE quantity <= threshold ORDER BY quantity ASC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── 辅助函数 ───

def normalize_room(room_text: str) -> str:
    """标准化房间名"""
    room_text = room_text.strip()
    if room_text in ROOM_ALIASES:
        return ROOM_ALIASES[room_text]
    if room_text in ROOM_DEFAULTS:
        return room_text
    # 模糊匹配
    for std_name in ROOM_DEFAULTS:
        if std_name in room_text or room_text in std_name:
            return std_name
    return room_text


def estimate_duration(user_text: str, rooms_count: int = 1) -> int:
    """根据文本估算耗时"""
    text = user_text.lower()
    for keyword, dur in sorted(DURATION_ESTIMATES.items(), key=lambda x: -len(x[0])):
        if keyword in text:
            return dur * rooms_count
    return 30 * rooms_count


def extract_rooms(text: str) -> list:
    """从文本提取房间列表"""
    found = set()
    for std_name in ROOM_DEFAULTS:
        if std_name in text:
            found.add(std_name)
    for alias, std_name in ROOM_ALIASES.items():
        if alias in text:
            found.add(std_name)
    if not found:
        # 尝试关键词匹配
        if any(w in text for w in ["灶台","油烟机","洗碗","水槽","冰箱","微波炉","锅"]):
            found.add("厨房")
        if any(w in text for w in ["马桶","厕所","淋浴","浴缸","洗手台","地漏","沐浴"]):
            found.add("卫生间")
        if any(w in text for w in ["沙发","电视","茶几"]):
            found.add("客厅")
        if any(w in text for w in ["床","被子","枕头","衣柜","被褥"]):
            found.add("卧室")
        if any(w in text for w in ["窗户","窗","玻璃","纱窗"]):
            found.add("全屋")
    if not found:
        found.add("全屋")
    return list(found)


def extract_duration(text: str) -> int:
    """提取时长（分钟）"""
    import re
    # 匹配 N小时/N分钟/N小时N分钟
    hours = 0
    mins = 0
    h_match = re.search(r'(\d+)\s*小时|(\d+)\s*个?钟头|(\d+)\s*h', text)
    if h_match:
        hours = int(h_match.group(1) or h_match.group(2) or h_match.group(3) or 0)
    m_match = re.search(r'(\d+)\s*分钟|(\d+)\s*分(?!钟头)|(\d+)\s*min', text)
    if m_match:
        mins = int(m_match.group(1) or m_match.group(2) or m_match.group(3) or 0)
    total = hours * 60 + mins
    if total > 0:
        return total
    return 0


# ─────────────────────────────────────────
# CLI 接口
# ─────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: cleaning_db.py <command> [args...]",
            "commands": ["init","add","list","recent","delete","summary",
                        "plan","checklist","supplies"]
        }, ensure_ascii=False))
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "init":
        init_db()
        ensure_checklists()
        print(json.dumps({"ok": True, "db": str(DB_PATH), "message": "数据库已初始化"},
                        ensure_ascii=False))

    elif cmd == "add":
        # add <date> <rooms> <items> <duration_min> [note]
        date_str = sys.argv[2]
        rooms = sys.argv[3]
        items = sys.argv[4] if len(sys.argv) > 4 else ""
        duration = int(sys.argv[5]) if len(sys.argv) > 5 else 30
        note = sys.argv[6] if len(sys.argv) > 6 else ""
        row_id = add_record(date_str, rooms, items, duration, note)
        print(json.dumps({"ok": True, "id": row_id, "message": f"✅ 已记录 #{row_id}"},
                        ensure_ascii=False))

    elif cmd == "list":
        year = int(sys.argv[2]) if len(sys.argv) > 2 else None
        month = int(sys.argv[3]) if len(sys.argv) > 3 else None
        room = sys.argv[4] if len(sys.argv) > 4 else None
        limit = int(sys.argv[5]) if len(sys.argv) > 5 else 50
        offset = int(sys.argv[6]) if len(sys.argv) > 6 else 0
        rows = list_records(year=year, month=month, room=room, limit=limit, offset=offset)
        print(json.dumps(rows, ensure_ascii=False))

    elif cmd == "recent":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        rows = get_recent(limit)
        print(json.dumps(rows, ensure_ascii=False))

    elif cmd == "delete":
        record_id = int(sys.argv[2])
        ok = delete_record(record_id)
        print(json.dumps({"ok": ok}, ensure_ascii=False))

    elif cmd == "summary":
        year = int(sys.argv[2]) if len(sys.argv) > 2 else None
        month = int(sys.argv[3]) if len(sys.argv) > 3 else None
        result = get_summary(year=year, month=month)
        print(json.dumps(result, ensure_ascii=False))

    elif cmd == "plan":
        rooms = sys.argv[2].split(",") if len(sys.argv) > 2 else None
        plan = generate_plan(rooms)
        print(json.dumps(plan, ensure_ascii=False))

    elif cmd == "checklist":
        sub = sys.argv[2] if len(sys.argv) > 2 else "list"
        if sub == "add":
            room = sys.argv[3]
            item = sys.argv[4]
            freq = sys.argv[5] if len(sys.argv) > 5 else "weekly"
            priority = sys.argv[6] if len(sys.argv) > 6 else "medium"
            checklist_add(room, item, freq, priority)
            print(json.dumps({"ok": True, "message": f"已添加 {room}·{item}"},
                            ensure_ascii=False))
        elif sub == "list":
            room = sys.argv[3] if len(sys.argv) > 3 else None
            rows = checklist_list(room)
            print(json.dumps(rows, ensure_ascii=False))
        elif sub == "delete":
            item_id = int(sys.argv[3])
            checklist_delete(item_id)
            print(json.dumps({"ok": True}, ensure_ascii=False))

    elif cmd == "supplies":
        sub = sys.argv[2] if len(sys.argv) > 2 else "list"
        if sub == "list":
            category = sys.argv[3] if len(sys.argv) > 3 else None
            rows = supplies_list(category)
            print(json.dumps(rows, ensure_ascii=False))
        elif sub == "add":
            name = sys.argv[3]
            category = sys.argv[4]
            qty = float(sys.argv[5]) if len(sys.argv) > 5 else 1
            unit = sys.argv[6] if len(sys.argv) > 6 else "瓶"
            threshold = float(sys.argv[7]) if len(sys.argv) > 7 else 1
            note = sys.argv[8] if len(sys.argv) > 8 else ""
            supplies_add(name, category, qty, unit, threshold, note)
            print(json.dumps({"ok": True, "message": f"已更新 {name}"},
                            ensure_ascii=False))
        elif sub == "use":
            name = sys.argv[3]
            amount = float(sys.argv[4]) if len(sys.argv) > 4 else 1
            result = supplies_use(name, amount)
            print(json.dumps(result, ensure_ascii=False))
        elif sub == "alert":
            alerts = supplies_alerts()
            print(json.dumps(alerts, ensure_ascii=False))

    else:
        print(json.dumps({"error": f"Unknown command: {cmd}"}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
