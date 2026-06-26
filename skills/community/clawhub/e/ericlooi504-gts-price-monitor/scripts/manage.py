#!/usr/bin/env python3
"""
E-commerce Price Monitor — Data Management
This is a help reference. The agent performs price tracking via web fetch.
Usage info only — see SKILL.md for full workflow.
"""
import sys

HELP = """
📊 E-Commerce Price Monitor

Commands (run by agent, not user):
  python3 scripts/manage.py products add <url>      — Add product
  python3 scripts/manage.py products list            — List tracked products
  python3 scripts/manage.py products remove <id>     — Remove product
  python3 scripts/manage.py alerts add               — Create alert
  python3 scripts/manage.py alerts list              — List alerts
  python3 scripts/manage.py alerts remove <id>       — Remove alert
  python3 scripts/manage.py history export --days 30 — Export CSV report

Data stored in scripts/prices.json and scripts/price_history.jsonl
"""

if __name__ == "__main__":
    print(HELP)
