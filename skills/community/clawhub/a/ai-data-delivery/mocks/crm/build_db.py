#!/usr/bin/env python3
"""build_db.py — CRM·销售与服务协同场景：生成确定性 SQLite 物理库（domain.db）。

业务故事：一家 B2B 企业，customers 是客户档案（一行一个客户），tickets 是服务工单
（一行一张工单，SLA 驱动的响应/关闭），leads 是市场线索（一行一条线索，首响时效是生命线）。
典型问数：工单量、超期工单数、工单关闭率、线索首响超时数。
领域词汇来自 ai-delivery-spec 仓库 domain-crm.md（Lead/Ticket/SLA/Customer 360）。
造数完全确定（无随机数），gold 期望可用 SQL 复算。
"""
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "domain.db")

LEVELS = ["普通", "银牌", "金牌"]
INDUSTRIES = ["制造", "零售", "软件", "物流"]
TYPES = ["咨询", "投诉", "故障"]
STATUS = ["新建", "处理中", "待客户", "已升级", "已关闭"]
SOURCES = ["官网", "转介绍", "展会"]
LEAD_STATUS = ["新线索", "已联系", "已转化", "无效"]


def build():
    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    conn.executescript("""
    CREATE TABLE customers (
        customer_id TEXT PRIMARY KEY,
        level TEXT NOT NULL,
        industry TEXT NOT NULL,
        register_date TEXT NOT NULL
    );
    CREATE TABLE tickets (
        ticket_id TEXT PRIMARY KEY,
        created_date TEXT NOT NULL,
        type TEXT NOT NULL,
        status TEXT NOT NULL,
        overdue TEXT NOT NULL,
        customer_id TEXT NOT NULL REFERENCES customers(customer_id)
    );
    CREATE TABLE leads (
        lead_id TEXT PRIMARY KEY,
        created_date TEXT NOT NULL,
        source TEXT NOT NULL,
        status TEXT NOT NULL,
        first_response_minutes INTEGER NOT NULL
    );
    """)
    # 30 个客户：等级/行业轮转，完全确定
    for i in range(1, 31):
        conn.execute("INSERT INTO customers VALUES (?,?,?,?)",
                     (f"C{i:03d}", LEVELS[i % 3], INDUSTRIES[i % 4],
                      f"2025-{(i % 12) + 1:02d}-10"))
    # 90 张工单：类型/状态错相位轮转；超期标记 = 序号每 5 取 1（18 张）
    for i in range(1, 91):
        conn.execute("INSERT INTO tickets VALUES (?,?,?,?,?,?)",
                     (f"T{i:04d}", f"2026-{(i % 6) + 1:02d}-{(i % 28) + 1:02d}",
                      TYPES[i % 3], STATUS[(i // 3) % 5],
                      "是" if i % 5 == 0 else "否", f"C{(i % 30) + 1:03d}"))
    # 60 条线索：首响分钟数 = 5 + (i*13)%120（SLA 30 分钟）
    for i in range(1, 61):
        conn.execute("INSERT INTO leads VALUES (?,?,?,?,?)",
                     (f"L{i:03d}", f"2026-{(i % 6) + 1:02d}-{(i % 28) + 1:02d}",
                      SOURCES[i % 3], LEAD_STATUS[i % 4], 5 + (i * 13) % 120))
    conn.commit()
    n = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
         for t in ("customers", "tickets", "leads")}
    conn.close()
    print(f"建库完成：{DB}（customers {n['customers']} / tickets {n['tickets']} / leads {n['leads']}）")


if __name__ == "__main__":
    build()
