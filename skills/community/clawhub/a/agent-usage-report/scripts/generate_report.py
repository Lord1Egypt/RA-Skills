#!/usr/bin/env python3
"""
OpenClaw Agent 周报生成器
读取 session 日志和 memory 文件，输出结构化周报
"""

import json
import os
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path

AGENT_ID = "xiaotianmao"  # 可通过 Runtime 动态获取
SESSIONS_DIR = Path.home() / ".openclaw" / "agents" / AGENT_ID / "sessions"
WORKSPACE = Path.home() / ".openclaw" / "workspaces" / "bot6"


def get_week_range(date_str=None):
    """返回上周的起止日期（周一到周日）"""
    if date_str:
        today = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        today = datetime.now()
    monday = today - timedelta(days=today.weekday() + 7)
    sunday = monday + timedelta(days=6)
    return monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d")


def list_sessions_in_week(start, end):
    """列出指定日期范围内的 session 文件"""
    sessions_dir = SESSIONS_DIR
    if not sessions_dir.exists():
        return []
    sessions = []
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt = datetime.strptime(end, "%Y-%m-%d")
    for f in sessions_dir.glob("*.jsonl"):
        try:
            with open(f) as fh:
                first = fh.readline()
                if not first:
                    continue
                meta = json.loads(first)
                ts = meta.get("timestamp", "")
                if not ts:
                    continue
                session_date = datetime.strptime(ts[:10], "%Y-%m-%d")
                if start_dt <= session_date <= end_dt:
                    sessions.append(f)
        except Exception:
            continue
    return sessions


def count_messages(session_file):
    """统计 session 中的消息数、用户/助手消息、工具调用"""
    user_count = 0
    assistant_count = 0
    tool_calls = []
    total_cost = 0.0
    try:
        with open(session_file) as f:
            for line in f:
                if not line.strip():
                    continue
                msg = json.loads(line)
                if msg.get("type") != "message":
                    continue
                role = msg.get("message", {}).get("role", "")
                content = msg.get("message", {}).get("content", [])
                usage = msg.get("message", {}).get("usage", {})
                cost = usage.get("cost", {}).get("total", 0) or 0
                total_cost += cost
                if role == "user":
                    user_count += 1
                elif role == "assistant":
                    assistant_count += 1
                    # 统计工具调用
                    for c in content:
                        if isinstance(c, dict) and c.get("type") == "toolCall":
                            tool_calls.append(c.get("name", "unknown"))
    except Exception as e:
        print(f"  ⚠️  读取 session 出错: {e}", file=sys.stderr)
    return user_count, assistant_count, tool_calls, total_cost


def get_memory_entries(start, end):
    """从 memory 目录读取指定日期范围的笔记"""
    memory_dir = WORKSPACE / "memory"
    if not memory_dir.exists():
        return []
    entries = []
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt = datetime.strptime(end, "%Y-%m-%d")
    for f in memory_dir.glob("*.md"):
        try:
            date_str = f.stem  # YYYY-MM-DD 或 YYYY-MM-DD-HHmm
            # 匹配日期部分
            m = re.match(r"(\d{4}-\d{2}-\d{2})", date_str)
            if not m:
                continue
            d = datetime.strptime(m.group(1), "%Y-%m-%d")
            if start_dt <= d <= end_dt:
                entries.append(f.read_text())
        except Exception:
            continue
    return entries


def get_daily_summary(start, end):
    """从 memory 中提取每日汇总信息"""
    entries = get_memory_entries(start, end)
    if not entries:
        return None
    # 合并所有 entries
    combined = "\n".join(entries)
    return combined


def build_report():
    """生成完整周报"""
    import argparse
    parser = argparse.ArgumentParser(description="生成 OpenClaw Agent 周报")
    parser.add_argument("--start", help="开始日期 YYYY-MM-DD（默认上周一）")
    parser.add_argument("--end", help="结束日期 YYYY-MM-DD（默认上周日）")
    parser.add_argument("--workspace", default=str(WORKSPACE), help="工作区路径")
    parser.add_argument("--output", help="输出文件路径（默认打印到 stdout）")
    args = parser.parse_args()

    if args.start and args.end:
        start, end = args.start, args.end
    else:
        start, end = get_week_range()

    print(f"📅 统计周期：{start} ~ {end}", file=sys.stderr)

    sessions = list_sessions_in_week(start, end)
    print(f"📂 找到 {len(sessions)} 个 session 文件", file=sys.stderr)

    total_user = 0
    total_assistant = 0
    all_tool_calls = []
    total_cost = 0.0
    for sf in sessions:
        u, a, tc, c = count_messages(sf)
        total_user += u
        total_assistant += a
        all_tool_calls.extend(tc)
        total_cost += c

    # 工具调用统计
    from collections import Counter
    tool_counter = Counter(all_tool_calls)
    top_tools = tool_counter.most_common(10)

    # memory 内容摘要
    memory_content = get_daily_summary(start, end)

    # 生成报告
    lines = []
    lines.append("=" * 60)
    lines.append("OpenClaw Agent 使用周报")
    lines.append(f"统计周期：{start} ~ {end}")
    lines.append("=" * 60)
    lines.append("")
    lines.append("一、运行数据概览")
    lines.append(f"  • 活跃 session 数：{len(sessions)} 个")
    lines.append(f"  • 用户消息总数：{total_user} 条")
    lines.append(f"  • 助手响应总数：{total_assistant} 次")
    lines.append(f"  • 工具调用总数：{sum(tool_counter.values())} 次")
    if total_cost > 0:
        lines.append(f"  • 总成本：约 ${total_cost:.4f}")
    lines.append("")
    lines.append("二、高频工具调用 TOP10")
    for tool, count in top_tools:
        lines.append(f"  {count:>4} 次  {tool}")
    lines.append("")
    lines.append("三、Memory 日志摘要")
    if memory_content:
        # 截取前 2000 字
        snippet = memory_content[:2000]
        lines.append("---")
        lines.append(snippet)
        lines.append("---")
    else:
        lines.append("  （本周无 memory 记录）")
    lines.append("")
    lines.append("四、异常记录")
    lines.append("  （从 session 日志中提取错误信息，待补充）")
    lines.append("")
    lines.append("=" * 60)
    lines.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 60)

    report = "\n".join(lines)

    if args.output:
        Path(args.output).write_text(report)
        print(f"✅ 报告已保存：{args.output}", file=sys.stderr)
    else:
        print(report)

    return report


if __name__ == "__main__":
    build_report()
