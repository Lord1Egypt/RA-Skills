#!/usr/bin/env python3
"""Create the next episode in an existing series (reuses its characters/elements).

Creates an empty episode shell that inherits the source story's per-episode settings
(genre, tone, art style, aspect, models, language) AND its videoConfirmation gate, so
ep2+ needs no new human confirmation. Drive the new episode with send_message.py.
Creating the shell does NOT spend credits.

Usage:
    create_episode.py --from S [--dry-run]

Returns: {"status", "storyId", "seriesId", "error"}
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _common import api_next_episode, print_json


def main():
    ap = argparse.ArgumentParser(description="Create the next episode in an Animeblip series.")
    ap.add_argument("--from", dest="from_story", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.dry_run:
        print(f"DRY: would POST /api/stories/{args.from_story}/next-episode. No spend (creates shell only).")
        return

    code, j = api_next_episode(args.from_story)
    print_json({"status": code, "storyId": j.get("storyId"), "seriesId": j.get("seriesId"), "error": j.get("error")}, indent=None)


if __name__ == "__main__":
    main()
