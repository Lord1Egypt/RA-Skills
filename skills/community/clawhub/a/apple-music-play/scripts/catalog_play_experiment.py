#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from typing import List

ITUNES_SEARCH_URL = "https://itunes.apple.com/search"


def run(cmd):
    return subprocess.run(cmd, text=True, capture_output=True)


def current_track():
    script = r'''
    tell application "Music"
        try
            set s to player state as text
        on error
            set s to "unknown"
        end try
        try
            set t to current track
            return s & "|" & (name of t) & "|" & (artist of t)
        on error
            return s & "|" & "" & "|" & ""
        end try
    end tell
    '''
    r = run(["osascript", "-e", script])
    parts = (r.stdout or "").strip().split("|", 2)
    while len(parts) < 3:
        parts.append("")
    return {"state": parts[0], "name": parts[1], "artist": parts[2]}


def search_catalog(query, limit=5):
    params = urllib.parse.urlencode({
        "term": query,
        "media": "music",
        "entity": "song",
        "limit": limit,
    })
    url = f"{ITUNES_SEARCH_URL}?{params}"
    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data.get("results", [])


def open_music_url(track_url):
    music_url = track_url.replace("https://", "music://")
    r = run(["open", music_url])
    return music_url, r


def send_keycode(code: int):
    return run(["osascript", "-e", 'tell application "Music" to activate', "-e", f'tell application "System Events" to key code {code}'])


def run_strategy(strategy: str) -> List[dict]:
    actions = []
    if strategy == "enter":
        r = send_keycode(36)
        actions.append({"action": "enter", "rc": r.returncode, "stdout": r.stdout, "stderr": r.stderr})
        time.sleep(1)
    elif strategy == "space":
        r = send_keycode(49)
        actions.append({"action": "space", "rc": r.returncode, "stdout": r.stdout, "stderr": r.stderr})
        time.sleep(1)
    elif strategy == "tab-enter":
        r1 = send_keycode(48)
        actions.append({"action": "tab", "rc": r1.returncode, "stdout": r1.stdout, "stderr": r1.stderr})
        time.sleep(0.3)
        r2 = send_keycode(36)
        actions.append({"action": "enter", "rc": r2.returncode, "stdout": r2.stdout, "stderr": r2.stderr})
        time.sleep(1)
    elif strategy == "double-enter":
        r1 = send_keycode(36)
        actions.append({"action": "enter-1", "rc": r1.returncode, "stdout": r1.stdout, "stderr": r1.stderr})
        time.sleep(0.3)
        r2 = send_keycode(36)
        actions.append({"action": "enter-2", "rc": r2.returncode, "stdout": r2.stdout, "stderr": r2.stderr})
        time.sleep(1)
    elif strategy == "tab-tab-enter":
        for name, code in [("tab-1", 48), ("tab-2", 48), ("enter", 36)]:
            r = send_keycode(code)
            actions.append({"action": name, "rc": r.returncode, "stdout": r.stdout, "stderr": r.stderr})
            time.sleep(0.3)
        time.sleep(1)
    elif strategy == "shift-tab-enter":
        r1 = run(["osascript", "-e", 'tell application "Music" to activate', "-e", 'tell application "System Events" to key code 48 using shift down'])
        actions.append({"action": "shift-tab", "rc": r1.returncode, "stdout": r1.stdout, "stderr": r1.stderr})
        time.sleep(0.3)
        r2 = send_keycode(36)
        actions.append({"action": "enter", "rc": r2.returncode, "stdout": r2.stdout, "stderr": r2.stderr})
        time.sleep(1)
    return actions


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--index", type=int, default=1, help="1-based result index")
    ap.add_argument("--press-enter", action="store_true")
    ap.add_argument("--press-space", action="store_true")
    ap.add_argument("--strategy", choices=["enter", "space", "tab-enter", "double-enter", "tab-tab-enter", "shift-tab-enter"])
    args = ap.parse_args()

    before = current_track()
    results = search_catalog(args.query, args.limit)
    if not results:
        json.dump({"ok": False, "error": "no_results", "query": args.query}, sys.stdout, indent=2)
        sys.stdout.write("\n")
        sys.exit(1)

    idx = max(1, min(args.index, len(results))) - 1
    chosen = results[idx]
    music_url, open_result = open_music_url(chosen["trackViewUrl"])
    time.sleep(2)

    actions = []
    if args.strategy:
        actions.extend(run_strategy(args.strategy))
    else:
        if args.press_enter:
            actions.extend(run_strategy("enter"))
        if args.press_space:
            actions.extend(run_strategy("space"))

    after = current_track()
    json.dump(
        {
            "ok": open_result.returncode == 0,
            "query": args.query,
            "chosen": {
                "trackName": chosen.get("trackName"),
                "artistName": chosen.get("artistName"),
                "collectionName": chosen.get("collectionName"),
                "trackViewUrl": chosen.get("trackViewUrl"),
                "musicUrl": music_url,
            },
            "open": {"rc": open_result.returncode, "stdout": open_result.stdout, "stderr": open_result.stderr},
            "actions": actions,
            "before": before,
            "after": after,
            "changed": (before["name"], before["artist"]) != (after["name"], after["artist"]),
        },
        sys.stdout,
        indent=2,
    )
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
