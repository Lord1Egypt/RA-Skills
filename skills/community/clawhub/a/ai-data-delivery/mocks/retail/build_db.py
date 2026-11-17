#!/usr/bin/env python3
"""build_db.py — 零售电商·销售运营场景：生成确定性 SQLite 物理库（domain.db）。

业务故事：一家全渠道零售商，订单表 orders 是事实表（一行一笔订单），
客户表 customers 是维度表（一行一个客户）。典型问数：订单量、GMV、退款率、金卡客户数。
造数完全确定（无随机数），gold 期望可用 SQL 复算。
"""
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "domain.db")

CHANNELS = ["线上", "线下", "直播"]
STATUS = ["已完成", "已退款", "待付款"]
LEVELS = ["普通", "银卡", "金卡"]
REGIONS = ["华东", "华北", "华南", "西南"]


def build():
    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    conn.executescript("""
    CREATE TABLE customers (
        customer_id TEXT PRIMARY KEY,
        level TEXT NOT NULL,
        region TEXT NOT NULL,
        register_date TEXT NOT NULL
    );
    CREATE TABLE orders (
        order_id TEXT PRIMARY KEY,
        order_date TEXT NOT NULL,
        channel TEXT NOT NULL,
        status TEXT NOT NULL,
        amount REAL NOT NULL,
        customer_id TEXT NOT NULL REFERENCES customers(customer_id)
    );
    """)
    # 40 个客户：level/region 按序号轮转，完全确定
    for i in range(1, 41):
        conn.execute(
            "INSERT INTO customers VALUES (?,?,?,?)",
            (f"C{i:03d}", LEVELS[i % 3], REGIONS[i % 4], f"2026-0{(i % 6) + 1}-15"))
    # 120 笔订单：渠道/状态错相位轮转（避免两列完全相关）；金额 = 100 + (i*7)%400
    for i in range(1, 121):
        conn.execute(
            "INSERT INTO orders VALUES (?,?,?,?,?,?)",
            (f"O{i:04d}", f"2026-{((i - 1) % 6) + 1:02d}-{((i - 1) % 28) + 1:02d}",
             CHANNELS[i % 3], STATUS[(i // 3) % 3], 100 + (i * 7) % 400, f"C{(i % 40) + 1:03d}"))
    conn.commit()
    n_c = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    n_o = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    conn.close()
    print(f"建库完成：{DB}（customers {n_c} 行 / orders {n_o} 行）")


if __name__ == "__main__":
    build()
