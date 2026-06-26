#!/usr/bin/env python3
"""
Social Media Content Generator — Help Reference
The agent generates posts and calendars directly from SKILL.md instructions.
"""
import sys

HELP = """
📱 Social Media Content Generator

Commands (run by agent):
  python3 scripts/generate.py post --topic "X" --platform twitter --count 5
  python3 scripts/generate.py calendar --theme "X" --weeks 4
  python3 scripts/generate.py repurpose --input post.md
"""

if __name__ == "__main__":
    print(HELP)
