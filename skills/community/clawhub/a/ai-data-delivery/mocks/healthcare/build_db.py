#!/usr/bin/env python3
"""build_db.py — 医疗·门诊运营场景：生成确定性 SQLite 物理库（domain.db）。

业务故事：一家综合医院的门诊运营。医生表 doctors（一行一个医生），
就诊表 visits 是事实表（一行一次门诊）。典型问数：门诊人次、复诊率、专家医师数、科室分布。
造数完全确定，gold 可用 SQL 复算。
"""
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "domain.db")

TITLES = ["住院医师", "主治医师", "副主任医师", "主任医师"]
DEPTS = ["内科", "外科", "儿科", "妇科"]
VTYPES = ["初诊", "复诊"]


def build():
    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    conn.executescript("""
    CREATE TABLE doctors (
        doctor_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        title TEXT NOT NULL,
        dept TEXT NOT NULL,
        hire_date TEXT NOT NULL
    );
    CREATE TABLE visits (
        visit_id TEXT PRIMARY KEY,
        visit_date TEXT NOT NULL,
        dept TEXT NOT NULL,
        visit_type TEXT NOT NULL,
        fee REAL NOT NULL,
        doctor_id TEXT NOT NULL REFERENCES doctors(doctor_id)
    );
    """)
    for i in range(1, 25):
        conn.execute("INSERT INTO doctors VALUES (?,?,?,?,?)",
                     (f"D{i:03d}", f"医生{i:03d}", TITLES[i % 4], DEPTS[i % 4],
                      f"20{10 + i % 15}-06-01"))
    for i in range(1, 201):
        conn.execute("INSERT INTO visits VALUES (?,?,?,?,?,?)",
                     (f"V{i:04d}", f"2026-{((i - 1) % 6) + 1:02d}-{((i - 1) % 28) + 1:02d}",
                      DEPTS[(i // 3) % 4], VTYPES[(i // 3) % 2], 20 + (i * 13) % 280,
                      f"D{(i % 24) + 1:03d}"))
    conn.commit()
    nd = conn.execute("SELECT COUNT(*) FROM doctors").fetchone()[0]
    nv = conn.execute("SELECT COUNT(*) FROM visits").fetchone()[0]
    conn.close()
    print(f"建库完成：{DB}（doctors {nd} / visits {nv}）")


if __name__ == "__main__":
    build()
