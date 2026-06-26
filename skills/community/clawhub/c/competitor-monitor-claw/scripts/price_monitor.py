#!/usr/bin/env python3
"""
竞品监控核心脚本
用法：
  python3 price_monitor.py init                          # 初始化数据库
  python3 price_monitor.py add --csv ./competitors.csv  # 从 CSV 导入竞品列表
  python3 price_monitor.py check                        # 立即检查所有竞品（模拟采集）
  python3 price_monitor.py report --days 30             # 生成近 N 天竞品报告
  python3 price_monitor.py events --limit 20            # 查看最近变化事件
"""

import argparse
import csv
import json
import os
import random
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "competitor_monitor.db"


def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS competitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            platform TEXT NOT NULL,
            product_url TEXT NOT NULL,
            sku_id TEXT,
            alert_threshold REAL DEFAULT 0.05,
            monitor_freq TEXT DEFAULT 'daily',
            owner TEXT,
            active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        );

        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            competitor_id INTEGER REFERENCES competitors(id),
            price REAL NOT NULL,
            promo_price REAL,
            review_count INTEGER,
            rating REAL,
            recorded_at TEXT DEFAULT (datetime('now', 'localtime'))
        );

        CREATE TABLE IF NOT EXISTS change_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            competitor_id INTEGER REFERENCES competitors(id),
            event_type TEXT,
            old_value TEXT,
            new_value TEXT,
            change_pct REAL,
            detected_at TEXT DEFAULT (datetime('now', 'localtime')),
            notified INTEGER DEFAULT 0
        );
    """)
    conn.commit()
    conn.close()
    print("[OK] 数据库初始化完成:", DB_PATH)


def add_from_csv(csv_path):
    conn = get_conn()
    added = 0
    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            conn.execute("""
                INSERT INTO competitors (name, platform, product_url, sku_id, alert_threshold, monitor_freq, owner)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                row.get('name', '').strip(),
                row.get('platform', 'jd').strip(),
                row.get('product_url', '').strip(),
                row.get('sku_id', '').strip() or None,
                float(row.get('alert_threshold', 0.05)),
                row.get('monitor_freq', 'daily').strip(),
                row.get('owner', '').strip() or None,
            ))
            added += 1
    conn.commit()
    conn.close()
    print(f"[OK] 已导入 {added} 条竞品记录")


def simulate_fetch(competitor):
    """
    模拟采集竞品数据（实际部署时替换为真实爬虫逻辑）
    返回 dict: price, promo_price, review_count, rating
    """
    base_price = 299.0 + (competitor['id'] * 37.5) % 500
    # 模拟小幅价格波动
    price = round(base_price * (1 + random.uniform(-0.08, 0.08)), 2)
    promo_price = round(price * random.uniform(0.85, 0.98), 2) if random.random() > 0.6 else None
    review_count = 1000 + competitor['id'] * 200 + random.randint(-50, 200)
    rating = round(random.uniform(4.3, 4.9), 1)
    return {
        "price": price,
        "promo_price": promo_price,
        "review_count": review_count,
        "rating": rating,
    }


def check_all():
    conn = get_conn()
    competitors = conn.execute("SELECT * FROM competitors WHERE active=1").fetchall()
    if not competitors:
        print("[!] 没有活跃的竞品，请先用 add --csv 导入竞品列表")
        conn.close()
        return

    events = []
    for comp in competitors:
        data = simulate_fetch(comp)

        # 获取上次价格
        last = conn.execute(
            "SELECT price FROM price_history WHERE competitor_id=? ORDER BY recorded_at DESC LIMIT 1",
            (comp['id'],)
        ).fetchone()

        # 记录本次快照
        conn.execute("""
            INSERT INTO price_history (competitor_id, price, promo_price, review_count, rating)
            VALUES (?, ?, ?, ?, ?)
        """, (comp['id'], data['price'], data['promo_price'], data['review_count'], data['rating']))

        # 检测价格变化
        if last:
            old_price = last['price']
            change_pct = (data['price'] - old_price) / old_price
            threshold = comp['alert_threshold']
            if abs(change_pct) >= threshold:
                event_type = 'price_drop' if change_pct < 0 else 'price_rise'
                conn.execute("""
                    INSERT INTO change_events (competitor_id, event_type, old_value, new_value, change_pct)
                    VALUES (?, ?, ?, ?, ?)
                """, (comp['id'], event_type, str(old_price), str(data['price']), round(change_pct * 100, 2)))
                events.append({
                    "name": comp['name'],
                    "event": event_type,
                    "old": old_price,
                    "new": data['price'],
                    "pct": round(change_pct * 100, 2),
                })

        print(f"  [{comp['platform'].upper()}] {comp['name']}: ¥{data['price']}"
              + (f" (促销价 ¥{data['promo_price']})" if data['promo_price'] else "")
              + f" | 评分 {data['rating']} | 评价数 {data['review_count']}")

    conn.commit()
    conn.close()

    print(f"\n[OK] 检查完成，共 {len(competitors)} 个竞品")
    if events:
        print(f"\n⚠️  触发预警 {len(events)} 条：")
        for e in events:
            direction = "↓降价" if e['event'] == 'price_drop' else "↑涨价"
            print(f"  {e['name']}: {direction} {abs(e['pct'])}%  ¥{e['old']} → ¥{e['new']}")
    else:
        print("  无价格预警")


