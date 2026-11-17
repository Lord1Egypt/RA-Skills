#!/usr/bin/env python3
"""build_db.py — 教育信息化·教学质量场景：生成确定性 SQLite 物理库（domain.db）。

业务故事：一所高校的教学数据平台，students 是学籍档案（一行一名学生），
course_scores 是修读成绩（一行一条修读记录，OBE 达成度分析的底座）。
典型问数：在读学生数、课程不及格率、平均成绩、学业预警学生数。
领域词汇来自 ai-delivery-spec 仓库 domain-education-it.md（Student/Course/
Academic Status/Graduation Requirement）。造数完全确定（无随机数），gold 期望可用 SQL 复算。
"""
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "domain.db")

COLLEGES = ["信息学院", "机电学院", "经管学院"]
GRADES = ["2023级", "2024级", "2025级"]
STATUS = ["在读", "在读", "在读", "休学", "毕业"]  # 3/5 在读
TERMS = ["2025-2026-1", "2025-2026-2"]


def build():
    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    conn.executescript("""
    CREATE TABLE students (
        student_id TEXT PRIMARY KEY,
        college TEXT NOT NULL,
        grade TEXT NOT NULL,
        status TEXT NOT NULL,
        warning TEXT NOT NULL,
        enroll_date TEXT NOT NULL
    );
    CREATE TABLE course_scores (
        score_id TEXT PRIMARY KEY,
        student_id TEXT NOT NULL REFERENCES students(student_id),
        course_id TEXT NOT NULL,
        term TEXT NOT NULL,
        score REAL NOT NULL,
        credit INTEGER NOT NULL
    );
    """)
    # 50 名学生：学院/年级轮转，状态 3/5 在读；预警标记 = 序号每 7 取 1
    for i in range(1, 51):
        conn.execute("INSERT INTO students VALUES (?,?,?,?,?,?)",
                     (f"S{i:03d}", COLLEGES[i % 3], GRADES[i % 3], STATUS[i % 5],
                      "是" if i % 7 == 0 else "否", f"20{23 + i % 3}-09-01"))
    # 200 条成绩：分数 = 40 + (i*17)%61（40–100），学期对半，课程 12 门轮转
    for i in range(1, 201):
        conn.execute("INSERT INTO course_scores VALUES (?,?,?,?,?,?)",
                     (f"SC{i:04d}", f"S{(i % 50) + 1:03d}", f"K{(i % 12) + 1:02d}",
                      TERMS[i % 2], 40 + (i * 17) % 61, 2 + i % 3))
    conn.commit()
    n = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
         for t in ("students", "course_scores")}
    conn.close()
    print(f"建库完成：{DB}（students {n['students']} / course_scores {n['course_scores']}）")


if __name__ == "__main__":
    build()
