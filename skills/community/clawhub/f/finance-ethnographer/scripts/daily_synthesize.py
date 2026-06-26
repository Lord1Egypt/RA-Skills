#!/usr/bin/env python3
"""
daily_synthesize.py
Finance UX Daily Synthesizer – runs at 23:55 America/Los_Angeles via cron.

Reads:   ~/.openclaw/skills/finance-ux-observer/data/observations/YYYY-MM-DD.jsonl
Writes:  ~/.openclaw/skills/finance-ux-observer/reports/YYYY-MM-DD/
           raw_observations.md
           insights.md
Then calls redact_reports.py to produce *.REDACTED.md versions.
"""

import json
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

SKILL_DIR        = Path(__file__).resolve().parent.parent
SKILL_DATA       = SKILL_DIR / "data"
OBSERVATIONS_DIR = SKILL_DATA / "observations"
REPORTS_BASE     = SKILL_DIR / "reports"


# ── Load ───────────────────────────────────────────────────────────────────────

def load_observations(target_date: str) -> List[Dict[str, Any]]:
    obs_file = OBSERVATIONS_DIR / f"{target_date}.jsonl"
    if not obs_file.exists():
        return []
    rows = []
    with open(obs_file, errors="replace") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return rows


# ── Raw observations report ────────────────────────────────────────────────────

def build_raw_md(observations: List[Dict[str, Any]], target_date: str) -> str:
    now = datetime.now(tz=timezone.utc).isoformat()
    lines = [
        "# Finance UX Observer — Raw Observations",
        "",
        f"**Date:** {target_date}  ",
        f"**Generated:** {now}  ",
        f"**Total observations:** {len(observations)}  ",
        "",
        "> ⚠️ DO NOT SHARE THIS FILE. Share only: `raw_observations.REDACTED.md`",
        "",
        "---",
        "",
    ]

    if not observations:
        lines.append("_No observations recorded for this date._")
        return "\n".join(lines)

    for i, obs in enumerate(observations, 1):
        tags   = obs.get("finance_topic_tags", [])
        tools  = obs.get("tools_actions_observed", [])
        sigs   = obs.get("ux_signals", [])
        quotes = obs.get("notable_quotes", [])

        lines += [
            f"## Observation {i} — `{obs.get('observation_id', f'obs_{i:04d}')}`",
            "",
            f"| | |",
            f"|---|---|",
            f"| **Timestamp** | `{obs.get('timestamp', 'n/a')}` |",
            f"| **Session** | `{obs.get('session_key', 'unknown')}` |",
            f"| **Channel** | {obs.get('channel', 'main')} |",
            "",
            "### What the user tried",
            obs.get("what_user_tried", "_not recorded_"),
            "",
            "### Finance topic tags",
            ", ".join(f"`{t}`" for t in tags) if tags else "_none_",
            "",
            "### Tools observed",
            ", ".join(f"`{t}`" for t in tools) if tools else "_none_",
            "",
            "### UX signals",
            ", ".join(f"`{s}`" for s in sigs) if sigs else "_none_",
            "",
            "### Notable quotes",
        ]
        if quotes:
            lines.extend(f"> {q}" for q in quotes)
        else:
            lines.append("_none_")
        lines += [
            "",
            "### Researcher notes",
            obs.get("researcher_notes", "_none_"),
            "",
            "---",
            "",
        ]

    return "\n".join(lines)


# ── Insights report ────────────────────────────────────────────────────────────

