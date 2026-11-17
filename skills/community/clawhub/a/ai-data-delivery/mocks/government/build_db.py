#!/usr/bin/env python3
"""build_db.py — 政务·民生服务场景：生成确定性 SQLite 物理库（domain.db）。

业务故事：一个政务服务大厅的办件数据。办件表 service_request（一行一件办件），
典型问数：办件量、按期办结率、满意度、渠道分布。信息中心人员是该场景的主力用户。
造数完全确定，gold 可用 SQL 复算。
"""
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "domain.db")

CATS = ["社保", "医保", "户籍", "公积金", "税务"]
CHANNELS = ["窗口", "网办", "电话"]
STATUS = ["按期办结", "超期办结", "办理中"]


def build():
    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    conn.executescript("""
    CREATE TABLE service_request (
        req_id TEXT PRIMARY KEY,
        req_date TEXT NOT NULL,
        category TEXT NOT NULL,
        channel TEXT NOT NULL,
        status TEXT NOT NULL,
        satisfaction INTEGER NOT NULL
    );
    """)
    for i in range(1, 151):
        conn.execute("INSERT INTO service_request VALUES (?,?,?,?,?,?)",
                     (f"G{i:04d}", f"2026-{((i - 1) % 6) + 1:02d}-{((i - 1) % 28) + 1:02d}",
                      CATS[i % 5], CHANNELS[(i // 3) % 3], STATUS[(i // 7) % 3],
                      1 + (i * 7) % 5))
    conn.commit()
    n = conn.execute("SELECT COUNT(*) FROM service_request").fetchone()[0]
    conn.close()
    print(f"建库完成：{DB}（service_request {n} 行）")


if __name__ == "__main__":
    build()
