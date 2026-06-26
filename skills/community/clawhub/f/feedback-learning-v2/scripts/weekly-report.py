#!/usr/bin/env python3
"""Generate weekly learning report from events and genes."""
import json, os
from datetime import datetime, timedelta
from collections import Counter

DIR = os.environ.get("FEEDBACK_LEARNING_DIR", os.path.expanduser("~/.openclaw/shared/learning"))
EVENTS_PATH = os.path.join(DIR, "events.jsonl")
GENES_PATH = os.path.join(DIR, "genes.json")
PATTERNS_PATH = os.path.join(DIR, "patterns.json")
REPORTS_DIR = os.path.join(DIR, "reports")

def load_events_since(days=7):
    cutoff = datetime.utcnow() - timedelta(days=days)
    events = []
    if not os.path.exists(EVENTS_PATH):
        return events
    with open(EVENTS_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
                ts = ev.get("ts", "")
                try:
                    ev_dt = datetime.fromisoformat(ts.replace("Z", "+00:00").replace("+00:00", ""))
                except:
                    continue
                if ev_dt >= cutoff:
                    events.append(ev)
            except json.JSONDecodeError:
                continue
    return events

def load_json(path, default=None):
    if not os.path.exists(path):
        return default or {}
    with open(path) as f:
        return json.load(f)

def main():
    now = datetime.utcnow()
    week_str = now.strftime("%Y-%m-%d")
    
    events = load_events_since(7)
    genes = load_json(GENES_PATH, {"rules": []})
    patterns = load_json(PATTERNS_PATH, {"patterns": {"negative": [], "positive": []}})

    # Stats
    type_counts = Counter(e.get("type", "unknown") for e in events)
    agent_counts = Counter(e.get("agent", "unknown") for e in events)
    source_counts = Counter(e.get("source", "unknown") for e in events)

    rules = genes.get("rules", [])
    active_rules = [r for r in rules if r.get("status") == "active"]
    stale_rules = [r for r in rules if r.get("status") == "stale"]
    resolved_rules = [r for r in rules if r.get("status") in ("resolved", "wont-fix")]

    neg_patterns = patterns.get("patterns", {}).get("negative", [])
    pos_patterns = patterns.get("patterns", {}).get("positive", [])

    # Generate report
    report = []
    report.append(f"# Weekly Learning Report — {week_str}")
    report.append(f"*Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}*\n")

    report.append(f"## 📊 Summary")
    report.append(f"- **Events this week:** {len(events)}")
    report.append(f"- **By type:** {', '.join(f'{t}: {c}' for t, c in type_counts.most_common())}")
    report.append(f"- **By agent:** {', '.join(f'{a}: {c}' for a, c in agent_counts.most_common())}")
    report.append(f"- **By source:** {', '.join(f'{s}: {c}' for s, c in source_counts.most_common())}")
    report.append("")

    report.append(f"## 🧬 Gene Health")
    report.append(f"- Active: **{len(active_rules)}** | Stale: **{len(stale_rules)}** | Resolved: **{len(resolved_rules)}**")
    report.append("")

    if active_rules:
        report.append("### Active Rules")
        for r in active_rules[:10]:
            report.append(f"- `{r['id']}` ({r.get('type','?')}, {r.get('occurrences',0)}x): {r.get('condition','?')} → {r.get('action','?')}")
        report.append("")

    if stale_rules:
        report.append("### ⚠️ Stale Rules (need review)")
        for r in stale_rules[:5]:
            report.append(f"- `{r['id']}`: {r.get('condition','?')}")
        report.append("")

    report.append(f"## 📈 Patterns")
    report.append(f"- Negative patterns tracked: **{len(neg_patterns)}**")
    report.append(f"- Positive patterns tracked: **{len(pos_patterns)}**")
    report.append("")

    # Top negative patterns
    if neg_patterns:
        top_neg = sorted(neg_patterns, key=lambda p: p.get("count", 0), reverse=True)[:5]
        report.append("### Top Negative Patterns")
        for p in top_neg:
            report.append(f"- ({p.get('count',0)}x) {p.get('key_text', p.get('key', '?'))}")
        report.append("")

    # Top positive patterns
    if pos_patterns:
        top_pos = sorted(pos_patterns, key=lambda p: p.get("count", 0), reverse=True)[:5]
        report.append("### Top Positive Patterns")
        for p in top_pos:
            report.append(f"- ({p.get('count',0)}x) {p.get('key_text', p.get('key', '?'))}")
        report.append("")

    # Recent notable events
    if events:
        report.append("## 🔍 Notable Events")
        corrections = [e for e in events if e.get("type") == "correction"][:5]
        for e in corrections:
            report.append(f"- [{e.get('agent','?')}] {e.get('context','?')}: \"{e.get('signal','?')}\" → {e.get('hint','?')}")
        report.append("")

    report_text = "\n".join(report)

    # Save report
    os.makedirs(REPORTS_DIR, exist_ok=True)
    report_path = os.path.join(REPORTS_DIR, f"WEEKLY_{week_str}.md")
    with open(report_path, "w") as f:
        f.write(report_text)

    print(f"✅ Report saved: {report_path}")
    print(f"   Events: {len(events)} | Genes: {len(active_rules)} active, {len(stale_rules)} stale")

if __name__ == "__main__":
    main()
