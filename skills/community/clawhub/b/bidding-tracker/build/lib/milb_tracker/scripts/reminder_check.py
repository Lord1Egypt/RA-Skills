#!/usr/bin/env python3
"""
扫描所有活跃项目，判断是否需要发送提醒，输出 JSON 数组。
由 Cron 每日调用两次（8:47 / 17:53 工作日）。

提醒规则：
  - 购买截止 ≤ 3 天 且 未购买      → doc_purchase    → manager
  - 封标建议时间 ≤ 2 天 且 未封标   → seal_warning    → manager
  - 开标时间 ≤ 1 天                → bid_opening     → manager + director

输出格式（JSON 数组）：
[
  {
    "project_id": 1,
    "project_name": "xxx项目",
    "reminder_type": "doc_purchase",
    "recipient_role": "manager",
    "project_manager": "张三",
    "message": "..."
  },
  ...
]

若无待提醒项，输出空数组 []，Agent 应静默退出。
"""

import json
import os
import sqlite3
import sys
from datetime import datetime, timedelta

from milb_tracker.config import get_db_path

DB_PATH = get_db_path()

ACTIVE_STATUSES = ('registered', 'doc_pending', 'doc_purchased', 'preparing', 'sealed')


def get_conn():
    conn = sqlite3.connect(os.path.abspath(DB_PATH), timeout=10.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def is_already_sent(conn, project_id: int, reminder_type: str) -> bool:
    """检查今日是否已发送同类型提醒。"""
    cur = conn.execute(
        "SELECT COUNT(*) FROM reminders "
        "WHERE project_id = ? AND reminder_type = ? "
        "AND DATE(sent_at) = DATE('now', 'localtime')",
        (project_id, reminder_type))
    return cur.fetchone()[0] > 0


def record_sent(conn, project_id: int, reminder_type: str, recipient_role: str):
    """记录已发送的提醒。"""
    conn.execute(
        "INSERT INTO reminders (project_id, reminder_type, recipient_role) VALUES (?, ?, ?)",
        (project_id, reminder_type, recipient_role))


def check_reminders() -> list:
    """扫描活跃项目，返回需要发送的提醒列表，并写入 reminders 表。"""
    conn = get_conn()
    try:
        placeholders = ','.join(['?'] * len(ACTIVE_STATUSES))
        cur = conn.execute(
            f"SELECT id, project_name, project_manager, status,"
            f" doc_purchase_deadline, suggested_seal_time, bid_opening_time"
            f" FROM projects WHERE status IN ({placeholders})",
            ACTIVE_STATUSES)
        cols = [d[0] for d in cur.description]
        projects = [dict(zip(cols, row)) for row in cur.fetchall()]
    except Exception as e:
        conn.close()
        print(json.dumps({"error": f"数据库连接失败: {e}", "code": 1}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    def parse_dt(s):
        try:
            return datetime.fromisoformat(s) if s else None
        except ValueError:
            return None

    now = datetime.now()
    reminders = []

    for p in projects:
        pid = p['id']
        name = p['project_name']
        manager = p['project_manager']
        status = p['status']

        # 规则 1：标书购买截止 ≤ 3 天且未购买
        if status in ('registered', 'doc_pending'):
            dl = parse_dt(p['doc_purchase_deadline'])
            if dl and timedelta(0) <= (dl - now) <= timedelta(days=3):
                if not is_already_sent(conn, pid, 'doc_purchase'):
                    reminders.append({
                        "project_id": pid,
                        "project_name": name,
                        "reminder_type": "doc_purchase",
                        "recipient_role": "manager",
                        "project_manager": manager,
                        "message": (
                            f"【标书购买提醒】{name} 购买截止 {dl.strftime('%Y-%m-%d')}，"
                            f"请尽快办理"
                        ),
                    })
                    record_sent(conn, pid, 'doc_purchase', 'manager')

        # 规则 2：建议封标时间 ≤ 2 天且未封标
        if status in ('registered', 'doc_pending', 'doc_purchased', 'preparing'):
            seal = parse_dt(p['suggested_seal_time'])
            if seal and timedelta(0) <= (seal - now) <= timedelta(days=2):
                if not is_already_sent(conn, pid, 'seal_warning'):
                    reminders.append({
                        "project_id": pid,
                        "project_name": name,
                        "reminder_type": "seal_warning",
                        "recipient_role": "manager",
                        "project_manager": manager,
                        "message": (
                            f"【封标提醒】{name} 建议封标时间 {seal.strftime('%Y-%m-%d')}，"
                            f"请确认制标进度"
                        ),
                    })
                    record_sent(conn, pid, 'seal_warning', 'manager')

        # 规则 3：开标时间 ≤ 1 天 → 同时通知 manager 和 director
        opening = parse_dt(p['bid_opening_time'])
        if opening and timedelta(0) <= (opening - now) <= timedelta(days=1):
            if not is_already_sent(conn, pid, 'bid_opening'):
                for role in ("manager", "director"):
                    reminders.append({
                        "project_id": pid,
                        "project_name": name,
                        "reminder_type": "bid_opening",
                        "recipient_role": role,
                        "project_manager": manager,
                        "message": (
                            f"【开标提醒】{name} 开标时间 "
                            f"{opening.strftime('%Y-%m-%d %H:%M')}，请做好准备"
                        ),
                    })
                # 去重表只写1条（manager角色），is_already_sent 按 project_id+type+DATE 检查，与角色无关
                record_sent(conn, pid, 'bid_opening', 'manager')

    conn.commit()
    conn.close()
    return reminders


def main():
    reminders = check_reminders()
    print(json.dumps(reminders or [], ensure_ascii=False, indent=2))
    sys.exit(0)


if __name__ == '__main__':
    main()
