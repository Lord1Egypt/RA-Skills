#!/usr/bin/env python3
"""日志分析工具 - 免费版

用法:
    python3 log_analyzer.py
    python3 log_analyzer.py --log-file /path/to/logfile
    python3 log_analyzer.py --level error
    python3 log_analyzer.py --json
    python3 log_analyzer.py --since "2024-01-01" --until "2024-01-31"
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime


# 常见OpenClaw日志路径
DEFAULT_LOG_PATHS = [
    os.path.expanduser("~/.openclaw/logs/openclaw.log"),
    os.path.expanduser("~/.openclaw/logs/gateway.log"),
    "/var/log/openclaw.log",
]

# 日志级别正则（匹配多种格式）
LOG_PATTERN = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2}:\d{2}[^\s]*)?"
    r"\s*(?P<level>\[?(?:ERROR|WARN|WARNING|INFO|DEBUG|FATAL|CRITICAL|VERBOSE)\]?)"
    r"\s*(?P<message>.*)",
    re.IGNORECASE
)

LEVEL_MAP = {
    "error": ["ERROR", "FATAL", "CRITICAL"],
    "warn": ["WARN", "WARNING"],
    "info": ["INFO", "VERBOSE"],
    "debug": ["DEBUG"],
}


def parse_log_line(line):
    """解析单行日志"""
    line = line.strip()
    if not line:
        return None

    match = LOG_PATTERN.match(line)
    if match:
        level = match.group("level").strip("[]").upper()
        # 标准化级别
        if level == "WARNING":
            level = "WARN"
        return {
            "timestamp": match.group("timestamp") or "",
            "level": level,
            "message": match.group("message").strip(),
        }
    else:
        # 尝试简单匹配
        upper = line[:20].upper()
        if "ERROR" in upper or "ERR" in upper:
            level = "ERROR"
        elif "WARN" in upper:
            level = "WARN"
        elif "DEBUG" in upper:
            level = "DEBUG"
        else:
            level = "INFO"
        return {
            "timestamp": "",
            "level": level,
            "message": line,
        }


def find_log_file(log_file=None):
    """查找日志文件"""
    if log_file and os.path.exists(log_file):
        return log_file

    for path in DEFAULT_LOG_PATHS:
        if os.path.exists(path):
            return path

    return None


def analyze_log(log_path, level_filter=None, since=None, until=None):
    """分析日志文件"""
    if not log_path or not os.path.exists(log_path):
        return {
            "error": f"日志文件不存在: {log_path}",
            "hint": "请指定 --log-file 参数",
        }

    entries = []
    line_count = 0
    error_messages = []

    with open(log_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line_count += 1
            parsed = parse_log_line(line)
            if not parsed:
                continue

            # 级别过滤
            if level_filter:
                allowed = LEVEL_MAP.get(level_filter, [level_filter.upper()])
                if parsed["level"] not in allowed:
                    continue

            entries.append(parsed)
            if parsed["level"] in ("ERROR", "FATAL", "CRITICAL"):
                error_messages.append(parsed["message"][:120])

    # 统计
    level_counts = Counter(e["level"] for e in entries)

    # 错误模式分析
    error_patterns = Counter()
    for msg in error_messages:
        # 提取关键词
        for pattern in [
            r"Error:?\s*(.+)",
            r"failed\s+to\s+(.+)",
            r"cannot\s+(.+)",
            r"unavailable",
            r"timeout",
            r"connection\s+(?:refused|reset)",
        ]:
            m = re.search(pattern, msg, re.IGNORECASE)
            if m:
                error_patterns[m.group(0)[:80]] += 1
                break

    result = {
        "log_file": log_path,
        "total_lines": line_count,
        "parsed_entries": len(entries),
        "level_counts": dict(level_counts),
        "error_count": sum(
            level_counts.get(l, 0)
            for l in ("ERROR", "FATAL", "CRITICAL")
        ),
        "warn_count": level_counts.get("WARN", 0),
        "top_errors": error_patterns.most_common(10),
        "recent_errors": error_messages[-5:] if error_messages else [],
    }

    return result


def format_text(result):
    """格式化文本输出"""
    if "error" in result:
        return f"❌ {result['error']}\n💡 {result.get('hint', '')}"

    lines = []
    lines.append("\n📋 日志分析报告")
    lines.append("=" * 45)
    lines.append(f"  日志文件: {result['log_file']}")
    lines.append(f"  总行数: {result['total_lines']}")
    lines.append(f"  解析条目: {result['parsed_entries']}")
    lines.append("")
    lines.append("  📊 级别统计:")
    for level, count in sorted(
        result["level_counts"].items(), key=lambda x: -x[1]
    ):
        emoji = {"ERROR": "🔴", "WARN": "🟡", "INFO": "🔵", "DEBUG": "⚪", "FATAL": "💀", "CRITICAL": "💀"}.get(level, "⚪")
        lines.append(f"    {emoji} {level}: {count}")

    if result["top_errors"]:
        lines.append("")
        lines.append("  🔍 常见错误模式:")
        for pattern, count in result["top_errors"]:
            lines.append(f"    • {pattern} (x{count})")

    if result["recent_errors"]:
        lines.append("")
        lines.append("  ⏱ 最近错误:")
        for msg in result["recent_errors"]:
            lines.append(f"    → {msg}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="OpenClaw日志分析工具")
    parser.add_argument("--log-file", default=None, help="日志文件路径")
    parser.add_argument(
        "--level", choices=["error", "warn", "info", "debug", "all"],
        default="all", help="日志级别过滤"
    )
    parser.add_argument("--since", default=None, help="起始时间 (YYYY-MM-DD)")
    parser.add_argument("--until", default=None, help="结束时间 (YYYY-MM-DD)")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()

    level_filter = None if args.level == "all" else args.level

    log_path = find_log_file(args.log_file)
    result = analyze_log(
        log_path,
        level_filter=level_filter,
        since=args.since,
        until=args.until,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_text(result))
        if "error" not in result:
            print(f"\n💡 免费版功能: 日志分析 | 付费版: 自动化告警、故障诊断")


if __name__ == "__main__":
    main()
