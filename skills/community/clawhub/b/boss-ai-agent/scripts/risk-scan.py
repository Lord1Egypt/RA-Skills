#!/usr/bin/env python3
"""Generate a risk dashboard from MCP tool outputs.

Usage: Claude calls MCP tools, saves JSON responses to temp files, then runs:
  python risk-scan.py --mentor musk \
    --company-state state.json \
    --top-risks risks.json \
    --signals signals.json \
    --overdue overdue.json \
    --alerts alerts.json

Outputs formatted risk dashboard markdown to stdout.
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


def severity_icon(score):
    if score >= 0.8:
        return "🔴"
    elif score >= 0.5:
        return "🟡"
    return "🟢"


def categorize_risks(signals, overdue, alerts):
    """Split risks into people, delivery, and metric categories."""
    people, delivery, metric = [], [], []

    sig_list = signals if isinstance(signals, list) else (signals.get("signals", []) if signals else [])
    for s in sig_list:
        sig_type = s.get("type", s.get("name", "")).lower()
        entry = {
            "name": s.get("type", s.get("name", "Unknown")),
            "score": s.get("score", 0),
            "reason": s.get("reason", s.get("description", "")),
            "employees": s.get("employees", []),
        }
        if any(k in sig_type for k in ["overload", "engagement", "burnout"]):
            people.append(entry)
        elif any(k in sig_type for k in ["delivery", "blocker", "cascade"]):
            delivery.append(entry)
        else:
            metric.append(entry)

    # Overdue tasks are delivery risks
    overdue_list = overdue if isinstance(overdue, list) else (overdue.get("tasks", []) if overdue else [])
    for t in overdue_list:
        delivery.append({
            "name": f"Overdue: {t.get('title', 'Unknown task')}",
            "score": 0.6,
            "reason": f"Assigned to {t.get('assignee', 'unassigned')}, {t.get('days_overdue', '?')} days late",
            "employees": [t.get("assignee", "")] if t.get("assignee") else [],
        })

    # Alerts (consecutive misses) are people risks
    alert_list = alerts if isinstance(alerts, list) else (alerts.get("alerts", []) if alerts else [])
    for a in alert_list:
        people.append({
            "name": f"Missed check-ins: {a.get('name', a.get('employee_name', 'Unknown'))}",
            "score": min(a.get("consecutive_misses", a.get("missed_days", 0)) / 5, 1.0),
            "reason": f"{a.get('consecutive_misses', a.get('missed_days', '?'))} consecutive missed days",
            "employees": [a.get("name", a.get("employee_name", ""))],
        })

    # Sort each by score descending
    for lst in [people, delivery, metric]:
        lst.sort(key=lambda x: x["score"], reverse=True)

    return people, delivery, metric


def format_risk_section(title, risks, empty_msg):
    if not risks:
        return f"### {title}\n{empty_msg}\n"
    lines = [f"### {title}"]
    for r in risks:
        icon = severity_icon(r["score"])
        lines.append(f"- {icon} **{r['name']}** [{r['score']:.0%}]: {r['reason']}")
    return "\n".join(lines) + "\n"


def format_blocked_projects(state):
    if not state:
        return ""
    blocked = state.get("blocked_projects", [])
    if not blocked:
        return ""
    lines = ["### Blocked Projects"]
    for p in blocked:
        name = p.get("name", p.get("title", "Unknown"))
        reason = p.get("reason", p.get("blocker", "Unknown blocker"))
        lines.append(f"- **{name}**: {reason}")
    return "\n".join(lines) + "\n"


MENTOR_ACTIONS = {
    "musk": "Eliminate the highest-score blocker immediately. What's the 10x fix?",
    "inamori": "Check on affected team members first. Who needs support?",
    "ma": "Which risks affect customers? Address those first.",
    "dalio": "What principles apply? Be radically transparent about these risks with the team.",
    "grove": "Which risks threaten our OKRs? Prioritize by key result impact.",
    "bezos": "Which risks affect customer experience? Think long-term.",
}


def build_dashboard(mentor, state, risks, signals, overdue, alerts):
    now = datetime.now()
    people, delivery, metric = categorize_risks(signals, overdue, alerts)

    total_risks = len(people) + len(delivery) + len(metric)
    critical = sum(1 for r in people + delivery + metric if r["score"] >= 0.8)
    moderate = sum(1 for r in people + delivery + metric if 0.5 <= r["score"] < 0.8)

    lines = [
        f"# Risk Dashboard — {now.strftime('%B %d, %Y')}",
        f"*Mentor: {mentor.title()} | Generated at {now.strftime('%H:%M')}*\n",
        f"**Summary**: {total_risks} risks detected — {critical} critical, {moderate} moderate\n",
    ]

    # Top risks from MCP tool (pre-ranked)
    risk_list = risks if isinstance(risks, list) else (risks.get("signals", []) if risks else [])
    if risk_list:
        lines.append("## Top Risks (Pre-ranked by AI)")
        for r in risk_list[:5]:
            name = r.get("type", r.get("name", "Unknown"))
            score = r.get("score", 0)
            reason = r.get("reason", r.get("description", ""))
            lines.append(f"- {severity_icon(score)} **{name}** [{score:.0%}]: {reason}")
        lines.append("")

    lines.append("## Risk Breakdown\n")
    lines.append(format_risk_section("People Risks", people, "No people risks detected."))
    lines.append(format_risk_section("Delivery Risks", delivery, "No delivery risks detected."))
    lines.append(format_risk_section("Metric Risks", metric, "No metric risks detected."))

    blocked = format_blocked_projects(state)
    if blocked:
        lines.append(blocked)

    # Recommended actions
    lines.append("## Recommended Actions\n")
    action_items = []
    if people:
        top = people[0]
        emps = ", ".join(top["employees"][:3]) if top["employees"] else "affected team members"
        action_items.append(f"1. **Check on {emps}** — {top['reason']}")
    if delivery:
        top = delivery[0]
        action_items.append(f"2. **Unblock**: {top['name']} — {top['reason']}")
    if metric:
        top = metric[0]
        action_items.append(f"3. **Investigate metric**: {top['name']} — {top['reason']}")
    if not action_items:
        action_items.append("No immediate actions needed.")
    lines.extend(action_items)

    mentor_action = MENTOR_ACTIONS.get(mentor, f"Apply {mentor}'s philosophy to prioritize these risks.")
    lines.extend([
        "",
        "## Mentor Perspective",
        f"*{mentor_action}*\n",
        "---",
        "*Generated by Boss AI Agent. Read `references/scenarios.md` Scenario 8 for the full risk review flow.*",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate risk dashboard from MCP data")
    parser.add_argument("--mentor", default="musk", help="Active mentor ID")
    parser.add_argument("--company-state", help="Path to company state JSON")
    parser.add_argument("--top-risks", help="Path to top risks JSON")
    parser.add_argument("--signals", help="Path to execution signals JSON")
    parser.add_argument("--overdue", help="Path to overdue tasks JSON")
    parser.add_argument("--alerts", help="Path to alerts JSON")
    args = parser.parse_args()
    if args.mentor not in ALLOWED_MENTORS:
        print(f"Warning: unknown mentor '{args.mentor}', falling back to 'musk'", file=sys.stderr)
        args.mentor = "musk"

    state = load_json(args.company_state)
    risks = load_json(args.top_risks)
    signals = load_json(args.signals)
    overdue = load_json(args.overdue)
    alerts = load_json(args.alerts)

    print(build_dashboard(args.mentor, state, risks, signals, overdue, alerts))


if __name__ == "__main__":
    main()
