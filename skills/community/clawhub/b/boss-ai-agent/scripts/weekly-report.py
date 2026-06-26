#!/usr/bin/env python3
"""Generate a formatted weekly report from MCP tool outputs.

Usage: Claude saves MCP responses to temp files, then runs:
  python weekly-report.py --mentor musk \
    --report report.json \
    --kpi kpi.json \
    --task-stats tasks.json \
    --signals signals.json

Outputs formatted weekly report markdown to stdout.
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


MAX_JSON_SIZE = 10 * 1024 * 1024  # 10MB

ALLOWED_MENTORS = frozenset({
    "musk", "inamori", "ma", "dalio", "grove", "ren", "son", "jobs", "bezos",
    "buffett", "zhangyiming", "leijun", "caodewang", "chushijian", "meyer", "trout",
})

MEDAL_SENTIMENT = {"gold": "positive", "silver": "neutral", "bronze": "needs attention"}


def load_json(path):
    if not path or not Path(path).exists():
        return None
    file_path = Path(path)
    if file_path.stat().st_size > MAX_JSON_SIZE:
        print(f"Error: {path} exceeds 10MB size limit", file=sys.stderr)
        return None
    try:
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error loading {path}: {e}", file=sys.stderr)
        return None


def format_employee_table(report_data):
    if not report_data:
        return "No report data available.\n"

    employees = report_data if isinstance(report_data, list) else report_data.get("employees", report_data.get("ranking", report_data.get("rankings", [])))
    if not employees:
        return "No employee data.\n"

    lines = ["| Rank | Name | Check-in Rate | Sentiment | Highlights |",
             "|------|------|--------------|-----------|------------|"]
    for i, emp in enumerate(employees, 1):
        name = emp.get("name", "Unknown")
        # Handle both direct rate fields and MCP ranking format {days, medal}
        rate = emp.get("checkin_rate", emp.get("submission_rate"))
        if rate is not None:
            rate_str = f"{rate:.0%}" if isinstance(rate, float) and rate <= 1 else str(rate)
        else:
            days = emp.get("days", 0)
            rate_str = f"{days} days" if days else "0 days"
        sentiment = emp.get("sentiment", emp.get("sentiment_trend"))
        if sentiment is None:
            medal = emp.get("medal", "")
            sentiment = MEDAL_SENTIMENT.get(medal, "N/A")
        highlights = emp.get("highlights", emp.get("summary", ""))
        if isinstance(highlights, list):
            highlights = "; ".join(highlights[:2])
        lines.append(f"| {i} | {name} | {rate_str} | {sentiment} | {highlights} |")
    return "\n".join(lines) + "\n"


def format_task_summary(task_data):
    if not task_data:
        return "No task data available.\n"
    
    stats = task_data if isinstance(task_data, dict) else {}
    total = sum(stats.get(k, 0) for k in ["todo", "in_progress", "in_review", "done", "blocked"])
    if total == 0:
        return "No tasks tracked.\n"
    
    done = stats.get("done", 0)
    blocked = stats.get("blocked", 0)
    completion = f"{done/total:.0%}" if total else "N/A"
    
    lines = [
        f"- **Total tasks**: {total}",
        f"- **Completed**: {done} ({completion})",
        f"- **In progress**: {stats.get('in_progress', 0)}",
        f"- **Blocked**: {blocked}" + (" ⚠️" if blocked > 0 else ""),
        f"- **In review**: {stats.get('in_review', 0)}",
        f"- **Todo**: {stats.get('todo', 0)}",
    ]
    return "\n".join(lines) + "\n"


def format_kpi_summary(kpi_data):
    if not kpi_data:
        return "No KPI data available.\n"
    
    metrics = kpi_data if isinstance(kpi_data, list) else kpi_data.get("metrics", [])
    if not metrics:
        return "No metrics configured.\n"
    
    green, yellow, red = [], [], []
    for m in metrics:
        name = m.get("name", "Unknown")
        current = m.get("current_value", m.get("value", 0))
        target = m.get("target_value", m.get("target", 0))
        if not target:
            green.append(f"- {name}: {current} (no target set)")
            continue
        ratio = current / target if target else 0
        entry = f"- **{name}**: {current} / {target} ({ratio:.0%})"
        if ratio >= 0.9:
            green.append(entry)
        elif ratio >= 0.7:
            yellow.append(entry + " ⚠️")
        else:
            red.append(entry + " 🔴")
    
    lines = []
    if red:
        lines.append("**Off Track:**\n" + "\n".join(red))
    if yellow:
        lines.append("**At Risk:**\n" + "\n".join(yellow))
    if green:
        lines.append("**On Track:**\n" + "\n".join(green))
    return "\n\n".join(lines) + "\n"


def mentor_commentary(mentor):
    comments = {
        "musk": "Focus on velocity — are we moving fast enough? What's the 10x opportunity this week?",
        "inamori": "Focus on people — who needs support? Who grew this week? Is the team harmonious?",
        "ma": "Focus on customers — how did we serve customers better? What change should we embrace?",
        "dalio": "Focus on principles — what mistakes did we learn from? Where can we be more transparent?",
        "grove": "Focus on OKRs — are we hitting our key results? What data supports our decisions?",
        "bezos": "Focus on Day 1 — are we still customer-obsessed? What long-term bets should we make?",
    }
    return comments.get(mentor, f"Apply {mentor}'s philosophy to interpret these results.")


def build_report(mentor, report, kpi, tasks, signals):
    now = datetime.now()
    lines = [
        f"# Weekly Report — Week of {now.strftime('%B %d, %Y')}",
        f"*Mentor: {mentor.title()} | Generated at {now.strftime('%Y-%m-%d %H:%M')}*\n",
        "## Team Performance",
        format_employee_table(report),
        "## Task Progress",
        format_task_summary(tasks),
        "## KPI Health",
        format_kpi_summary(kpi),
    ]

    # Execution signals summary
    if signals:
        sig_list = signals if isinstance(signals, list) else signals.get("signals", [])
        high_sigs = [s for s in sig_list if s.get("score", 0) > 0.5]
        if high_sigs:
            lines.append("## Risk Signals")
            for s in high_sigs[:5]:
                name = s.get("type", s.get("name", "Unknown"))
                score = s.get("score", 0)
                reason = s.get("reason", s.get("description", ""))
                lines.append(f"- **{name}** [{score:.0%}]: {reason}")
            lines.append("")

    lines.extend([
        "## Mentor Perspective",
        f"*{mentor_commentary(mentor)}*\n",
        "## Suggested 1:1 Topics",
        "*(Based on this week's data — read each employee's profile for details)*\n",
        "---",
        "*Generated by Boss AI Agent. Read `references/scenarios.md` for the full report flow.*",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate weekly report from MCP data")
    parser.add_argument("--mentor", default="musk", help="Active mentor ID")
    parser.add_argument("--report", help="Path to get_report JSON")
    parser.add_argument("--kpi", help="Path to KPI dashboard JSON")
    parser.add_argument("--task-stats", help="Path to task stats JSON")
    parser.add_argument("--signals", help="Path to execution signals JSON")
    args = parser.parse_args()
    if args.mentor not in ALLOWED_MENTORS:
        print(f"Warning: unknown mentor '{args.mentor}', falling back to 'musk'", file=sys.stderr)
        args.mentor = "musk"

    report = load_json(args.report)
    kpi = load_json(args.kpi)
    tasks = load_json(args.task_stats)
    signals = load_json(args.signals)

    print(build_report(args.mentor, report, kpi, tasks, signals))


if __name__ == "__main__":
    main()
