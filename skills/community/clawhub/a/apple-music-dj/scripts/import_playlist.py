#!/usr/bin/env python3
"""
import_playlist.py — Rebuild a playlist from another service in Apple Music.

Input is either
  - a CSV (e.g. a Spotify export from Exportify) with title + artist columns and/or
    an ISRC column, or
  - a text file with one "Artist - Title" per line (blank lines and # comments ignored).

Matching: ISRC first (exact, batched), then a strict title + artist search.
Anything that doesn't clearly match is reported as unmatched rather than guessed.

Usage:
  python3 import_playlist.py <file> [--storefront us]                 # preview only
  python3 import_playlist.py <file> --create --name "My Playlist"     # create it (writes to your library)

Requires: APPLE_MUSIC_DEV_TOKEN and APPLE_MUSIC_USER_TOKEN env vars.
"""

import sys

if sys.version_info < (3, 10):
    sys.exit(
        f"ERROR: Python 3.10+ is required (you have "
        f"{sys.version_info.major}.{sys.version_info.minor}). Please upgrade."
    )

import argparse
import csv
import difflib
import io
import json
import re
from pathlib import Path

from _common import call_api, get_storefront, load_config, require_env_tokens

ISRC_RE = re.compile(r"^[A-Z]{2}[A-Z0-9]{3}[0-9]{7}$")
ISRC_BATCH = 25  # the API (and apple_music_api.sh) accept at most 25 per call
MAX_ROWS = 500
TITLE_MATCH_THRESHOLD = 0.85

TITLE_COLUMNS = ("track name", "track", "title", "song", "name")
ARTIST_COLUMNS = ("artist name(s)", "artist names", "artist name", "artists", "artist")
ISRC_COLUMNS = ("isrc", "track isrc")


# ── Parsing ──────────────────────────────────────────────────────

def _clean_isrc(value: str | None) -> str | None:
    isrc = (value or "").replace("-", "").strip().upper()
    return isrc if ISRC_RE.match(isrc) else None


def _first_artist(value: str) -> str:
    return re.split(r"[;]", value)[0].strip()


def _column(header: list[str], names: tuple[str, ...]) -> str | None:
    lowered = {h.strip().lower(): h for h in header}
    return next((lowered[n] for n in names if n in lowered), None)


def parse_csv(text: str) -> list[dict]:
    reader = csv.DictReader(io.StringIO(text, newline=""))
    header = reader.fieldnames or []
    title_col, artist_col, isrc_col = (_column(header, c) for c in (TITLE_COLUMNS, ARTIST_COLUMNS, ISRC_COLUMNS))
    if not isrc_col and not (title_col and artist_col):
        raise ValueError("CSV needs an ISRC column, or both title and artist columns "
                         f"(found: {', '.join(header) or 'no header'}).")
    rows = []
    for rec in reader:
        row = {
            "title": (rec.get(title_col) or "").strip() if title_col else "",
            "artist": _first_artist(rec.get(artist_col) or "") if artist_col else "",
            "isrc": _clean_isrc(rec.get(isrc_col)) if isrc_col else None,
        }
        if row["isrc"] or (row["title"] and row["artist"]):
            rows.append(row)
    return rows


def parse_text(text: str) -> list[dict]:
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.split(r"\s+[-–—]\s+", line, maxsplit=1)
        if len(m) == 2 and m[0] and m[1]:
            rows.append({"artist": m[0].strip(), "title": m[1].strip(), "isrc": None})
    return rows


def parse_file(path: str) -> list[dict]:
    text = Path(path).read_text(encoding="utf-8-sig")
    if Path(path).suffix.lower() == ".csv":
        return parse_csv(text)
    return parse_text(text)


# ── Matching ─────────────────────────────────────────────────────

