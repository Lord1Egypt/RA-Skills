#!/usr/bin/env python3
"""
friction_detector.py - Friction Detection

Analyzes recent failures (from REGRESSIONS.md) to identify workflow bottlenecks
and suggest optimizations. Runs during heartbeat to keep us aware of friction
points and ensure we continuously improve.

Output format: concise markdown-style report for quick reading.
"""

import re
from pathlib import Path
from collections import Counter
from datetime import datetime, timedelta

WORKSPACE = Path("/home/node/.openclaw/workspace")
REGRESSIONS_MD = WORKSPACE / "REGRESSIONS.md"

# Category mapping based on failure descriptions (generic keywords)
CATEGORY_PATTERNS = {
    "network_block": [
        r"403",
        r"blocked",
        r"cloudflare",
        r"access.*denied",
        r"network.*fail",
        r"timeout",
        r"unreachable"
    ],
    "third_party_service": [
        r"x\.com",
        r"twitter",
        r"twitter\.com",
        r"third.*party",
        r"external.*site",
        r"api.*fail"
    ],
    "silent_wait": [
        r"silent",
        r"unresponsive",
        r"hang",
        r"stuck",
        r"no.*response",
        r"long.*wait"
    ],
    "model_selection": [
        r"model",
        r"switch.*model",
        r"invalid.*model",
        r"model.*timeout"
    ],
    "tool_error": [
        r"tool.*fail",
        r"exec.*error",
        r"read.*error",
        r"command.*failed"
    ]
}

def parse_friction_entries():
    """Parse REGRESSIONS.md and return list of {date, description}."""
    if not REGRESSIONS_MD.exists():
        return []
    
    text = REGRESSIONS_MD.read_text(encoding="utf-8")
    
    # Pattern: ### YYYY-MM-DD Description ... then "Failure:" line then "**Rules**:"
    pattern = r'###\s+(\d{4}-\d{2}-\d{2})\s+[^\n]*?\n.*?\nFailure:\s*(.+?)\n\*\*Rules\*\*:'
    matches = re.findall(pattern, text, re.DOTALL)
    
    entries = []
    for date_str, description in matches:
        # Clean description (take first line)
        desc_line = description.split('\n')[0].strip()
        entries.append({
            "date": date_str,
            "description": desc_line
        })
    return entries

def categorize_friction(description):
    """Assign friction category based on description keywords."""
    desc_low = description.lower()
    for category, patterns in CATEGORY_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, desc_low, re.IGNORECASE):
                return category
    return "other"

def compute_friction_stats(entries, days_back=7):
    """Stat friction counts over recent days."""
    cutoff = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    recent = [e for e in entries if e["date"] >= cutoff]
    total = len(recent)
    
    if total == 0:
        return None
    
    # Count by category
    cat_counter = Counter()
    for e in recent:
        cat = categorize_friction(e["description"])
        cat_counter[cat] += 1
    
    # Top frictions
    top3 = cat_counter.most_common(3)
    
    return {
        "total": total,
        "period_days": days_back,
        "categories": dict(cat_counter),
        "top3": top3
    }

def generate_report(stats):
    """Create human-friendly friction report."""
    lines = [
        "🛠️  Friction Detection Report",
        "--------------------------------",
        f"Last {stats['period_days']} days: {stats['total']} friction(s) recorded",
        ""
    ]
    
    if not stats['categories']:
        lines.append("✅ No significant frictions detected.")
        return "\n".join(lines)
    
    lines.append("Top friction categories:")
    for cat, count in stats['top3']:
        pct = (count / stats['total']) * 100
        lines.append(f"• {cat}: {count} ({pct:.0f}%)")
    
    lines.append("")
    lines.append("🔧 Recommendations:")
    
    # Suggest based on top category
    top_cat = stats['top3'][0][0]
    if top_cat == "network_block":
        lines.append(" - Use search fallback (e.g., tavily) for blocked sites; avoid repeated direct fetches.")
    elif top_cat == "third_party_service":
        lines.append(" - Use model-based retrieval (e.g., grok42) for third-party services like X/Twitter.")
    elif top_cat == "silent_wait":
        lines.append(" - Send periodic progress on long operations; break into smaller steps.")
    elif top_cat == "model_selection":
        lines.append(" - Cache best-performing model per task type; auto-select on recurrence.")
    elif top_cat == "tool_error":
        lines.append(" - Review tool errors and add guardrails or retry logic.")
    else:
        lines.append(" - Investigate recurring failures and convert to guardrail rules.")
    
    lines.append("")
    lines.append("See REGRESSIONS.md for full history and stored guardrails.")
    return "\n".join(lines)

def detect_frictions():
    """Main entry: extract, analyze, print report."""
    entries = parse_friction_entries()
    if not entries:
        print("\n🛠️  Friction Detection: No failure records found yet.\n")
        return
    
    stats = compute_friction_stats(entries)
    if not stats:
        print("\n🛠️  Friction Detection: No recent frictions (within period).\n")
        return
    
    report = generate_report(stats)
    print(report)

if __name__ == "__main__":
    detect_frictions()
