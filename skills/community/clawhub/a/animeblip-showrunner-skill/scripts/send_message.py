#!/usr/bin/env python3
"""Send a message to a story's production agent — VERBATIM (instruction-driven).

This sends exactly what you pass in `--message`, with nothing appended. End-to-end vs
step-by-step is decided by WHAT you send, not a flag:
  • Full pipeline in one shot → include an end-to-end instruction in the message
    (e.g. "… Produce the complete final video end-to-end — do not stop for input.").
  • One scoped step → send a scoped instruction (e.g. "Write the screenplay only, then
    stop."), poll query_session, read get_project_state, critique, then send the next step.

Usage:
    send_message.py --story S --message "..." [--dry-run]

Returns: {"status", "runId", "error"}
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _common import api_send, print_json


def main():
    ap = argparse.ArgumentParser(description="Send a verbatim message to an Animeblip story's agent.")
    ap.add_argument("--story", required=True)
    ap.add_argument("--message", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    # Verbatim — nothing appended. The caller decides scope (full brief vs scoped step).
    msg = args.message
    if args.dry_run:
        print(f"DRY: would POST /api/chat for {args.story} with message (verbatim):")
        print(msg)
        return

    code, j = api_send(args.story, msg)
    print_json({"status": code, "runId": j.get("runId"), "error": j.get("error")}, indent=None)


if __name__ == "__main__":
    main()
