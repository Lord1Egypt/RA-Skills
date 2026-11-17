#!/usr/bin/env python3
"""build_db.py — 高校本科教学审核评估场景：生成确定性 SQLite 物理库（domain.db）。

业务故事：一所应用型本科高校要迎接教育部本科教育教学审核评估，
信息中心把"全国高校教学基本状态数据库"的填报数据沉淀为两张表：
  dws_teaching_stats —— 教学基本状态宽表（一行一学院一学年，真实填报系统就是这个形态）
  graduates          —— 毕业生明细表（一行一名毕业生）
指标口径参照真实文件：教发[2004]2号《普通高等学校基本办学条件指标（试行）》、
《中国教育监测与评价统计指标体系（2020年版）》、教育部本科教育教学审核评估
指标体系（2021-2025年）第二类、本科教学质量报告支撑数据口径。
造数完全确定（无随机数），gold 期望可用 SQL 复算。
"""
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "domain.db")

COLLEGES = ["信息学院", "机电学院", "经管学院"]
YEARS = ["2023-2024", "2024-2025", "2025-2026"]
DESTINATIONS = ["协议就业", "升学", "灵活就业"]


def build():
    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    conn.executescript("""
    CREATE TABLE dws_teaching_stats (
        college TEXT NOT NULL,
        year TEXT NOT NULL,
        student_cnt INTEGER NOT NULL,
        teacher_cnt INTEGER NOT NULL,
        senior_title_cnt INTEGER NOT NULL,
        professor_cnt INTEGER NOT NULL,
        course_offered_cnt INTEGER NOT NULL,
        professor_taught_cnt INTEGER NOT NULL,
        teach_fund_amount REAL NOT NULL,
        stat_date TEXT NOT NULL,
        PRIMARY KEY (college, year)
    );
    CREATE TABLE graduates (
        student_id TEXT PRIMARY KEY,
        college TEXT NOT NULL,
        grad_year TEXT NOT NULL,
        degree_granted TEXT NOT NULL,
        destination TEXT NOT NULL,
        fitness_pass TEXT NOT NULL,
        grad_date TEXT NOT NULL
    );
    """)
    # 9 行宽表：学院 × 学年，各列按序号线性递推，完全确定
    for c, college in enumerate(COLLEGES):
        for y, year in enumerate(YEARS):
            student_cnt = 800 + c * 200 + y * 40
            teacher_cnt = 50 + c * 10 + y * 2
            row = (
                college, year, student_cnt, teacher_cnt,
                20 + c * 5 + y,          # senior_title_cnt 高级职称教师数
                8 + c * 2 + y,           # professor_cnt 教授数
                60 + c * 15 + y * 3,     # course_offered_cnt 开设课程门数
                30 + c * 9 + y * 2,      # professor_taught_cnt 教授主讲课程门数
                student_cnt * (1400 + c * 100 + y * 50),  # teach_fund_amount 教学日常运行支出(元)
                f"20{24 + y}-08-31",     # stat_date 统计截止日（学年结束）
            )
            conn.execute("INSERT INTO dws_teaching_stats VALUES (?,?,?,?,?,?,?,?,?,?)", row)
    # 150 名毕业生：前 75 行 2025 届，后 75 行 2026 届；各属性按序号轮转
    for i in range(1, 151):
        grad_year = "2025" if i <= 75 else "2026"
        conn.execute(
            "INSERT INTO graduates VALUES (?,?,?,?,?,?,?)",
            (f"G{i:04d}", COLLEGES[(i - 1) % 3], grad_year,
             "否" if i % 25 == 0 else "是",                       # degree_granted 学位授予
             "未落实" if i % 10 == 0 else DESTINATIONS[i % 3],      # destination 毕业去向
             "否" if i % 15 == 0 else "是",                       # fitness_pass 体质测试达标
             f"{grad_year}-06-30"))
    conn.commit()
    n_d = conn.execute("SELECT COUNT(*) FROM dws_teaching_stats").fetchone()[0]
    n_g = conn.execute("SELECT COUNT(*) FROM graduates").fetchone()[0]
    conn.close()
    print(f"建库完成：{DB}（dws_teaching_stats {n_d} 行 / graduates {n_g} 行）")


if __name__ == "__main__":
    build()
