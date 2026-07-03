#!/usr/bin/env python3
"""Create a new Animeblip project (series) + its first episode (story).

In Animeblip's data model a Story IS an episode and a Series IS a project; this mints a
brand-new series and its episode 1 in one call. Add later episodes with create_episode.py.

Stories created here auto-approve video generation (videoConfirmation=always_allow),
so generation never stalls on the app's per-video confirmation. Any review/approval
before publish or the next episode is something YOU (the driving agent) choose to do.

Usage:
    create_project.py --title T [--idea ..] [--genre ..] [--tone ..]
                    [--aspect 9:16] [--lang en] [--dry-run]

ART STYLE: the skill uses ONE fixed art style (the "Anime6" preset) for every story —
do NOT pass a style. To use a different art style, change it on the website (the
storyboard editor); the skill does not select styles.

Returns: {"status", "storyId", "error"}
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _common import api_create_story, print_json

# The single, fixed art style every story is created with (the "Anime6" preset). The skill
# does NOT let the agent choose a style — to change it, the user updates it on the website.
DEFAULT_ART_STYLE_ID = "723542b2-ddfa-4bf7-8125-dd612373588a"


def main():
    ap = argparse.ArgumentParser(description="Create a new Animeblip story (ep1, new series).")
    ap.add_argument("--title")
    ap.add_argument("--idea")
    ap.add_argument("--genre")
    ap.add_argument("--tone")
    # Accepted but IGNORED — the skill uses one fixed art style (see below). Kept so an
    # agent that still passes --style doesn't error.
    ap.add_argument("--style", help=argparse.SUPPRESS)
    ap.add_argument("--aspect", default="9:16")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    # Art style is HARD-CODED to the skill's single supported preset (Anime6). Whatever the
    # caller passes in --style is intentionally ignored. To use a different art style, change
    # it on the website (the storyboard editor) — the skill does not pick styles.
    style = DEFAULT_ART_STYLE_ID

    if args.dry_run:
        print(f"DRY: would POST /api/stories (artStyleId={style}, "
              f"videoConfirmation=always_allow). No spend.")
        return

    code, j = api_create_story(args.title, args.idea, args.genre, args.tone, style,
                               args.aspect, args.lang)
    print_json({"status": code, "storyId": j.get("storyId"), "error": j.get("error")}, indent=None)


if __name__ == "__main__":
    main()
