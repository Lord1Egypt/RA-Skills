#!/usr/bin/env python3
"""
Spotify API Artist Lookup — Post Feb 2026 Development Mode
Collects all available data for an artist within API limitations.

Usage:
    python spotify_api_lookup.py "Artist Name"
    python spotify_api_lookup.py --id SPOTIFY_ID
    python spotify_api_lookup.py "Artist Name" --json

Output:
    Artist metadata, discography, related artists (no followers/popularity)
"""
import argparse
import json
import sys
import os

# Add parent dir to path for spotify_auth import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../../spotify-songs-to-notion")

import spotipy
from dotenv import load_dotenv

load_dotenv(os.path.dirname(os.path.abspath(__file__)) + "/../../spotify-songs-to-notion/.env")


def get_client():
    """Get Spotify client (user auth)."""
    from spotify_auth import get_spotify_client
    return get_spotify_client()


def search_artist(sp: spotipy.Spotify, name: str) -> dict | None:
    """Search for artist by name, return first result."""
    results = sp.search(q=name, type="artist", limit=1)
    items = results.get("artists", {}).get("items", [])
    return items[0] if items else None


def get_artist_data(sp: spotipy.Spotify, artist_id: str) -> dict:
    """Collect all available data for an artist."""
    data = {}

    # Basic artist info (limited in Dev Mode)
    data["artist"] = sp.artist(artist_id)

    # Albums
    try:
        albums = sp.artist_albums(artist_id, album_type="album,single", limit=50, country="PL")
        data["albums"] = albums["items"]
    except Exception as e:
        data["albums_error"] = str(e)

    # Related artists (still works!)
    try:
        related = sp.artist_related_artists(artist_id)
        data["related_artists"] = [
            {
                "name": r["name"],
                "id": r["id"],
                "genres": r.get("genres", []),
                "images": r.get("images", []),
                "spotify_url": r.get("external_urls", {}).get("spotify", ""),
            }
            for r in related.get("artists", [])[:10]
        ]
    except Exception as e:
        data["related_error"] = str(e)

    # Search for tracks (since top-tracks endpoint is removed)
    artist_name = data["artist"].get("name", "")
    try:
        track_search = sp.search(q=f'artist:"{artist_name}"', type="track", limit=10)
        data["search_tracks"] = track_search.get("tracks", {}).get("items", [])
    except Exception as e:
        data["search_error"] = str(e)

    return data


def format_output(data: dict, as_json: bool = False) -> str:
    """Format artist data for display."""
    if as_json:
        return json.dumps(data, ensure_ascii=False, indent=2, default=str)

    lines = []
    artist = data.get("artist", {})

    lines.append("=" * 60)
    lines.append(f"ARTIST: {artist.get('name', 'N/A')}")
    lines.append("=" * 60)
    lines.append(f"ID: {artist.get('id', 'N/A')}")
    lines.append(f"Spotify URL: {artist.get('external_urls', {}).get('spotify', 'N/A')}")
    lines.append(f"Type: {artist.get('type', 'N/A')}")
    lines.append(f"Images: {len(artist.get('images', []))} available")

    # Check for missing fields (Dev Mode)
    missing = []
    for key in ["followers", "popularity", "genres"]:
        if key not in artist or not artist.get(key):
            missing.append(key)
    if missing:
        lines.append(f"[!] MISSING (Dev Mode): {', '.join(missing)}")

    # Albums
    albums = data.get("albums", [])
    lines.append(f"\n--- DISCOGRAPHY ({len(albums)} releases) ---")
    seen = set()
    for a in albums:
        name = a.get("name", "N/A")
        if name in seen:
            continue
        seen.add(name)
        a_type = a.get("album_type", "unknown").upper()
        date = a.get("release_date", "N/A")
        tracks = a.get("total_tracks", "?")
        url = a.get("external_urls", {}).get("spotify", "")
        lines.append(f"  [{a_type}] {name} ({date}) — {tracks} tracks")
        if url:
            lines.append(f"    {url}")

    # Related artists
    related = data.get("related_artists", [])
    if related:
        lines.append(f"\n--- RELATED ARTISTS ({len(related)}) ---")
        for r in related:
            lines.append(f"  {r['name']} — {', '.join(r['genres'][:3]) or 'no genres'}")

    # Search tracks
    tracks = data.get("search_tracks", [])
    if tracks:
        lines.append(f"\n--- TOP TRACKS (from search) ---")
        for i, t in enumerate(tracks[:10], 1):
            t_artists = ", ".join(a["name"] for a in t.get("artists", []))
            album = t.get("album", {}).get("name", "N/A")
            lines.append(f"  {i}. {t['name']} — {t_artists}")
            lines.append(f"     Album: {album} | Pop: {t.get('popularity', 'N/A')}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Spotify Artist Lookup (Feb 2026 Dev Mode compatible)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("name", nargs="?", help="Artist name to search")
    group.add_argument("--id", help="Spotify artist ID")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    print("Connecting to Spotify...", file=sys.stderr)
    sp = get_client()

    if args.id:
        artist_id = args.id
    else:
        print(f"Searching for: {args.name}", file=sys.stderr)
        result = search_artist(sp, args.name)
        if not result:
            print(f"Artist not found: {args.name}", file=sys.stderr)
            sys.exit(1)
        artist_id = result["id"]
        print(f"Found: {result['name']} (ID: {artist_id})", file=sys.stderr)

    print("Collecting data...", file=sys.stderr)
    data = get_artist_data(sp, artist_id)

    output = format_output(data, as_json=args.json)
    print(output)

    # Also save JSON if requested
    if args.json:
        filename = f"artist_{artist_id}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        print(f"\nJSON saved to: {filename}", file=sys.stderr)


if __name__ == "__main__":
    main()
