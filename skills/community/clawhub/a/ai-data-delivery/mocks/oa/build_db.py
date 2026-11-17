#!/usr/bin/env python3
"""build_db.py — OA·协同办公流程场景：生成确定性 SQLite 物理库（domain.db）。

业务故事：一家集团企业的 OA 平台，todos 是统一待办（一行一条待办，跨审批/公文/任务），
workflow_instances 是流程实例（一行一次审批流转，节点超时是流程健康度的核心信号）。
典型问数：待办按期办结率、流程平均时长、节点超时数、已办结流程数。
领域词汇来自 ai-delivery-spec 仓库 domain-oa.md（Unified Todo/Workflow Instance/
Workflow Node/Supervision Task）。造数完全确定（无随机数），gold 期望可用 SQL 复算。
"""
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "domain.db")

SOURCES = ["审批", "公文", "任务", "提醒"]
TODO_STATUS = ["待处理", "处理中", "已办结", "已取消"]
DEPTS = ["综合部", "财务部", "人事部"]
DEFS = ["请假审批", "报销审批", "采购审批"]
WF_STATUS = ["运行中", "已完成", "已驳回"]


def build():
    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    conn.executescript("""
    CREATE TABLE todos (
        todo_id TEXT PRIMARY KEY,
        created_date TEXT NOT NULL,
        source TEXT NOT NULL,
        status TEXT NOT NULL,
        ontime TEXT NOT NULL,
        owner_dept TEXT NOT NULL
    );
    CREATE TABLE workflow_instances (
        instance_id TEXT PRIMARY KEY,
        submit_date TEXT NOT NULL,
        def_name TEXT NOT NULL,
        status TEXT NOT NULL,
        duration_hours REAL NOT NULL,
        timeout_nodes INTEGER NOT NULL
    );
    """)
    # 80 条待办：来源/部门轮转，状态错相位；按期标记 = i%5<3（48 条）
    for i in range(1, 81):
        conn.execute("INSERT INTO todos VALUES (?,?,?,?,?,?)",
                     (f"D{i:03d}", f"2026-{(i % 6) + 1:02d}-{(i % 28) + 1:02d}",
                      SOURCES[i % 4], TODO_STATUS[(i // 4) % 4],
                      "是" if i % 5 < 3 else "否", DEPTS[i % 3]))
    # 60 个流程实例：时长 = 2 + (i*7)%70 小时；超时节点 = i%3（0/1/2）
    for i in range(1, 61):
        conn.execute("INSERT INTO workflow_instances VALUES (?,?,?,?,?,?)",
                     (f"W{i:03d}", f"2026-{(i % 6) + 1:02d}-{(i % 28) + 1:02d}",
                      DEFS[i % 3], WF_STATUS[i % 3], 2 + (i * 7) % 70, i % 3))
    conn.commit()
    n = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
         for t in ("todos", "workflow_instances")}
    conn.close()
    print(f"建库完成：{DB}（todos {n['todos']} / workflow_instances {n['workflow_instances']}）")


if __name__ == "__main__":
    build()
