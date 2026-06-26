#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import time
import urllib.parse
import urllib.request

ITUNES_SEARCH_URL = "https://itunes.apple.com/search"


def run(cmd):
    return subprocess.run(cmd, text=True, capture_output=True)


def applescript(script: str):
    return run(["osascript", "-e", script])


def search_catalog(query, limit=5):
    params = urllib.parse.urlencode({
        "term": query,
        "media": "music",
        "entity": "song",
        "limit": limit,
    })
    with urllib.request.urlopen(f"{ITUNES_SEARCH_URL}?{params}", timeout=10) as r:
        return json.loads(r.read().decode("utf-8")).get("results", [])


def ensure_playlist(name: str):
    script = f'''
    tell application "Music"
      if not (exists playlist "{name}") then
        make new user playlist with properties {{name:"{name}"}}
      end if
    end tell
    '''
    r = applescript(script)
    return r.returncode == 0, (r.stderr or r.stdout).strip()


def add_track_to_playlist(playlist_name: str, song_name: str, artist_name: str):
    esc_song = song_name.replace('"', '\\"')
    esc_artist = artist_name.replace('"', '\\"')
    esc_playlist = playlist_name.replace('"', '\\"')
    script = f'''
    tell application "Music"
      set matchingTracks to (every track of library playlist 1 whose name is "{esc_song}" and artist is "{esc_artist}")
      if (count of matchingTracks) is 0 then
        return "NOT_FOUND"
      end if
      duplicate item 1 of matchingTracks to playlist "{esc_playlist}"
      return "OK"
    end tell
    '''
    r = applescript(script)
    out = (r.stdout or "").strip()
    err = (r.stderr or "").strip()
    return r.returncode == 0 and out == "OK", out or err


def add_catalog_song_to_library(track_view_url: str):
    music_url = track_view_url.replace("https://", "music://")
    open_res = run(["open", music_url])
    time.sleep(2)
    steps = [
        'tell application "Music" to activate',
        'tell application "System Events" to tell process "Music" to keystroke "l" using command down',
        'tell application "System Events" to key code 36',
    ]
    for s in steps:
        applescript(s)
        time.sleep(0.6)
    return open_res.returncode == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("playlist")
    ap.add_argument("queries", nargs="+")
    ap.add_argument("--limit", type=int, default=5)
    args = ap.parse_args()

    ok, msg = ensure_playlist(args.playlist)
    if not ok:
        print(json.dumps({"ok": False, "error": "playlist_create_failed", "details": msg}, indent=2))
        sys.exit(1)

    results = []
    for query in args.queries:
        entry = {"query": query}
        try:
            found = search_catalog(query, args.limit)
        except Exception as e:
            entry.update({"ok": False, "error": f"catalog_search_failed: {e}"})
            results.append(entry)
            continue
        if not found:
            entry.update({"ok": False, "error": "no_catalog_results"})
            results.append(entry)
            continue
        chosen = found[0]
        entry["chosen"] = {
            "trackName": chosen.get("trackName"),
            "artistName": chosen.get("artistName"),
            "collectionName": chosen.get("collectionName"),
            "trackViewUrl": chosen.get("trackViewUrl"),
        }
        added, detail = add_track_to_playlist(args.playlist, chosen.get("trackName", ""), chosen.get("artistName", ""))
        if added:
            entry.update({"ok": True, "method": "library-duplicate"})
            results.append(entry)
            continue
        add_catalog_song_to_library(chosen.get("trackViewUrl", ""))
        time.sleep(1.5)
        added2, detail2 = add_track_to_playlist(args.playlist, chosen.get("trackName", ""), chosen.get("artistName", ""))
        if added2:
            entry.update({"ok": True, "method": "catalog-add-then-duplicate"})
        else:
            entry.update({"ok": False, "error": "add_failed", "details": detail2 or detail})
        results.append(entry)

    print(json.dumps({"ok": True, "playlist": args.playlist, "results": results}, indent=2))


if __name__ == "__main__":
    main()
