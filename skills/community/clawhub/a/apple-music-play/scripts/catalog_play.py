#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import time
import urllib.parse
import urllib.request

ITUNES_SEARCH_URL = "https://itunes.apple.com/search"
STRATEGIES = ["tab-tab-enter", "tab-enter", "shift-tab-enter"]


def run(cmd):
    return subprocess.run(cmd, text=True, capture_output=True)


def current_track():
    r = run(["clawtunes", "status"])
    text = (r.stdout or r.stderr).strip().splitlines()
    if not text:
        return {"raw": "", "name": "", "artist": ""}
    name = ""
    artist = ""
    first = text[0].strip()
    if first.startswith(("▶", "⏸", "⏹")):
        name = first[1:].strip()
    for line in text:
        line = line.strip()
        if line.startswith("Artist:"):
            artist = line.split(":", 1)[1].strip()
    return {"raw": "\n".join(text), "name": name, "artist": artist}


def search_catalog(query, limit=5):
    params = urllib.parse.urlencode({
        "term": query,
        "media": "music",
        "entity": "song",
        "limit": limit,
    })
    with urllib.request.urlopen(f"{ITUNES_SEARCH_URL}?{params}", timeout=10) as r:
        return json.loads(r.read().decode("utf-8")).get("results", [])


def send_keycode(code: int, shift: bool = False):
    if shift:
        return run(["osascript", "-e", 'tell application "Music" to activate', "-e", f'tell application "System Events" to key code {code} using shift down'])
    return run(["osascript", "-e", 'tell application "Music" to activate', "-e", f'tell application "System Events" to key code {code}'])


def apply_strategy(name: str):
    actions = []
    if name == "tab-tab-enter":
        for label, code in [("tab-1", 48), ("tab-2", 48), ("enter", 36)]:
            r = send_keycode(code)
            actions.append({"action": label, "rc": r.returncode, "stderr": r.stderr})
            time.sleep(0.3)
    elif name == "tab-enter":
        for label, code in [("tab", 48), ("enter", 36)]:
            r = send_keycode(code)
            actions.append({"action": label, "rc": r.returncode, "stderr": r.stderr})
            time.sleep(0.3)
    elif name == "shift-tab-enter":
        r1 = send_keycode(48, shift=True)
        actions.append({"action": "shift-tab", "rc": r1.returncode, "stderr": r1.stderr})
        time.sleep(0.3)
        r2 = send_keycode(36)
        actions.append({"action": "enter", "rc": r2.returncode, "stderr": r2.stderr})
    time.sleep(1)
    return actions


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--index", type=int, default=1)
    args = ap.parse_args()

    before = current_track()
    results = search_catalog(args.query, args.limit)
    if not results:
        json.dump({"ok": False, "error": "no_results", "query": args.query}, sys.stdout, indent=2)
        sys.stdout.write("\n")
        sys.exit(1)

    idx = max(1, min(args.index, len(results))) - 1
    chosen = results[idx]
    music_url = chosen["trackViewUrl"].replace("https://", "music://")
    open_result = run(["open", music_url])
    time.sleep(2)

    attempts = []
    final_after = before
    worked = False
    for strategy in STRATEGIES:
        actions = apply_strategy(strategy)
        after = current_track()
        changed = (after["name"], after["artist"]) != (before["name"], before["artist"])
        matched = chosen.get("trackName", "").lower() in after["name"].lower() if after["name"] else False
        attempt = {
            "strategy": strategy,
            "actions": actions,
            "after": after,
            "changed": changed,
            "matched": matched,
        }
        attempts.append(attempt)
        final_after = after
        if changed and matched:
            worked = True
            break

    json.dump(
        {
            "ok": open_result.returncode == 0,
            "worked": worked,
            "query": args.query,
            "chosen": {
                "trackName": chosen.get("trackName"),
                "artistName": chosen.get("artistName"),
                "collectionName": chosen.get("collectionName"),
                "trackViewUrl": chosen.get("trackViewUrl"),
                "musicUrl": music_url,
            },
            "before": before,
            "after": final_after,
            "attempts": attempts,
        },
        sys.stdout,
        indent=2,
    )
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
