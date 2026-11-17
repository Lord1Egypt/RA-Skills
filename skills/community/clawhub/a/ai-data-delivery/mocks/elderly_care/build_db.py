#!/usr/bin/env python3
"""build_db.py — 养老机构等级评定场景：生成确定性 SQLite 物理库（domain.db）。

业务故事：一家连锁养老集团准备申报等级评定（GB/T 37276-2018 五级），
运营部把评级所需的定量证据沉淀为两张表：
  dws_facility_monthly —— 机构月度运营宽表（一行一机构一月，民政填报系统就是这个形态）
  residents            —— 入住老人明细表（一行一名入住老人，能力等级口径见 GB/T 42195-2022）
指标口径参照 GB/T 37276-2018（机构入住率 = 入住老年人总数 ÷ 总床位数）与配套标准。
造数完全确定（无随机数），gold 期望可用 SQL 复算。
"""
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "domain.db")

FACILITIES = ["康宁养老院", "颐年养老院", "安泰养老院"]
MONTHS = ["2026-06", "2026-07", "2026-08"]
STAT_DATES = ["2026-06-30", "2026-07-31", "2026-08-31"]
ABILITY = ["自理", "半失能", "失能"]
CARE_LEVELS = ["一级", "二级", "三级"]


def build():
    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    conn.executescript("""
    CREATE TABLE dws_facility_monthly (
        facility TEXT NOT NULL,
        month TEXT NOT NULL,
        bed_count INTEGER NOT NULL,
        resident_count INTEGER NOT NULL,
        caregiver_count INTEGER NOT NULL,
        certified_caregiver_count INTEGER NOT NULL,
        rehab_service_cnt INTEGER NOT NULL,
        complaint_cnt INTEGER NOT NULL,
        stat_date TEXT NOT NULL
        ,PRIMARY KEY (facility, month)
    );
    CREATE TABLE residents (
        resident_id TEXT PRIMARY KEY,
        facility TEXT NOT NULL,
        ability_level TEXT NOT NULL,
        care_level TEXT NOT NULL,
        admit_date TEXT NOT NULL
    );
    """)
    # 9 行宽表：机构 × 月；入住率逐月爬升（86%→94% 区间，对照等级门槛故事）
    for c, fac in enumerate(FACILITIES):
        beds = 200 + c * 50
        for m, month in enumerate(MONTHS):
            conn.execute(
                "INSERT INTO dws_facility_monthly VALUES (?,?,?,?,?,?,?,?,?)",
                (fac, month, beds,
                 beds * (86 + m * 2 + c * 2) // 100,  # resident_count 入住老人数
                 30 + c * 6 + m,                      # caregiver_count 护理员数
                 21 + c * 4 + m,                      # certified_caregiver_count 持证护理员数
                 90 + c * 20 + m * 5,                 # rehab_service_cnt 康复服务人次数
                 2 + (c + m) % 3,                     # complaint_cnt 投诉件数
                 STAT_DATES[m]))
    # 120 名入住老人：能力等级轮转（失能 1/4、半失能 1/4、自理 1/2）
    for i in range(1, 121):
        conn.execute(
            "INSERT INTO residents VALUES (?,?,?,?,?)",
            (f"R{i:04d}", FACILITIES[(i - 1) % 3],
             "失能" if i % 4 == 0 else ("半失能" if i % 4 == 2 else "自理"),
             CARE_LEVELS[i % 3],
             f"202{5 + (i % 2)}-{((i - 1) % 12) + 1:02d}-{(i % 28) + 1:02d}"))
    conn.commit()
    n_d = conn.execute("SELECT COUNT(*) FROM dws_facility_monthly").fetchone()[0]
    n_r = conn.execute("SELECT COUNT(*) FROM residents").fetchone()[0]
    conn.close()
    print(f"建库完成：{DB}（dws_facility_monthly {n_d} 行 / residents {n_r} 行）")


if __name__ == "__main__":
    build()
