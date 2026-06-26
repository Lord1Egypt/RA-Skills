#!/usr/bin/env python3
"""
E-commerce Price Monitor — Report Generator
This is a help reference. The agent generates reports inline.
"""
import sys

HELP = """
📊 Price Report Generator

Usage (run by agent):
  python3 scripts/report.py              — Show summary
  python3 scripts/report.py --csv        — Export CSV
  python3 scripts/report.py --product N  — Single product history
  python3 scripts/report.py --trends     — Trend analysis

Reports saved to reports/ directory.
"""

if __name__ == "__main__":
    print(HELP)