def normalize_title(title: str) -> str:
    t = title.lower()
    t = re.sub(r"[\(\[].*?[\)\]]", " ", t)                       # (Remastered 2009), [Live]
    t = re.sub(r"\s[-–—]\s.*(remaster|version|mix|edit|live|mono|stereo).*$", " ", t)
    t = re.sub(r"\b(feat|ft)\.?\s.*$", " ", t)
    t = re.sub(r"[^\w\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def normalize_artist(artist: str) -> str:
    a = re.sub(r"[^\w\s]", " ", artist.lower())
    a = re.sub(r"^the\s+", "", a.strip())
    return re.sub(r"\s+", " ", a).strip()


_CREDIT_SPLIT = re.compile(r"\s*(?:,|;|/|&|\band\b|\bfeat\.?|\bft\.?|\bfeaturing\b|\bwith\b|\bx\b)\s*", re.IGNORECASE)


def artist_credited(want: str, credit: str) -> bool:
    """True if `want` is the whole credit or one of its collaborators.

    "Muse" must not match "Museum", and "Queen" must not match "Queens of the Stone Age"
    or "Queen Latifah"; "Queen & David Bowie" does match "Queen".
    """
    wanted = normalize_artist(want)
    if not wanted:
        return False
    if normalize_artist(credit) == wanted:
        return True
    return any(normalize_artist(part) == wanted for part in _CREDIT_SPLIT.split(credit))


def _as_match(song: dict) -> dict:
    attrs = song.get("attributes", {})
    return {"id": song.get("id", ""), "name": attrs.get("name", ""), "artist": attrs.get("artistName", "")}


def best_search_match(row: dict, songs: list[dict]) -> dict | None:
    """Strict choice among search results: artist must match and the title must be close."""
    want_title = normalize_title(row["title"])
    best, best_score = None, 0.0
    for song in songs:
        attrs = song.get("attributes", {})
        if not artist_credited(row["artist"], attrs.get("artistName", "")):
            continue
        score = difflib.SequenceMatcher(None, want_title, normalize_title(attrs.get("name", ""))).ratio()
        if score > best_score:
            best, best_score = song, score
    return _as_match(best) if best and best_score >= TITLE_MATCH_THRESHOLD else None


def match_by_isrc(rows: list[dict], sf: str) -> dict[str, dict]:
    """{isrc: match} for every ISRC the catalog knows (batched)."""
    isrcs = list(dict.fromkeys(r["isrc"] for r in rows if r["isrc"]))
    found: dict[str, dict] = {}
    for i in range(0, len(isrcs), ISRC_BATCH):
        resp = call_api("songs-by-isrc", sf, ",".join(isrcs[i:i + ISRC_BATCH]))
        for song in (resp or {}).get("data", []):
            isrc = song.get("attributes", {}).get("isrc")
            if isrc and isrc not in found:
                found[isrc] = _as_match(song)
    return found


def match_rows(rows: list[dict], sf: str) -> list[dict]:
    """One result per input row: {"input", "match" (or None), "how": exact|fuzzy|unmatched}."""
    by_isrc = match_by_isrc(rows, sf)
    results = []
    for row in rows:
        match = by_isrc.get(row["isrc"]) if row["isrc"] else None
        how = "exact" if match else "unmatched"
        if not match and row["title"] and row["artist"]:
            resp = call_api("search", sf, f"{row['title']} {row['artist']}", "songs")
            songs = (resp or {}).get("results", {}).get("songs", {}).get("data", [])
            match = best_search_match(row, songs)
            how = "fuzzy" if match else "unmatched"
        results.append({"input": row, "match": match, "how": how})
    return results


def build_report(results: list[dict]) -> dict:
    """Counts, ordered unique tracks, and the unmatched rows."""
    tracks, seen, duplicates = [], set(), 0
    for r in results:
        if r["match"]:
            if r["match"]["id"] in seen:
                duplicates += 1
                continue
            seen.add(r["match"]["id"])
            tracks.append(r["match"])
    return {
        "counts": {
            "total": len(results),
            "exact": sum(r["how"] == "exact" for r in results),
            "fuzzy": sum(r["how"] == "fuzzy" for r in results),
            "unmatched": sum(r["how"] == "unmatched" for r in results),
            "duplicates": duplicates,
        },
        "tracks": tracks,
        "fuzzy": [r for r in results if r["how"] == "fuzzy"],
        "unmatched": [r["input"] for r in results if r["how"] == "unmatched"],
    }


# ── Main ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Import a playlist from CSV / text into Apple Music")
    parser.add_argument("file", help="CSV (ISRC or title+artist columns) or text file ('Artist - Title' per line)")
    parser.add_argument("--storefront", default=None, help="Storefront code (default: auto)")
    parser.add_argument("--create", action="store_true", help="Create the playlist (writes to your library)")
    parser.add_argument("--name", default=None, help="Playlist name (required with --create)")
    args = parser.parse_args()

    if args.create and not args.name:
        parser.error("--create needs --name")

    try:
        rows = parse_file(args.file)
    except (OSError, UnicodeDecodeError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    if not rows:
        print("ERROR: No usable rows found in the file.", file=sys.stderr)
        sys.exit(1)
    if len(rows) > MAX_ROWS:
        print(f"⚠️  {len(rows)} rows found — only the first {MAX_ROWS} will be imported.", file=sys.stderr)
        rows = rows[:MAX_ROWS]

    require_env_tokens()
    sf = get_storefront(args.storefront or load_config().get("default_storefront"))
    print(f"🔎 Matching {len(rows)} tracks in the {sf} catalog...", file=sys.stderr)
    report = build_report(match_rows(rows, sf))
    c = report["counts"]
    print(f"✅ {c['exact']} exact, {c['fuzzy']} fuzzy, {c['unmatched']} unmatched"
          + (f", {c['duplicates']} duplicates dropped" if c["duplicates"] else "") + ".", file=sys.stderr)

    if args.create:
        if not report["tracks"]:
            print("ERROR: Nothing matched, so no playlist was created.", file=sys.stderr)
            print(json.dumps(report, indent=2))
            sys.exit(1)
        # Imported lazily: strategy_engine pulls in the whole strategy stack
        from playlist_history import log_playlist
        from strategy_engine import create_playlist_from_tracks

        if not create_playlist_from_tracks(report["tracks"], args.name, "Imported with Apple Music DJ."):
            print("❌ Failed to create playlist.", file=sys.stderr)
            sys.exit(1)
        report["created"] = args.name
        try:
            log_playlist(args.name, "import", [t["id"] for t in report["tracks"]])
        except Exception as e:
            print(f"⚠️  Could not log to history: {e}", file=sys.stderr)
        print(f"✅ Playlist '{args.name}' created with {len(report['tracks'])} tracks.", file=sys.stderr)
    else:
        print("Preview only — add --create --name \"...\" to build the playlist.", file=sys.stderr)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
