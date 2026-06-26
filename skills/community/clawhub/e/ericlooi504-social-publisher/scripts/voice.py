#!/usr/bin/env python3
"""
Brand Voice Manager — Help Reference
"""
import sys

HELP = """
🎙️ Brand Voice Manager

Commands (run by agent):
  python3 scripts/voice.py set --name my-brand --tone professional
  python3 scripts/voice.py list
  python3 scripts/voice.py apply --voice my-brand --input draft.md
"""

if __name__ == "__main__":
    print(HELP)
