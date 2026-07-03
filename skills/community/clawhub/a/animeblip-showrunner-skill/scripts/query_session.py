#!/usr/bin/env python3
"""Read one status snapshot for a story (the raw /api/chat/session = query_session payload).

Includes state, toolLogsSummary, finalVideoUrl/finalVideoStatus, the structured failures[]
({op, scene, error}) you triage on, and — when --after-seq is given — the agent's new
messages[] ({role, text, sequenceNumber}) plus the next cursor. This is your poll channel:
read it on a cadence (~60s) until the final video appears or a failure/question needs you.
See docs/triage-rules.md.

Usage:
    query_session.py --story S [--after-seq N]

Returns: the full status JSON (pretty-printed).
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _common import api_status, print_json


def main():
    ap = argparse.ArgumentParser(description="Read one Animeblip story status snapshot.")
    ap.add_argument("--story", required=True)
    ap.add_argument("--after-seq", type=int, default=None,
                    help="Message cursor: pass the previous read's cursor (0 first time) to also get new agent messages[] since it.")
    args = ap.parse_args()

    code, j = api_status(args.story, after_seq=args.after_seq)
    print_json(j)


if __name__ == "__main__":
    main()
