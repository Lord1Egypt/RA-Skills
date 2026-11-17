#!/usr/bin/env python3
"""build_db.py — 绿色工厂评价场景：生成确定性 SQLite 物理库（domain.db）。

业务故事：一家装备制造企业申报国家级绿色工厂（GB/T 36132-2025），
能环部把"五化"评价所需的定量证据沉淀为两张表：
  dws_workshop_monthly —— 车间月度能耗与产出宽表（一行一车间一月，能源管理系统就是这个形态）
  waste_records        —— 固废处置明细表（一行一条处置记录）
指标口径参照 GB/T 36132-2025 的关键定量公式（单位产品综合能耗、可再生能源利用率、
工业用水重复利用率 R_w=V_r/(V+V_r)、一般工业固废综合利用率）。
造数完全确定（无随机数），gold 期望可用 SQL 复算。
"""
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "domain.db")

WORKSHOPS = ["冲压车间", "焊装车间", "涂装车间"]
MONTHS = ["2026-06", "2026-07", "2026-08"]
STAT_DATES = ["2026-06-30", "2026-07-31", "2026-08-31"]
WASTE_TYPES = ["边角料", "废包装", "污泥"]


def build():
    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    conn.executescript("""
    CREATE TABLE dws_workshop_monthly (
        workshop TEXT NOT NULL,
        month TEXT NOT NULL,
        energy_tce REAL NOT NULL,
        renewable_tce REAL NOT NULL,
        output_units INTEGER NOT NULL,
        water_intake_t REAL NOT NULL,
        water_reuse_t REAL NOT NULL,
        waste_gen_t REAL NOT NULL,
        waste_reused_t REAL NOT NULL,
        stat_date TEXT NOT NULL
        ,PRIMARY KEY (workshop, month)
    );
    CREATE TABLE waste_records (
        record_id TEXT PRIMARY KEY,
        workshop TEXT NOT NULL,
        waste_type TEXT NOT NULL,
        amount_t REAL NOT NULL,
        disposal TEXT NOT NULL,
        record_date TEXT NOT NULL
    );
    """)
    # 9 行宽表：车间 × 月；重复利用水量 = 9 × 取用新水量（重复利用率恒 90%，对照基准值达标）
    for c, ws in enumerate(WORKSHOPS):
        for m, month in enumerate(MONTHS):
            intake = 800 + c * 100 + m * 20
            conn.execute(
                "INSERT INTO dws_workshop_monthly VALUES (?,?,?,?,?,?,?,?,?,?)",
                (ws, month,
                 120 + c * 20 + m * 4,        # energy_tce 综合能耗（吨标煤）
                 12 + c * 6 + m * 3,          # renewable_tce 可再生能源
                 10000 + c * 2000 + m * 500,  # output_units 合格品产量（件）
                 intake,                      # water_intake_t 取用新水（吨）
                 intake * 9,                  # water_reuse_t 重复利用水（吨）
                 100 + c * 15 + m * 3,        # waste_gen_t 固废产生量（吨）
                 92 + c * 14 + m * 3,         # waste_reused_t 综合利用量（吨）
                 STAT_DATES[m]))
    # 90 条固废处置记录：i%13==0 为安全处置（6 条），其余综合利用
    for i in range(1, 91):
        conn.execute(
            "INSERT INTO waste_records VALUES (?,?,?,?,?,?)",
            (f"W{i:04d}", WORKSHOPS[(i - 1) % 3], WASTE_TYPES[i % 3],
             1 + (i % 9) * 0.5,
             "安全处置" if i % 13 == 0 else "综合利用",
             f"2026-0{6 + i % 3}-{(i % 28) + 1:02d}"))
    conn.commit()
    n_d = conn.execute("SELECT COUNT(*) FROM dws_workshop_monthly").fetchone()[0]
    n_w = conn.execute("SELECT COUNT(*) FROM waste_records").fetchone()[0]
    conn.close()
    print(f"建库完成：{DB}（dws_workshop_monthly {n_d} 行 / waste_records {n_w} 行）")


if __name__ == "__main__":
    build()
