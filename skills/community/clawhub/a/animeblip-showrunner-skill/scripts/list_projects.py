#!/usr/bin/env python3
"""List the projects (series) on this account — paged — to find one to resume.

A "project" = a SERIES. Each project is returned with its FULL episode list
({order, storyId}), so you can drive any existing episode (send_message.py /
query_session.py with its storyId) or start the next one (create_episode.py --from
the latest episode's storyId). Hits GET /api/series?limit&cursor.

Usage:
    list_projects.py [--limit 20] [--cursor C] [--dry-run]

Returns: {"status", "projects": [{seriesId, title, episodeCount,
          episodes: [{order, storyId}]}], "nextCursor", "error"}
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _common import api_list_projects, print_json


def main():
    ap = argparse.ArgumentParser(description="List Animeblip projects (series) with their episodes.")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--cursor", default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.dry_run:
        print(f"DRY: would GET /api/series?limit={args.limit}{'&cursor=' + args.cursor if args.cursor else ''}. No spend.")
        return

    code, j = api_list_projects(args.limit, args.cursor)
    series = j.get("series") or []
    projects = []
    for s in series:
        eps = sorted(s.get("episodes") or [], key=lambda e: e.get("order") or 0)
        projects.append({
            "seriesId": s.get("seriesId", ""),
            "title": s.get("title") or "(untitled)",
            "episodeCount": s.get("episodeCount", len(eps)),
            "episodes": [{"order": e.get("order"), "storyId": e.get("storyId")} for e in eps],
        })
    print_json({"status": code, "projects": projects,
                "nextCursor": j.get("nextCursor"), "error": j.get("error")})


if __name__ == "__main__":
    main()
