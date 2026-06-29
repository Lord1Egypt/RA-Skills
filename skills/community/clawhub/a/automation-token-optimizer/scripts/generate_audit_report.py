#!/usr/bin/env python3
"""
月度定时任务综合审计报告生成器（v2.0）
负责：跑 SQL → 拿数据 → 按模板渲染 → 输出 Markdown
AI 只需：分析 Top 3 prompt + 合并评估 + 冗余清理 → 补充优化建议
"""

import sqlite3
import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = os.path.expanduser("~/.workbuddy/workbuddy.db")


def get_last_month_range():
    """获取上个月的第一天和最后一天的时间戳（毫秒）"""
    now = datetime.now()
    if now.month == 1:
        first_day = datetime(now.year - 1, 12, 1)
    else:
        first_day = datetime(now.year, now.month - 1, 1)
    if now.month == 1:
        this_month_first = datetime(now.year - 1, 12, 1)
    else:
        this_month_first = datetime(now.year, now.month, 1)

    start_ts = int(first_day.timestamp() * 1000)
    end_ts = int(this_month_first.timestamp() * 1000)
    month_label = first_day.strftime("%Y-%m")
    return start_ts, end_ts, month_label


def query_token_stats(conn, start_ts, end_ts):
    """查询各任务的 token 消耗排行"""
    sql = """
    SELECT 
      COALESCE(s.custom_title, s.title) as task_name,
      s.id,
      COUNT(*) as run_count,
      COALESCE(SUM(su.used), 0) as total_used,
      COALESCE(SUM(su.size), 0) as total_size,
      COALESCE(ROUND(AVG(su.used)), 0) as avg_per_run
    FROM sessions s
    LEFT JOIN session_usage su ON s.id = su.session_id
    WHERE s.is_background_automation = 1
      AND s.created_at >= ?
      AND s.created_at < ?
    GROUP BY task_name
    ORDER BY total_used DESC;
    """
    cursor = conn.execute(sql, (start_ts, end_ts))
    rows = []
    for row in cursor.fetchall():
        title = row[0] if row[0] else f"(未命名任务 {row[1][:8]}...)"
        rows.append({
            "title": title,
            "id": row[1],
            "run_count": row[2],
            "total_used": row[3],
            "total_size": row[4],
            "avg_per_run": row[5],
        })
    return rows


def query_grand_total(conn, start_ts, end_ts):
    """查询总消耗"""
    sql = """
    SELECT 
      COUNT(DISTINCT s.id) as total_runs,
      COALESCE(SUM(su.used), 0) as total_used,
      COALESCE(SUM(su.size), 0) as total_size
    FROM sessions s
    LEFT JOIN session_usage su ON s.id = su.session_id
    WHERE s.is_background_automation = 1
      AND s.created_at >= ?
      AND s.created_at < ?;
    """
    cursor = conn.execute(sql, (start_ts, end_ts))
    row = cursor.fetchone()
    return {
        "total_runs": row[0],
        "total_used": row[1],
        "total_size": row[2],
    }


def format_tokens(n):
    """格式化 token 数量为易读格式"""
    if n is None:
        return "0"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}万"
    elif n >= 10_000:
        return f"{n / 10_000:.1f}万"
    elif n >= 1_000:
        return f"{n / 1_000:.1f}K"
    else:
        return str(n)


def render_report(month_label, grand_total, task_stats):
    """按固定模板渲染 Markdown 报告（v2.0 含合并评估和冗余清理占位）"""
    lines = []
    lines.append(f"## 📊 定时任务综合审计报告（{month_label}）")
    lines.append("")
    lines.append("### 📈 Token 消耗概览")
    lines.append(f"- 自动化任务总运行次数：{grand_total['total_runs']} 次")
    lines.append(f"- 总 token 消耗：{format_tokens(grand_total['total_used'])}（上下文窗口总占用 {format_tokens(grand_total['total_size'])}）")
    top5 = task_stats[:5]
    lines.append(f"- 高消耗任务（前 {len(top5)}）")
    lines.append("")
    lines.append("### 🔴 高消耗任务排行")
    lines.append("| 排名 | 任务名 | 月运行次数 | 月消耗 token | 每次均值 | 优化方向 |")
    lines.append("|------|--------|-----------|-------------|---------|---------|")

    for i, task in enumerate(top5, 1):
        suggestion = "待 AI 分析"
        lines.append(
            f"| {i} | {task['title']} | {task['run_count']} | "
            f"{format_tokens(task['total_used'])} | "
            f"{format_tokens(task['avg_per_run'])} | {suggestion} |"
        )

    lines.append("")
    lines.append("### 🔀 可合并任务")
    lines.append("| 合并组 | 任务A | 任务B | 合并理由 | 建议操作 |")
    lines.append("|--------|-------|-------|---------|---------|")
    lines.append("<!-- AI 补充：按时间相近+领域相同规则评估 -->")
    lines.append("")

    lines.append("### 🗑️ 可删除任务")
    lines.append("| 任务名 | 状态 | 删除理由 |")
    lines.append("|--------|------|---------|")
    lines.append("<!-- AI 补充：长期 PAUSED + 被替代 + 重复任务 -->")
    lines.append("")

    lines.append("### ⏰ 降频建议")
    lines.append("| 任务名 | 当前频率 | 建议频率 | 理由 |")
    lines.append("|--------|---------|---------|------|")
    lines.append("<!-- AI 补充：高频低价值任务 -->")
    lines.append("")

    lines.append("### 💡 优化行动建议（可执行）")
    lines.append("<!-- AI 补充：针对 Top 3 任务的 prompt 分析和具体优化建议 -->")
    lines.append("")
    lines.append("### ✅ 综合结论")
    lines.append("<!-- AI 补充：总消耗是否合理、合并/删除/降频收益汇总 -->")
    lines.append("")
    return "\n".join(lines)


def main():
    if not os.path.exists(DB_PATH):
        print(f"❌ 数据库不存在：{DB_PATH}", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    try:
        start_ts, end_ts, month_label = get_last_month_range()
        task_stats = query_token_stats(conn, start_ts, end_ts)
        grand_total = query_grand_total(conn, start_ts, end_ts)

        if not task_stats:
            print(f"⚠️ {month_label} 无定时任务执行记录")
            return

        report = render_report(month_label, grand_total, task_stats)
        print(report)

        # 同时输出 Top 3 任务 ID 供 AI 后续分析
        print("\n---")
        print("### 待 AI 分析的 Top 3 任务 ID：")
        for i, task in enumerate(task_stats[:3], 1):
            print(f"{i}. `{task['id']}` — {task['title']}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