def generate_report(days=30):
    conn = get_conn()
    since = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')

    competitors = conn.execute("SELECT * FROM competitors WHERE active=1").fetchall()
    if not competitors:
        print("[!] 没有竞品数据")
        conn.close()
        return

    print(f"\n{'='*60}")
    print(f"  竞品监控报告（近 {days} 天）")
    print(f"  生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")

    for comp in competitors:
        prices = conn.execute("""
            SELECT price, promo_price, rating, review_count, recorded_at
            FROM price_history
            WHERE competitor_id=? AND recorded_at >= ?
            ORDER BY recorded_at ASC
        """, (comp['id'], since)).fetchall()

        events = conn.execute("""
            SELECT event_type, old_value, new_value, change_pct, detected_at
            FROM change_events
            WHERE competitor_id=? AND detected_at >= ?
            ORDER BY detected_at DESC
        """, (comp['id'], since)).fetchall()

        print(f"▶ {comp['name']} [{comp['platform'].upper()}]")
        if prices:
            price_list = [p['price'] for p in prices]
            latest = prices[-1]
            print(f"  当前价格：¥{latest['price']}"
                  + (f"（促销价 ¥{latest['promo_price']}）" if latest['promo_price'] else ""))
            print(f"  价格区间：¥{min(price_list):.2f} – ¥{max(price_list):.2f}")
            print(f"  评分：{latest['rating']}  |  评价数：{latest['review_count']}")
        else:
            print("  暂无采集数据")

        if events:
            print(f"  变化事件（{len(events)} 条）：")
            for e in events[:5]:
                direction = "↓降价" if e['event_type'] == 'price_drop' else "↑涨价"
                print(f"    {e['detected_at'][:10]} {direction} {abs(e['change_pct'])}%  ¥{e['old_value']} → ¥{e['new_value']}")
        else:
            print("  无价格变化事件")
        print()

    conn.close()


def show_events(limit=20):
    conn = get_conn()
    rows = conn.execute("""
        SELECT c.name, c.platform, e.event_type, e.old_value, e.new_value, e.change_pct, e.detected_at
        FROM change_events e
        JOIN competitors c ON c.id = e.competitor_id
        ORDER BY e.detected_at DESC
        LIMIT ?
    """, (limit,)).fetchall()

    if not rows:
        print("[!] 暂无变化事件记录")
    else:
        print(f"\n最近 {limit} 条变化事件：\n")
        for r in rows:
            direction = "↓降价" if r['event_type'] == 'price_drop' else "↑涨价"
            print(f"  {r['detected_at'][:16]}  [{r['platform'].upper()}] {r['name']}: "
                  f"{direction} {abs(r['change_pct'])}%  ¥{r['old_value']} → ¥{r['new_value']}")
    conn.close()


def main():
    parser = argparse.ArgumentParser(description='竞品监控工具')
    sub = parser.add_subparsers(dest='cmd')

    sub.add_parser('init', help='初始化数据库')

    p_add = sub.add_parser('add', help='从 CSV 导入竞品')
    p_add.add_argument('--csv', required=True, help='CSV 文件路径')

    sub.add_parser('check', help='立即检查所有竞品价格')

    p_report = sub.add_parser('report', help='生成竞品报告')
    p_report.add_argument('--days', type=int, default=30, help='报告天数范围（默认30天）')

    p_events = sub.add_parser('events', help='查看变化事件')
    p_events.add_argument('--limit', type=int, default=20, help='显示条数')

    args = parser.parse_args()

    if args.cmd == 'init':
        init_db()
    elif args.cmd == 'add':
        init_db()
        add_from_csv(args.csv)
    elif args.cmd == 'check':
        init_db()
        check_all()
    elif args.cmd == 'report':
        generate_report(args.days)
    elif args.cmd == 'events':
        show_events(args.limit)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
