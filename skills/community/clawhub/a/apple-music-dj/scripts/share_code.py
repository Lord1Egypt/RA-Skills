#!/usr/bin/env python3
"""
share_code.py — A taste code you can send a friend, and read one they sent you.

A code is a compact, ID-free summary of a taste profile: artist names, genre and decade weights and
a few scores (the same data as a taste snapshot). It holds no song IDs, ratings, library contents or
tokens. Blend with a friend's code instead of swapping profile files.

Usage:
  python3 share_code.py make [--profile PATH]      # print your code (and what is inside it)
  python3 share_code.py show <code> [--json]       # see exactly what a code from someone else contains
  python3 strategy_engine.py --strategy blend --profile mine.json --profile-b <code> --storefront us
  python3 compatibility.py profile mine.json <code>

A code from another person is untrusted input: it is size-capped, its shape is checked (anything
it holds beyond the known fields is ignored, and over-long lists are cut), and every string in it is
stripped of control characters and shortened before anything uses it.
This script makes no network calls and writes no files.
"""

import sys

if sys.version_info < (3, 11):
    sys.exit(
        f"ERROR: Python 3.11+ is required (you have "
        f"{sys.version_info.major}.{sys.version_info.minor}). Please upgrade."
    )

import argparse
import base64
import json
import math
import re
import unicodedata
import zlib

from _common import APP_DIR, load_profile, make_snapshot, search_artist

PREFIX = "amdj1:"
CODE_START = re.compile(r"amdj\d+:")  # any version of the prefix; a different version gets its own message
MAX_CODE_CHARS = 4000       # a real code is under ~1,000 characters
MAX_JSON_BYTES = 16 * 1024  # decompressed size cap (a zip-bomb guard)
MAX_ARTISTS, MAX_GENRES, MAX_ERAS = 10, 10, 8
MAX_TEXT = 80
ENERGY_VALUES = {"high-energy", "chill", "balanced"}
DEFAULT_PROFILE = APP_DIR / "taste_profile.json"


class ShareCodeError(ValueError):
    """The code is malformed, too large, from a newer version, or empty."""


# ── Encoding ─────────────────────────────────────────────────────

def encode(profile: dict) -> str:
    """The code for a profile. Built from the ID-free snapshot, so nothing personal can leak in."""
    snap = make_snapshot(profile)
    payload = {
        "v": 1,
        "a": [[a["name"], round(float(a["weight"]), 3)] for a in snap["top_artists"][:MAX_ARTISTS] if a["name"]],
        "g": [[g["genre"], round(float(g["weight"]), 3)] for g in snap["genre_distribution"][:MAX_GENRES] if g["genre"]],
        "e": [[e["decade"], round(float(e["weight"]), 3)] for e in snap["era_distribution"][:MAX_ERAS] if e["decade"]],
        "en": snap["energy_profile"],
        "va": round(float(snap["variety_score"]), 3),
        "ma": round(float(snap["mainstream_score"]), 3),
    }
    raw = zlib.compress(json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode(), 9)
    return PREFIX + base64.urlsafe_b64encode(raw).decode().rstrip("=")


# ── Decoding (untrusted input) ───────────────────────────────────

def _clean(text: str) -> str:
    """One line of printable text: no control or invisible-format characters, shortened."""
    kept = "".join(" " if ch.isspace() else ch for ch in text if not unicodedata.category(ch).startswith("C") or ch.isspace())
    return re.sub(r"\s+", " ", kept).strip()[:MAX_TEXT]


