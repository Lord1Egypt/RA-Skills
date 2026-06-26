#!/usr/bin/env python3
"""Format a morning briefing from MCP tool outputs.

Usage: Claude calls MCP tools, saves JSON responses to temp files, then runs:
  python format-briefing.py --mentor musk \
    --company-state state.json \
    --top-risks risks.json \
    --alerts alerts.json \
    --kpi kpi.json \
    --working-memory memory.json \
    --recommendations recs.json

Outputs formatted markdown briefing to stdout.
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

MENTOR_PRIORITIES = {
    "musk":    ["blockers", "delivery_risks", "metrics", "people"],
    "inamori": ["people", "team_harmony", "blockers", "metrics"],
    "ma":      ["customer_impact", "adaptability", "team", "metrics"],
    "dalio":   ["transparency_gaps", "principle_violations", "metrics", "people"],
    "grove":   ["okr_progress", "metrics", "blockers", "people"],
    "bezos":   ["customer_impact", "day1_indicators", "metrics", "delivery_risks"],
}


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


def format_section(title, items, empty_msg="No items."):
    if not items:
        return f"### {title}\n{empty_msg}\n"
    lines = [f"### {title}"]
    for item in items:
        if isinstance(item, dict):
            name = item.get("title", item.get("name", item.get("employee_name", item.get("metric_name", str(item)))))
            detail = item.get("description", item.get("reason", item.get("value", "")))
            if not detail and item.get("missed_days"):
                detail = f"{item['missed_days']} consecutive missed days"
            score = item.get("score", item.get("severity", ""))
            score_str = f" [{score:.0%}]" if isinstance(score, (int, float)) and score <= 1 else ""
            lines.append(f"- **{name}**{score_str}: {detail}")
        else:
            lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def extract_off_track_kpis(kpi_data):
    if not kpi_data:
        return []
    metrics = kpi_data if isinstance(kpi_data, list) else kpi_data.get("metrics", [])
    off_track = []
    for m in metrics:
        current = m.get("current_value", m.get("value", 0))
        target = m.get("target_value", m.get("target", 0))
        if target and current < target * 0.9:
            off_track.append({
                "metric_name": m.get("name", "Unknown"),
                "value": f"{current} / {target} ({current/target:.0%})" if target else str(current),
            })
    return off_track


def extract_action_items(memory_data):
    if not memory_data:
        return []
    items = memory_data.get("action_items", [])
    if not items:
        pending = memory_data.get("pending_decisions", [])
        return [{"name": d} for d in pending] if pending else []
    return [{"name": item} if isinstance(item, str) else item for item in items]


def build_briefing(mentor, state, risks, alerts, kpi, memory, recs):
    now = datetime.now()
    lines = [
        f"# Morning Briefing — {now.strftime('%A, %B %d, %Y')}",
        f"*Mentor: {mentor.title()} | Generated at {now.strftime('%H:%M')}*\n",
    ]

    # Momentum indicator from working memory
    if memory:
        momentum = memory.get("team_momentum", "neutral")
        lines.append(f"**Team Momentum**: {momentum}\n")

    priority_order = MENTOR_PRIORITIES.get(mentor, MENTOR_PRIORITIES["musk"])

    sections = {
        "blockers": ("Blockers & Urgent Issues",
                     (risks or []) if isinstance(risks, list) else (risks.get("signals", []) if risks else []),
                     "No critical risks detected."),
        "delivery_risks": ("Delivery Risks",
                           (state.get("overdue_tasks", []) if state else []),
                           "No overdue tasks."),
        "metrics": ("Off-Track Metrics",
                    extract_off_track_kpis(kpi),
                    "All metrics on track."),
        "people": ("People Alerts",
                   (alerts if isinstance(alerts, list) else (alerts.get("alerts", []) if alerts else [])),
                   "No people alerts."),
        "customer_impact": ("Customer Impact",
                            [], "No customer-facing issues detected."),
        "team_harmony": ("Team Harmony",
                         [], "No team concerns detected."),
        "adaptability": ("Adaptability & Change",
                         [], "No adaptation issues."),
        "transparency_gaps": ("Transparency Gaps",
                              [], "No transparency issues."),
        "principle_violations": ("Principle Violations",
                                 [], "No violations detected."),
        "okr_progress": ("OKR Progress",
                         [], "Check `get_goal_state` for details."),
        "day1_indicators": ("Day 1 Indicators",
                            [], "Check customer metrics for details."),
        "team": ("Team Updates",
                 [], "No notable team updates."),
    }

    for key in priority_order:
        if key in sections:
            title, items, empty = sections[key]
            lines.append(format_section(title, items, empty))

    # AI Recommendations
    if recs:
        rec_list = recs if isinstance(recs, list) else recs.get("recommendations", [])
        if rec_list:
            lines.append(format_section("AI Recommendations", rec_list[:3], "None pending."))

    # Action items from working memory
    action_items = extract_action_items(memory)
    if action_items:
        lines.append(format_section("Pending Action Items", action_items))

    lines.append("---\n*Read `references/scenarios.md` Scenario 3 for the full briefing flow.*")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Format morning briefing from MCP data")
    parser.add_argument("--mentor", default="musk", help="Active mentor ID")
    parser.add_argument("--company-state", help="Path to company state JSON")
    parser.add_argument("--top-risks", help="Path to top risks JSON")
    parser.add_argument("--alerts", help="Path to alerts JSON")
    parser.add_argument("--kpi", help="Path to KPI dashboard JSON")
    parser.add_argument("--working-memory", help="Path to working memory JSON")
    parser.add_argument("--recommendations", help="Path to recommendations JSON")
    args = parser.parse_args()
    if args.mentor not in ALLOWED_MENTORS:
        print(f"Warning: unknown mentor '{args.mentor}', falling back to 'musk'", file=sys.stderr)
        args.mentor = "musk"

    state = load_json(args.company_state)
    risks = load_json(args.top_risks)
    alerts = load_json(args.alerts)
    kpi = load_json(args.kpi)
    memory = load_json(args.working_memory)
    recs = load_json(args.recommendations)

    print(build_briefing(args.mentor, state, risks, alerts, kpi, memory, recs))


if __name__ == "__main__":
    main()
