#!/usr/bin/env python3
"""
regressions_guardrail.py - Failure-to-Guardrail Pipeline

Scans REGRESSIONS.md for new failure entries and surfaces actionable rules
during heartbeat to ensure they are applied and never forgotten.

Process:
- Extract all failure entries and their rule blocks
- Print a concise summary of current active guardrails
- Optionally can update HEARTBEAT.md or generate guardrails_active.json (future)
"""

import re
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/home/node/.openclaw/workspace")
REGRESSIONS_MD = WORKSPACE / "REGRESSIONS.md"
HEARTBEAT_MD = WORKSPACE / "HEARTBEAT.md"

def extract_rules():
    """Parse REGRESSIONS.md and return list of {date, summary, details}."""
    if not REGRESSIONS_MD.exists():
        return []
    
    text = REGRESSIONS_MD.read_text(encoding="utf-8")
    
    # Pattern: ### YYYY-MM-DD Description ... then "**Rules**:"
    # We'll find all sections that start with ### and capture the rule block
    pattern = r'###\s+(\d{4}-\d{2}-\d{2})\s+[^\n]*?\n.*?\n\*\*Rules\*\*:\s*\n((?:-(?:.|\n)*?)(?=\n###|\Z))'
    matches = re.findall(pattern, text, re.DOTALL)
    
    rules = []
    for date, rule_block in matches:
        # Clean: get list of rule lines (starting with "- ")
        lines = []
        for line in rule_block.splitlines():
            stripped = line.strip()
            if stripped.startswith('- '):
                lines.append(stripped[2:])  # remove "- "
        if lines:
            rules.append({
                "date": date,
                "summary": lines[0],
                "details": lines
            })
    return rules

def apply_guardrails():
    """Run guardrail check and output active rules."""
    rules = extract_rules()
    
    if not rules:
        print("\n🛡️  Guardrail: No failure rules found in REGRESSIONS.md")
        return
    
    print("\n🛡️  Active Guardrail Rules (from REGRESSIONS.md):\n")
    for idx, r in enumerate(rules, 1):
        print(f"{idx}. [{r['date']}] {r['summary']}")
        for detail in r['details'][1:]:  # skip summary as already printed
            print(f"   • {detail}")
    print(f"\nTotal {len(rules)} guardrail rule(s).\n")
    
    # Future: can automatically inject these into HEARTBEAT.md or guardrails_active.json
    # For now, just printing ensures we see them during each heartbeat and can't forget.

if __name__ == "__main__":
    apply_guardrails()