def build_insights_md(observations: List[Dict[str, Any]], target_date: str) -> str:
    now = datetime.now(tz=timezone.utc).isoformat()

    if not observations:
        return "\n".join([
            "# Finance UX Observer — Daily Insights",
            "",
            f"**Date:** {target_date}  ",
            f"**Generated:** {now}  ",
            "",
            "_No observations recorded. Verify the observer cron job is running._",
            "",
            "```bash",
            "crontab -l | grep finance-ux-observer",
            "```",
        ])

    # Aggregates
    all_topics:  List[str] = []
    all_signals: List[str] = []
    all_tools:   List[str] = []
    sessions:    set        = set()

    for obs in observations:
        all_topics.extend(obs.get("finance_topic_tags", []))
        all_signals.extend(obs.get("ux_signals", []))
        all_tools.extend(obs.get("tools_actions_observed", []))
        sessions.add(obs.get("session_key", ""))

    topic_counts  = Counter(all_topics)
    signal_counts = Counter(all_signals)
    tool_counts   = Counter(all_tools)

    def by_signal(sig: str) -> List[Dict[str, Any]]:
        return [o for o in observations if sig in o.get("ux_signals", [])]

    friction_obs    = by_signal("friction")
    confusion_obs   = by_signal("confusion")
    delight_obs     = by_signal("delight")
    workaround_obs  = by_signal("workaround")
    abandonment_obs = by_signal("abandonment")
    pain_obs        = friction_obs + confusion_obs

    topic_to_obs: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for obs in observations:
        for tag in obs.get("finance_topic_tags", []):
            topic_to_obs[tag].append(obs)

    lines = [
        "# Finance UX Observer — Daily Insights",
        "",
        f"**Date:** {target_date}  ",
        f"**Generated:** {now}  ",
        f"**Observation windows:** {len(observations)}  ",
        f"**Unique sessions:** {len(sessions)}  ",
        "",
        "> ⚠️ DO NOT SHARE THIS FILE. Share only: `insights.REDACTED.md`",
        "",
        "---",
        "",
        "## Executive Summary",
        "",
    ]

    if topic_counts:
        top3 = [f"**{t}**" for t, _ in topic_counts.most_common(3)]
        lines.append("Dominant finance topics today: " + ", ".join(top3) + ".")
    if signal_counts:
        dom, cnt = signal_counts.most_common(1)[0]
        lines.append(f"Most common UX signal: **{dom}** ({cnt} instance{'s' if cnt != 1 else ''}).")

    lines += ["", "---", "", "## Finance Topics Observed", ""]
    if topic_counts:
        total = sum(topic_counts.values())
        lines += ["| Topic | Count | % |", "|-------|-------|---|"]
        for topic, count in topic_counts.most_common():
            lines.append(f"| `{topic}` | {count} | {count/total*100:.0f}% |")
    else:
        lines.append("_None detected._")

    SIGNAL_INTERP = {
        "confusion":   "User expressed confusion or asked clarifying questions",
        "friction":    "User encountered difficulty or repeated failures",
        "delight":     "User expressed satisfaction or success",
        "workaround":  "User found an alternative path around a blocked flow",
        "abandonment": "User gave up on a task or abruptly changed direction",
    }
    lines += ["", "---", "", "## UX Signal Summary", ""]
    if signal_counts:
        lines += ["| Signal | Count | Interpretation |", "|--------|-------|----------------|"]
        for sig, cnt in signal_counts.most_common():
            lines.append(f"| `{sig}` | {cnt} | {SIGNAL_INTERP.get(sig, '')} |")
    else:
        lines.append("_None detected._")

    lines += ["", "---", "", "## Behavioral Patterns by Topic", ""]
    for topic, obs_list in sorted(topic_to_obs.items(), key=lambda x: -len(x[1])):
        lines += [f"### {topic.replace('_', ' ').title()}", ""]
        lines.append(f"**{len(obs_list)} window(s)**")
        for obs in obs_list[:4]:
            what = obs.get("what_user_tried", "")[:150]
            sigs = obs.get("ux_signals", [])
            sig_str = f" _{', '.join(sigs)}_" if sigs else ""
            lines.append(f"- {what}{sig_str}")
        lines.append("")

    lines += ["---", "", "## Pain Points & Friction", ""]
    if pain_obs:
        for obs in pain_obs[:6]:
            topics_str = ", ".join(obs.get("finance_topic_tags", ["general"]))
            sigs_str   = ", ".join(obs.get("ux_signals", []))
            lines.append(f"- **[{topics_str}]** `{sigs_str}`  ")
            lines.append(f"  {obs.get('what_user_tried', '')[:150]}")
    else:
        lines.append("_None detected._")

    lines += ["", "---", "", "## Delight Moments", ""]
    if delight_obs:
        for obs in delight_obs[:4]:
            topics_str = ", ".join(obs.get("finance_topic_tags", ["general"]))
            lines.append(f"- **[{topics_str}]** {obs.get('what_user_tried', '')[:150]}")
    else:
        lines.append("_None detected._")

    lines += ["", "---", "", "## Workarounds", ""]
    if workaround_obs:
        for obs in workaround_obs[:4]:
            topics_str = ", ".join(obs.get("finance_topic_tags", ["general"]))
            lines.append(f"- **[{topics_str}]** {obs.get('what_user_tried', '')[:150]}")
        lines.append("\n_Each workaround is a feature request in disguise._")
    else:
        lines.append("_None detected._")

    lines += ["", "---", "", "## Abandonment Signals", ""]
    if abandonment_obs:
        for obs in abandonment_obs[:4]:
            topics_str = ", ".join(obs.get("finance_topic_tags", ["general"]))
            lines.append(f"- **[{topics_str}]** {obs.get('what_user_tried', '')[:150]}")
    else:
        lines.append("_None detected._")

    UNMET_NEEDS = {
        "budgeting":          "Guided budget setup wizard or ready-made templates",
        "investing":          "Jargon-free investment explanations with comparison tools",
        "retirement":         "Step-by-step retirement planning workflow",
        "taxes":              "Tax estimation, scenario modeling, or filing checklist",
        "crypto":             "Plain-language crypto risk/reward education",
        "scenario_planning":  "Interactive financial modeling with what-if sliders",
        "savings":            "Goal-based savings tracking with progress visualization",
        "household_budgeting":"Household expense categorization with shared access",
        "debt":               "Side-by-side debt payoff strategy comparison",
        "insurance":          "Coverage gap analysis and plain-English policy comparison",
        "estate_planning":    "Step-by-step estate checklist with beneficiary management",
        "social_spending":    "Group expense splitting with settlement suggestions",
        "spending":           "Automated spending pattern detection and anomaly alerts",
        "shopping":           "Price history tracking and deal alerting",
        "financial_advice":   "Personalized financial health score with next steps",
    }

    pain_topics = []
    for obs in pain_obs + abandonment_obs + workaround_obs:
        pain_topics.extend(obs.get("finance_topic_tags", []))

    lines += ["", "---", "", "## Inferred Unmet Needs", "",
              "_Derived from friction + confusion + abandonment observations:_", ""]
    printed = set()
    for topic in sorted(set(pain_topics)):
        if topic in UNMET_NEEDS and topic not in printed:
            lines.append(f"- **{topic.replace('_', ' ').title()}:** {UNMET_NEEDS[topic]}")
            printed.add(topic)
    if not printed:
        lines.append("_Insufficient signal today._")

    lines += ["", "---", "", "## Tools & Actions Observed", ""]
    if tool_counts:
        lines += ["| Tool | Uses |", "|------|------|"]
        for tool, count in tool_counts.most_common(12):
            lines.append(f"| `{tool}` | {count} |")
    else:
        lines.append("_None recorded._")

    # Recommendations
    recs = []
    if signal_counts.get("confusion", 0) >= 2:
        recs.append("**Improve clarity** for the most-confused finance workflows.")
    if signal_counts.get("friction", 0) >= 2:
        recs.append("**Streamline friction-heavy flows** (see Pain Points above).")
    if workaround_obs:
        recs.append("**Investigate workarounds** — each one is a hidden feature gap.")
    if abandonment_obs:
        recs.append("**Analyze abandonment triggers** to find where motivation breaks down.")
    if not recs:
        recs.append("_No specific recommendations today — usage appeared smooth._")

    lines += ["", "---", "", "## Recommendations", ""]
    for i, rec in enumerate(recs, 1):
        lines.append(f"{i}. {rec}")

    lines += [
        "",
        "---",
        "",
        "## Pre-Share Checklist",
        "",
        "- [ ] Reviewed `insights.REDACTED.md` (not this file)",
        "- [ ] Verified no PII in the redacted version",
        "- [ ] Attaching only `*.REDACTED.md` files",
        "",
    ]

    return "\n".join(lines)


