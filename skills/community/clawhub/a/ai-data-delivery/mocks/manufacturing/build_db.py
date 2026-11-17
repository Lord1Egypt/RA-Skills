#!/usr/bin/env python3
"""build_db.py — 制造·设备与生产场景：生成确定性 SQLite 物理库（domain.db）。

业务故事：一家离散制造工厂。生产记录表 production_run 是事实表（一行一次生产批次），
设备表 equipment 是维度表（一行一台设备）。典型问数：总产量、不良率、停机设备数、产线分布。
造数完全确定，gold 可用 SQL 复算。
"""
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "domain.db")

LINES = ["A线", "B线", "C线"]
PRODUCTS = ["零件甲", "零件乙", "零件丙"]
DTYPES = ["冲压机", "焊接机", "组装线"]
ESTATUS = ["运行", "停机", "检修"]


def build():
    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    conn.executescript("""
    CREATE TABLE production_run (
        run_id TEXT PRIMARY KEY,
        prod_date TEXT NOT NULL,
        line TEXT NOT NULL,
        product TEXT NOT NULL,
        qty INTEGER NOT NULL,
        defect_qty INTEGER NOT NULL
    );
    CREATE TABLE equipment (
        device_id TEXT PRIMARY KEY,
        device_type TEXT NOT NULL,
        status TEXT NOT NULL,
        line TEXT NOT NULL,
        last_maintenance_date TEXT NOT NULL
    );
    """)
    for i in range(1, 181):
        conn.execute("INSERT INTO production_run VALUES (?,?,?,?,?,?)",
                     (f"R{i:04d}", f"2026-{((i - 1) % 6) + 1:02d}-{((i - 1) % 28) + 1:02d}",
                      LINES[i % 3], PRODUCTS[(i // 3) % 3], 50 + (i * 11) % 150,
                      3 if i % 9 == 0 else (1 if i % 13 == 0 else 0)))
    for i in range(1, 16):
        conn.execute("INSERT INTO equipment VALUES (?,?,?,?,?)",
                     (f"E{i:03d}", DTYPES[i % 3], ESTATUS[(i // 2) % 3], LINES[i % 3],
                      f"2026-0{(i % 6) + 1}-20"))
    conn.commit()
    nr = conn.execute("SELECT COUNT(*) FROM production_run").fetchone()[0]
    ne = conn.execute("SELECT COUNT(*) FROM equipment").fetchone()[0]
    conn.close()
    print(f"建库完成：{DB}（production_run {nr} / equipment {ne}）")


if __name__ == "__main__":
    build()
