#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import time


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
    out = (r.stdout or "").strip().split("|", 2)
    while len(out) < 3:
        out.append("")
    return {"state": out[0], "name": out[1], "artist": out[2]}


def play_library(song):
    return run(["clawtunes", "-1", "play", "song", song])


def open_catalog(song):
    return run(["clawtunes", "-1", "catalog", "search", song, "-n", "5"])


def music_play():
    return run(["osascript", "-e", 'tell application "Music" to play'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--song")
    ap.add_argument("--catalog", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    if args.status:
        json.dump({"ok": True, "track": current_track()}, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return

    if not args.song:
        print("--song is required unless --status is used", file=sys.stderr)
        sys.exit(2)

    before = current_track()

    if args.catalog:
        r = open_catalog(args.song)
        time.sleep(2)
        music_play()
        time.sleep(2)
        after = current_track()
        changed = (after["name"], after["artist"]) != (before["name"], before["artist"])
        json.dump(
            {
                "ok": r.returncode == 0,
                "mode": "catalog",
                "requested": args.song,
                "command_stdout": r.stdout,
                "command_stderr": r.stderr,
                "before": before,
                "after": after,
                "changed": changed,
                "autoplay_worked": changed and after["state"] == "playing",
            },
            sys.stdout,
            indent=2,
        )
        sys.stdout.write("\n")
        return

    r = play_library(args.song)
    time.sleep(2)
    after = current_track()
    changed = (after["name"], after["artist"]) != (before["name"], before["artist"])
    json.dump(
        {
            "ok": r.returncode == 0,
            "mode": "library",
            "requested": args.song,
            "command_stdout": r.stdout,
            "command_stderr": r.stderr,
            "before": before,
            "after": after,
            "changed": changed,
            "autoplay_worked": changed and after["state"] == "playing",
        },
        sys.stdout,
        indent=2,
    )
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
