"""Strategy: remix (an Apple Music playlist, made to fit your taste)."""

import random
import re
import sys
from urllib.parse import urlparse

from _common import call_api, passes_user_filters, search_artist, swap_explicit_for_clean, taste_affinity
from strategies.candidates import USER_FILTERS, _artist_top_songs, _clean_genres, _finish, _similar_artists, _song_candidate
from strategies.scoring import (
    OWN_ARTIST_BOOST,
    REMIX_KEEP_BASE,
    REMIX_KEEP_MIN,
    REMIX_MAX_LOOKUPS,
    REMIX_SWAP_BASE,
)

# What the last run did, for the CLI to report ("you'd keep 14 of 50"). Cleared at the start of each run.
LAST_REMIX: dict = {}

MAX_PLAYLIST_PAGES = 10  # up to 1,000 tracks

_CATALOG_PLAYLIST_ID = re.compile(r"^pl\.[A-Za-z0-9_-]+$")
_STOREFRONT = re.compile(r"^[a-z]{2}$")


def parse_playlist_ref(value: str) -> tuple[str | None, str]:
    """Accept a music.apple.com playlist URL or a bare `pl.…` ID; return (storefront or None, id)."""
    value = value.strip()
    if _CATALOG_PLAYLIST_ID.match(value):
        return None, value
    parsed = urlparse(value)
    if parsed.scheme in ("http", "https") and parsed.hostname == "music.apple.com":
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) >= 2 and parts[1] == "playlist" and _CATALOG_PLAYLIST_ID.match(parts[-1]):
            return (parts[0] if _STOREFRONT.match(parts[0]) else None), parts[-1]
    raise ValueError("expected an Apple Music playlist link (music.apple.com/<storefront>/playlist/<name>/pl.…) "
                     f"or a playlist ID starting with pl., got {value!r}")


def _fetch_playlist(sf: str, playlist_id: str) -> tuple[str, list[dict]]:
    data = (call_api("catalog-playlist", sf, playlist_id) or {}).get("data") or []
    if not data:
        return "", []
    playlist = data[0]
    page = playlist.get("relationships", {}).get("tracks", {})
    tracks = list(page.get("data", []))
    pages = 1
    while page.get("next") and pages < MAX_PLAYLIST_PAGES:  # long playlists come in pages of up to 100
        page = call_api("catalog-playlist-tracks", sf, playlist_id, str(len(tracks))) or {}
        if not page.get("data"):
            break
        tracks += page["data"]
        pages += 1
    return playlist.get("attributes", {}).get("name", ""), [t for t in tracks if t.get("type", "songs") == "songs"]