def _number(value, low: float, high: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ShareCodeError("The code has a value that is not a number.")
    return round(min(max(float(value), low), high), 3)


def _pairs(value, limit: int, what: str, keep=lambda name: True) -> list[tuple[str, float]]:
    if not isinstance(value, list):
        raise ShareCodeError(f"The code's {what} are not a list.")
    out = []
    for item in value[:limit]:
        if not (isinstance(item, list) and len(item) == 2 and isinstance(item[0], str)):
            raise ShareCodeError(f"The code has a malformed entry in its {what}.")
        name = _clean(item[0])
        if name and keep(name):
            out.append((name, _number(item[1], 0, 1_000_000)))
    return out


def decode(code: str) -> dict:
    """A profile-shaped dict from someone's code (artist names only, no IDs). Raises ShareCodeError."""
    code = (code or "").strip()
    if not CODE_START.match(code):
        raise ShareCodeError(f"That is not a taste code (it should start with '{PREFIX}').")
    if not code.startswith(PREFIX):
        raise ShareCodeError("That code comes from a different version of Apple Music DJ. Ask for a new one.")
    if len(code) > MAX_CODE_CHARS:
        raise ShareCodeError("That code is far too long to be a taste code.")
    body = code[len(PREFIX):]
    if not body or not re.fullmatch(r"[A-Za-z0-9_-]+", body):
        raise ShareCodeError("The code has characters a taste code cannot contain. Was it cut off or edited?")
    try:
        inflater = zlib.decompressobj()
        data = inflater.decompress(base64.urlsafe_b64decode(body + "=" * (-len(body) % 4)), MAX_JSON_BYTES + 1)
        if len(data) > MAX_JSON_BYTES or inflater.unconsumed_tail or not inflater.eof:
            raise ShareCodeError("The code is damaged or too large. Was it cut off?")
        if inflater.unused_data:  # bytes after a complete stream: not something `make` ever produces
            raise ShareCodeError("The code has extra data after its end. Was it edited?")
        obj = json.loads(data.decode("utf-8"))
    except ShareCodeError:
        raise
    except (ValueError, zlib.error):
        raise ShareCodeError("The code is damaged. Was it cut off or edited?") from None
    if not isinstance(obj, dict) or obj.get("v") != 1:
        raise ShareCodeError("That code comes from a different version of Apple Music DJ. Ask for a new one.")

    artists = _pairs(obj.get("a", []), MAX_ARTISTS, "artists")
    genres = _pairs(obj.get("g", []), MAX_GENRES, "genres")
    eras = _pairs(obj.get("e", []), MAX_ERAS, "decades", keep=lambda d: re.fullmatch(r"\d{4}s", d) is not None)
    if not artists and not genres:
        raise ShareCodeError("The code has no artists or genres in it.")
    energy = obj.get("en")
    return {
        "top_artists": [{"name": n, "play_weight": w} for n, w in artists],
        "genre_distribution": [{"genre": n, "weight": w} for n, w in genres],
        "era_distribution": [{"decade": n, "weight": w} for n, w in eras],
        "energy_profile": energy if energy in ENERGY_VALUES else "balanced",
        "variety_score": _number(obj.get("va", 0.5), 0, 1),
        "mainstream_score": _number(obj.get("ma", 0.5), 0, 1),
        "shared_code": True,
    }


def looks_like_code(value: str) -> bool:
    """A taste code, as opposed to a profile path (a file called amdj-friend.json is still a path)."""
    return CODE_START.match(value.strip()) is not None


def load_profile_arg(value: str) -> dict:
    """A profile from a path, or from a taste code. Exits with a plain message when a code is bad."""
    if not looks_like_code(value):
        return load_profile(value)
    try:
        return decode(value)
    except ShareCodeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


def resolve_artist_ids(profile: dict, sf: str, limit: int = 8, search=search_artist) -> int:
    """Look up catalog IDs for a code's artists (a code carries names only). Returns how many were found.

    An artist is only accepted when the catalog's top match has the same name, so a common name can't
    quietly turn into a different artist.
    """
    found = 0
    for artist in profile.get("top_artists", [])[:limit]:
        if artist.get("id"):
            continue
        match = search(sf, artist["name"])
        name = ((match or {}).get("attributes") or {}).get("name", "")
        if match and match.get("id") and _clean(name).casefold() == artist["name"].casefold():
            artist["id"] = match["id"]
            found += 1
    return found


# ── Display ──────────────────────────────────────────────────────

def describe(profile: dict) -> str:
    def shares(items: list[dict], key: str) -> str:
        total = sum(i["weight"] for i in items) or 1
        return ", ".join(f"{i[key]} {round(100 * i['weight'] / total)}%" for i in items)

    lines = ["Top artists: " + (", ".join(a["name"] for a in profile["top_artists"]) or "none"),
             "Genres: " + (shares(profile["genre_distribution"], "genre") or "none"),
             "Decades: " + (shares(profile["era_distribution"], "decade") or "none"),
             f"Energy: {profile['energy_profile']} · variety {round(100 * profile['variety_score'])}% · "
             f"mainstream {round(100 * profile['mainstream_score'])}%"]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Make or read a taste code.")
    sub = parser.add_subparsers(dest="mode", required=True)
    p_make = sub.add_parser("make", help="Print your taste code")
    p_make.add_argument("--profile", default=str(DEFAULT_PROFILE), help="Taste profile JSON (default: your cached profile)")
    p_show = sub.add_parser("show", help="Show what is inside a taste code")
    p_show.add_argument("code")
    p_show.add_argument("--json", action="store_true", help="Print the decoded profile as JSON")
    args = parser.parse_args(argv)

    if args.mode == "make":
        profile = load_profile(args.profile)
        code = encode(profile)
        print("This code holds only what is below: no song IDs, ratings, library or tokens.", file=sys.stderr)
        print(describe(decode(code)), file=sys.stderr)
        print(code)
        return 0
    try:
        profile = decode(args.code)
    except ShareCodeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print(json.dumps(profile, indent=2, ensure_ascii=False) if args.json else describe(profile))
    return 0


if __name__ == "__main__":
    sys.exit(main())