# ── Write + redact ─────────────────────────────────────────────────────────────

def write_reports(target_date: str, raw_md: str, insights_md: str) -> Path:
    report_dir = REPORTS_BASE / target_date
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "raw_observations.md").write_text(raw_md, encoding="utf-8")
    (report_dir / "insights.md").write_text(insights_md, encoding="utf-8")
    return report_dir


def trigger_redaction(report_dir: Path) -> bool:
    redact_script = SKILL_DIR / "scripts" / "redact_reports.py"
    try:
        r = subprocess.run(
            [sys.executable, str(redact_script), str(report_dir)],
            capture_output=True, text=True, timeout=120,
        )
        return r.returncode == 0
    except (subprocess.TimeoutExpired, OSError):
        return False


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    target_date  = date.today().isoformat()
    observations = load_observations(target_date)

    topic_counts  = Counter(t for o in observations for t in o.get("finance_topic_tags", []))
    signal_counts = Counter(s for o in observations for s in o.get("ux_signals", []))

    raw_md      = build_raw_md(observations, target_date)
    insights_md = build_insights_md(observations, target_date)
    report_dir  = write_reports(target_date, raw_md, insights_md)
    redacted_ok = trigger_redaction(report_dir)

    top_topics  = [t for t, _ in topic_counts.most_common(3)]
    top_signals = [s for s, _ in signal_counts.most_common(2)]
    redact_msg  = "✅ Complete" if redacted_ok else "⚠️  Run `redact_reports.py` manually"

    print(f"""## 🔬 Finance UX Observer — Daily Report Ready

**Date:** {target_date}
**Observations:** {len(observations)}
**Top topics:** {', '.join(f'`{t}`' for t in top_topics) or '_none_'}
**Top signals:** {', '.join(f'`{s}`' for s in top_signals) or '_none_'}
**Redaction:** {redact_msg}

### Reports saved to
`{report_dir}/`

| File | Share? |
|------|--------|
| `raw_observations.md` | ❌ No — may contain PII |
| `raw_observations.REDACTED.md` | ✅ Yes |
| `insights.md` | ❌ No — may contain PII |
| `insights.REDACTED.md` | ✅ Yes |

**Next steps:** Review the two REDACTED files, then use the email template in SKILL.md to share with your research team.
""")


if __name__ == "__main__":
    main()
