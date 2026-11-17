#!/usr/bin/env python3
"""build_db.py — 金融·信贷风控场景：生成确定性 SQLite 物理库（domain.db）。

业务故事：一家区域性银行的信贷业务。借款人表 borrowers 含敏感证件号（演示敏感标记），
贷款表 loans 是事实表。故意埋一个双口径：status='逾期' 与 overdue_days>0 不一致
（部分贷款有历史逾期天数但当前状态正常）——用于演示 declared_conflict 声明式冲突。
造数完全确定，gold 可用 SQL 复算。
"""
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "domain.db")

RISK = ["低", "中", "高"]
PRODUCT = ["经营贷", "消费贷", "房贷"]
STATUS = ["正常", "逾期", "结清"]


def build():
    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    conn.executescript("""
    CREATE TABLE borrowers (
        borrower_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        risk_level TEXT NOT NULL,
        id_card TEXT NOT NULL,
        reg_date TEXT NOT NULL
    );
    CREATE TABLE loans (
        loan_id TEXT PRIMARY KEY,
        apply_date TEXT NOT NULL,
        product_type TEXT NOT NULL,
        status TEXT NOT NULL,
        amount REAL NOT NULL,
        overdue_days INTEGER NOT NULL,
        borrower_id TEXT NOT NULL REFERENCES borrowers(borrower_id)
    );
    """)
    for i in range(1, 31):
        conn.execute("INSERT INTO borrowers VALUES (?,?,?,?,?)",
                     (f"B{i:03d}", f"借款人{i:03d}", RISK[i % 3],
                      f"1101011990{i % 12 + 1:02d}{(i % 28) + 1:02d}{i:04d}",
                      f"2025-{(i % 12) + 1:02d}-10"))
    for i in range(1, 91):
        conn.execute("INSERT INTO loans VALUES (?,?,?,?,?,?,?)",
                     (f"L{i:04d}", f"2026-{((i - 1) % 6) + 1:02d}-{((i - 1) % 28) + 1:02d}",
                      PRODUCT[i % 3], STATUS[(i // 5) % 3], 5000 + (i * 997) % 45000,
                      6 if i % 7 == 0 else 0, f"B{(i % 30) + 1:03d}"))
    conn.commit()
    nb = conn.execute("SELECT COUNT(*) FROM borrowers").fetchone()[0]
    nl = conn.execute("SELECT COUNT(*) FROM loans").fetchone()[0]
    s1 = conn.execute("SELECT COUNT(*) FROM loans WHERE status='逾期'").fetchone()[0]
    s2 = conn.execute("SELECT COUNT(*) FROM loans WHERE overdue_days > 0").fetchone()[0]
    conn.close()
    print(f"建库完成：{DB}（borrowers {nb} / loans {nl}；状态口径逾期 {s1} vs 天数口径 {s2}——双口径已埋）")


if __name__ == "__main__":
    build()
