#!/usr/bin/env python3
"""
Content Calendar Manager — Help Reference
"""
import sys

HELP = """
📅 Content Calendar Manager

Commands (run by agent):
  python3 scripts/calendar.py create --month may --theme X
  python3 scripts/calendar.py view
  python3 scripts/calendar.py export --csv
  python3 scripts/calendar.py add --date YYYY-MM-DD --platform X --topic "Y"
"""

if __name__ == "__main__":
    print(HELP)