def strategy_remix(profile: dict, sf: str, playlist: str, target_size: int = 30,
                   include_library: bool = False, rng: random.Random | None = None) -> list[dict]:
    """Keep the tracks of an Apple Music playlist you'd like; swap the rest for taste-matched picks."""
    LAST_REMIX.clear()
    try:
        playlist_sf, playlist_id = parse_playlist_ref(playlist)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return []

    print(f"  Fetching playlist {playlist_id}...", file=sys.stderr)
    name, originals = _fetch_playlist(playlist_sf or sf, playlist_id)
    if not originals:
        print(f"ERROR: Couldn't load tracks for playlist '{playlist_id}'. Check the link and storefront.",
              file=sys.stderr)
        return []
    LAST_REMIX.update(name=name, original=len(originals))

    user_genres = profile.get("genre_distribution", [])
    loved_artists = {a["name"].lower() for a in profile.get("top_artists", [])}
    loved_artists |= {n.lower() for n in profile.get("recently_added_artists", [])}
    library_ids = set() if include_library else set(profile.get("library_song_ids", []))
    disliked = set(profile.get("disliked_song_ids", []))
    in_playlist = {t.get("id", "") for t in originals}

    def fit(genres: list[str], artist_name: str) -> float:
        score = taste_affinity(genres, user_genres)
        return score + OWN_ARTIST_BOOST if artist_name.lower() in loved_artists else score

    def eligible(song: dict, source: str, reason: str, fallback_artist: str = "") -> dict | None:
        """The song as a candidate (its clean version in clean mode), or None if your filters rule it out:
        an excluded artist, a recently used track, an explicit song with no clean version."""
        c = swap_explicit_for_clean(_song_candidate(song, source, reason, 0.0, fallback_artist), USER_FILTERS)
        return c if passes_user_filters(c, USER_FILTERS) else None

    candidates: list[dict] = []
    dropped: list[dict] = []
    kept_artists: list[str] = []
    for song in originals:
        tid = song.get("id", "")
        if not tid or tid in library_ids:
            continue
        attrs = song.get("attributes", {})
        genres = _clean_genres(attrs)
        fits = fit(genres, attrs.get("artistName", ""))
        c = eligible(song, "remix_keep", "Kept from the original: it fits your taste.")
        if tid in disliked or fits < REMIX_KEEP_MIN or c is None:
            dropped.append(song)  # not for you, so it is swapped
            continue
        c["_score"] = REMIX_KEEP_BASE + fits
        candidates.append(c)
        if c["artist"] not in kept_artists:
            kept_artists.append(c["artist"])

    # Swap each dropped track for the same artist's best other song, else a similar artist's close match,
    # else more from an artist whose tracks you are keeping (the next one in turn, so no one is overused)
    used = set(in_playlist)
    artists_cache: dict[str, dict | None] = {}
    for turn, song in enumerate(dropped[:REMIX_MAX_LOOKUPS]):
        attrs = song.get("attributes", {})
        artist_name = attrs.get("artistName", "")
        title = attrs.get("name", "")
        if artist_name not in artists_cache:
            artists_cache[artist_name] = search_artist(sf, artist_name) if artist_name else None
        artist = artists_cache[artist_name]

        def usable(top: dict) -> bool:
            tid = top.get("id", "")
            return (bool(tid) and tid not in used and tid not in disliked and tid not in library_ids
                    and eligible(top, "remix_swap", "") is not None)

        pick: dict | None = None
        reason = ""
        own = [t for t in _artist_top_songs(sf, artist["id"]) if usable(t)] if artist and artist.get("id") else []
        own = [t for t in own if fit(_clean_genres(t.get("attributes", {})), artist_name) >= REMIX_KEEP_MIN]
        if own:
            pick, reason = own[0], f"Swapped '{title}' for another {artist_name} song that fits you better."
        elif artist and artist.get("id"):
            for sim in _similar_artists(sf, artist["id"])[:4]:
                sim_name = sim.get("attributes", {}).get("name", "")
                for top in _artist_top_songs(sf, sim.get("id", ""))[:3]:
                    top_genres = _clean_genres(top.get("attributes", {}))
                    if usable(top) and fit(top_genres, sim_name) >= REMIX_KEEP_MIN:
                        pick, reason = top, f"Swapped '{title}' for {sim_name}, a neighbour of {artist_name} that suits you."
                        break
                if pick:
                    break
        if not pick:
            for offset in range(len(kept_artists)):
                fan_name = kept_artists[(turn + offset) % len(kept_artists)]
                if fan_name not in artists_cache:
                    artists_cache[fan_name] = search_artist(sf, fan_name)
                fan = artists_cache[fan_name]
                more = [t for t in _artist_top_songs(sf, fan["id"]) if usable(t)] if fan and fan.get("id") else []
                if more:
                    pick, reason = more[0], f"Swapped '{title}' for more {fan_name}, whom you'd keep from this playlist."
                    break
        swap = eligible(pick, "remix_swap", reason, pick.get("attributes", {}).get("artistName", "")) if pick else None
        if swap:
            used.add(swap["id"])
            swap["_score"] = REMIX_SWAP_BASE + fit(swap["genre"], swap["artist"])
            candidates.append(swap)

    result = _finish(candidates, target_size, rng=rng)
    kept = sum(1 for t in result if t.get("source") == "remix_keep")
    LAST_REMIX.update(kept=kept, swapped=len(result) - kept)
    return result
