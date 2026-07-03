#!/usr/bin/env python3
"""Read a story's project state — the review channel.

Status can't show the content; this returns the screenplay scene-by-scene PLUS the
series characters[] and elements[] (each with its reference design image), so you (the
producer) can critique the story AND the character/element designs before paying for
images/video. Read it between scoped steps to review before paying for the next.

Usage:
    get_project_state.py --story S

Returns: the full project-state JSON (pretty-printed) — the same canonical state the
production agent sees:
  - top-level: videoWorkflow (reference | start-frame | storyboard-grid — decides whether
    scene images are needed), artStyleName, aspectRatio
  - scenes[]: order, visualDescription, characterKeys, elementKeys, durationSec, startSec,
    hasImage, hasMotion, imageUrl, videoUrl
  - characters[]: key, name, description, appearance, status, hasUploadedRefs, imageUrl
  - elements[]: key, name, type (location|prop), description, status, imageUrl
  - episodes[]: the series manifest

IMPORTANT — a scene image/video is only DONE when its url is present. hasImage/hasMotion are
true only for a READY asset, but always confirm success via imageUrl != null / videoUrl != null;
a failed/blocked generation shows no url. If a scene has no videoUrl, read query_session
failures[] for the reason (e.g. copyright). Use description/appearance/status to critique the
actual designs; videoWorkflow to plan steps.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _common import api_project_state, print_json


def main():
    ap = argparse.ArgumentParser(description="Read an Animeblip story's project state (scenes + characters + elements).")
    ap.add_argument("--story", required=True)
    args = ap.parse_args()

    code, j = api_project_state(args.story)
    print_json(j)


if __name__ == "__main__":
    main()
