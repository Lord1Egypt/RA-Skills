#!/usr/bin/env python3
"""
注册新招投标项目。

接收从招标公告（PDF/PNG）中提取的结构化信息，写入数据库，
自动生成项目编号，推算建议封标时间，并将附件移动到正确路径。

用法：
    python3 scripts/register_project.py --json '{"project_name": "...", ...}' --manager-name "张经理"
    python3 scripts/register_project.py --json '...' --manager-name "张经理" --travel-days 3
    python3 scripts/register_project.py --json '...' --manager-name "张经理" --announcement-file /tmp/xxx.pdf
"""

import argparse
import json
import os
import shutil
import sqlite3
import sys
from datetime import datetime, timedelta

from milb_tracker.config import get_db_path, get_attachments_dir

DB_PATH = get_db_path()
ATTACHMENTS_DIR = get_attachments_dir()


def get_conn():
    conn = sqlite3.connect(os.path.abspath(DB_PATH), timeout=10.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


# 支持的字段（与数据库列名对应）
ALLOWED_FIELDS = [
    'project_name', 'budget', 'procurer', 'bid_agency',
    'manager_contact',
    'registration_deadline', 'registration_location',
    'doc_purchase_location', 'doc_purchase_price', 'doc_purchase_deadline',
    'doc_required_materials',
    'bid_opening_time', 'bid_opening_location',
]


def calc_suggested_seal_time(bid_opening_time: str, travel_days: int) -> str | None:
    """根据开标时间和运输天数推算建议封标时间，自动避开周末（退到周五）。"""
    try:
        opening = datetime.fromisoformat(bid_opening_time)
    except (ValueError, TypeError):
        return None
    suggested = opening - timedelta(days=travel_days)
    weekday = suggested.weekday()  # 0=Mon, 5=Sat, 6=Sun
    if weekday == 5:               # 周六 → 周五
        suggested -= timedelta(days=1)
    elif weekday == 6:             # 周日 → 周五
        suggested -= timedelta(days=2)
    return suggested.strftime("%Y-%m-%dT%H:%M:%S")


def generate_project_no(conn) -> str:
    """按 YYYY-NNN 格式自动生成 project_no。"""
    year = datetime.now().year
    cur = conn.execute(
        "SELECT MAX(CAST(SUBSTR(project_no, 6) AS INTEGER)) FROM projects WHERE project_no LIKE ?",
        (f"{year}-%",))
    max_seq = cur.fetchone()[0]
    seq = (max_seq or 0) + 1
    return f"{year}-{seq:03d}"


def move_announcement(src: str, project_id: int) -> str:
    """将公告文件移动到 data/attachments/{project_id}/ 目录。"""
    dest_dir = os.path.abspath(os.path.join(ATTACHMENTS_DIR, str(project_id)))
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, os.path.basename(src))
    shutil.move(src, dest)
    return dest


def register(data: dict, manager_name: str, travel_days: int, announcement_file: str | None) -> dict:
    """
    将项目数据写入数据库，返回包含 project_id, project_no 等信息的 dict。
    """
    # 过滤只保留合法字段
    fields = {k: v for k, v in data.items() if k in ALLOWED_FIELDS}

    # 列表型字段序列化为 JSON 字符串
    if isinstance(fields.get('doc_required_materials'), list):
        fields['doc_required_materials'] = json.dumps(
            fields['doc_required_materials'], ensure_ascii=False)

    # 设置必填字段
    fields['project_manager'] = manager_name
    fields['travel_days'] = travel_days

    # 推算建议封标时间
    suggested = calc_suggested_seal_time(fields.get('bid_opening_time'), travel_days)
    if suggested:
        fields['suggested_seal_time'] = suggested

    conn = get_conn()
    attachment_dir = None
    try:
        # 生成 project_no（需要连接才能查询）
        project_no = generate_project_no(conn)
        fields['project_no'] = project_no

        columns = list(fields.keys())
        placeholders = ', '.join(['?'] * len(columns))
        col_clause = ', '.join(columns)
        values = [fields[c] for c in columns]

        cur = conn.execute(
            f"INSERT INTO projects ({col_clause}) VALUES ({placeholders})",
            values)
        conn.commit()
        project_id = cur.lastrowid

        # 移动公告文件
        if announcement_file and os.path.exists(announcement_file):
            dest = move_announcement(announcement_file, project_id)
            conn.execute(
                "UPDATE projects SET announcement_path=? WHERE id=?",
                (dest, project_id))
            conn.commit()
            attachment_dir = os.path.dirname(dest)
        else:
            attachment_dir = os.path.join(os.path.abspath(ATTACHMENTS_DIR), str(project_id))

        return {
            "project_id": project_id,
            "project_no": project_no,
            "project_name": fields.get('project_name', ''),
            "suggested_seal_time": suggested or '',
            "attachment_dir": attachment_dir,
        }
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description='注册新招投标项目')
    parser.add_argument('--json', required=True, help='项目信息 JSON 字符串')
    parser.add_argument('--manager-name', required=True, help='指派的项目负责人姓名')
    parser.add_argument('--travel-days', type=int, default=2, help='运输/路程天数（用于推算封标时间）')
    parser.add_argument('--announcement-file', help='招标公告文件路径（PDF/PNG），由 Tool 层从 __context__ 拦截后传入')
    args = parser.parse_args()

    try:
        data = json.loads(args.json)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON 解析失败：{e}", "code": 1}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    result = register(data, args.manager_name, args.travel_days, args.announcement_file)
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0)


if __name__ == '__main__':
    main()
