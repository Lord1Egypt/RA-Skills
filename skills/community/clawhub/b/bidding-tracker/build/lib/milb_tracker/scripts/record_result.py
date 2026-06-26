#!/usr/bin/env python3
"""
录入开标结果，同步更新项目状态为 won 或 lost。

用法：
    python3 scripts/record_result.py \
        --project-id 1 \
        --our-price 980000 \
        --winning-price 950000 \
        --winner "某某公司" \
        --won false \
        --notes "排名第二，差距3万"
"""

import argparse
import json
import os
import sqlite3
import sys

from milb_tracker.config import get_db_path

DB_PATH = get_db_path()


def get_conn():
    conn = sqlite3.connect(os.path.abspath(DB_PATH), timeout=10.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def record(project_id: int, our_price: float | None, winning_price: float | None,
           winner: str | None, is_won: bool, notes: str | None):
    """写入开标结果并更新项目状态。"""
    conn = get_conn()
    try:
        row = conn.execute(
            "SELECT status FROM projects WHERE id=?", (project_id,)).fetchone()
        if row is None:
            print(json.dumps({"error": f"项目不存在：{project_id}", "code": 1}, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)
        if row[0] != 'opened':
            print(json.dumps(
                {"error": f"项目当前状态 '{row[0]}' 不允许录入结果，仅opened状态可录入", "code": 1},
                ensure_ascii=False), file=sys.stderr)
            sys.exit(1)

        conn.execute(
            "INSERT INTO bid_results"
            " (project_id, our_bid_price, winning_price, winner, is_winner, notes)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (project_id, our_price, winning_price, winner, int(is_won), notes))
        new_status = 'won' if is_won else 'lost'
        conn.execute(
            "UPDATE projects SET status=?, updated_at=datetime('now','localtime')"
            " WHERE id=?",
            (new_status, project_id))
        conn.commit()
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description='录入开标结果')
    parser.add_argument('--project-id', type=int, required=True, help='项目 ID')
    parser.add_argument('--our-price', type=float, help='我方报价（元）')
    parser.add_argument('--winning-price', type=float, help='中标价格（元）')
    parser.add_argument('--winner', help='中标单位名称')
    parser.add_argument('--won', required=True, choices=['true', 'false'], help='是否中标')
    parser.add_argument('--notes', help='备注（评分、排名等现场情况）')
    args = parser.parse_args()

    is_won = args.won == 'true'
    record(args.project_id, args.our_price, args.winning_price, args.winner, is_won, args.notes)

    result_text = "中标" if is_won else "未中标"
    print(json.dumps({"status": "ok", "message": f"项目 {args.project_id} 开标结果已录入：{result_text}", "new_status": result_text}, ensure_ascii=False))
    sys.exit(0)


if __name__ == '__main__':
    main()
