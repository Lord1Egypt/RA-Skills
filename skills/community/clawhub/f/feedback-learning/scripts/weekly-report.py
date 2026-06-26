#!/usr/bin/env python3
"""
weekly-report.py — Generate weekly learning synthesis report.
Run via cron every Sunday at 4:00 AM.
"""
import json
import os
from datetime import datetime, timedelta, timezone
from collections import defaultdict

LEARNING_DIR = os.path.expanduser("~/.openclaw/shared/learning")
EVENTS_FILE = os.path.join(LEARNING_DIR, "events.jsonl")
PATTERNS_FILE = os.path.join(LEARNING_DIR, "patterns.json")
GENES_FILE = os.path.join(LEARNING_DIR, "genes.json")
REPORTS_DIR = os.path.join(LEARNING_DIR, "reports")


def load_week_events():
    events = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    if not os.path.exists(EVENTS_FILE) or os.path.getsize(EVENTS_FILE) == 0:
        return events
    with open(EVENTS_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
                ts = datetime.fromisoformat(ev["ts"].replace("Z", "+00:00"))
                if ts >= cutoff:
                    events.append(ev)
            except (json.JSONDecodeError, KeyError):
                continue
    return events


def load_json(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None


def generate_report():
    now = datetime.now(timezone.utc)
    week_num = now.isocalendar()[1]
    year = now.year
    
    events = load_week_events()
    patterns = load_json(PATTERNS_FILE) or {"patterns": []}
    genes = load_json(GENES_FILE) or {"rules": []}
    
    # Stats
    by_type = defaultdict(int)
    by_agent = defaultdict(int)
    by_source = defaultdict(int)
    for ev in events:
        by_type[ev.get("type", "?")] += 1
        by_agent[ev.get("agent", "?")] += 1
        by_source[ev.get("source", "?")] += 1
    
    # New rules this week
    new_rules = []
    week_ago = (now - timedelta(days=7)).isoformat()
    for r in genes.get("rules", []):
        if r.get("promoted_at", "") >= week_ago:
            new_rules.append(r)
    
    # Top patterns
    top_patterns = sorted(patterns.get("patterns", []), key=lambda x: -x.get("count", 0))[:5]
    
    # Generate markdown
    report = f"""# Weekly Learning Report — W{week_num:02d} {year}
Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}

## 📊 Summary
- **Total events this week:** {len(events)}
- **Errors/Corrections:** {by_type.get('error', 0) + by_type.get('correction', 0)}
- **Positive feedback:** {by_type.get('positive', 0)}
- **Requeries:** {by_type.get('requery', 0)}

## 🤖 By Agent
"""
    for agent, count in sorted(by_agent.items(), key=lambda x: -x[1]):
        report += f"- **{agent}:** {count} events\n"
    
    report += "\n## 📡 By Source\n"
    for src, count in sorted(by_source.items(), key=lambda x: -x[1]):
        report += f"- **{src}:** {count}\n"
    
    report += "\n## 🔥 Top Patterns\n"
    if top_patterns:
        for i, p in enumerate(top_patterns, 1):
            status = "🎯 PROMOTED" if p.get("promoted") else f"({p.get('count', 0)}/{3} to promote)"
            report += f"{i}. **{p.get('key', '?')[:80]}** — {p.get('count', 0)}x {status}\n"
    else:
        report += "_No patterns detected yet._\n"
    
    report += "\n## ⬆️ New Rules Promoted\n"
    if new_rules:
        for r in new_rules:
            report += f"- **{r.get('id', '?')}:** {r.get('rule', '?')}\n"
    else:
        report += "_No new rules promoted this week._\n"
    
    report += f"""
## 📈 Total Knowledge Base
- **Active rules:** {len([r for r in genes.get('rules', []) if r.get('active')])}
- **Total patterns tracked:** {len(patterns.get('patterns', []))}
- **Total events (all time):** {sum(1 for _ in open(EVENTS_FILE)) if os.path.exists(EVENTS_FILE) and os.path.getsize(EVENTS_FILE) > 0 else 0}
"""
    
    # Save
    os.makedirs(REPORTS_DIR, exist_ok=True)
    filename = f"WEEKLY_REPORT_{year}_W{week_num:02d}.md"
    filepath = os.path.join(REPORTS_DIR, filename)
    with open(filepath, "w") as f:
        f.write(report)
    
    print(f"Report saved: {filepath}")
    print(report)
    return filepath


if __name__ == "__main__":
    generate_report()
