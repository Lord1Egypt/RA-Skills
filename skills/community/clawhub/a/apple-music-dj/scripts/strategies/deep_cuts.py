"""Strategy: deep cuts (hidden gems from artists you love)."""

import random
import re
import sys

from _common import call_api, filter_generic_genres, get_album_tracks, passes_user_filters, swap_explicit_for_clean
from collections import Counter
from strategies.candidates import USER_FILTERS, _artist_top_songs, _finish
from strategies.scoring import ARTIST_CAP, DEEP_CUT_BASE, DEEP_CUT_POSITION_BONUS, _artist_boost
from strategies.sequencing import ALBUM_CAP


# ── Strategy: Deep Cuts ──────────────────────────────────────────

# Alternate takes of a song: a version tag in brackets or after " - ", e.g. "Song (Live)",
# "Song - Demo". A bare title word ("Live Forever") doesn't count.
_ALT_VERSION = re.compile(
    r"(?:[(\[]| - )[^)\]]*\b(?:live|remix(?:ed)?|demo|instrumental|acoustic|karaoke|commentary"
    r"|a ?cappella|radio edit|rehearsal|session)\b",
    re.IGNORECASE,
)


# Albums that only repeat material: live recordings and hits collections
_REPEAT_ALBUM = re.compile(r"\blive (?:at|from|in|on)\b|[(\[]live\b|\bgreatest hits\b|\bbest of\b",
                           re.IGNORECASE)


DEEP_CUT_ALBUMS_PER_ARTIST = 4


def _is_alt_version(name: str) -> bool:
    return bool(_ALT_VERSION.search(name))


def _title_key(name: str) -> str:
    """Song title without bracketed or " - " suffixes, for spotting one song on several releases."""
    base = re.split(r"\s[(\[]|\s-\s", name, maxsplit=1)[0]
    return re.sub(r"[\W_]", "", base.casefold())  # \W is Unicode-aware: 春 and 夏 stay distinct


def strategy_deep_cuts(profile: dict, sf: str, target_size: int = 30,
                       rng: random.Random | None = None) -> list[dict]:
    """Hidden gems from artists the user already loves."""
    top_artists = profile.get("top_artists", [])[:15]
    library_ids = set(profile.get("library_song_ids", []))
    disliked = set(profile.get("disliked_song_ids", []))
    rng = rng or random.Random()
    cap = ARTIST_CAP
    candidates = []
    seen_titles: set[tuple[str, str]] = set()
    per_album: Counter = Counter()  # eligible candidates per (artist, album)

    for i, artist in enumerate(top_artists):
        artist_id = artist.get("id")
        artist_name = artist.get("name", "")
        if not artist_id:
            continue
        print(f"  [{i+1}/{len(top_artists)}] Scanning {artist_name}...", file=sys.stderr)

        # Get top songs to identify hits to exclude
        top_song_keys = {_title_key(ts.get("attributes", {}).get("name", ""))
                         for ts in _artist_top_songs(sf, artist_id)}
        top_song_keys.discard("")

        # Fetch discography: full albums only, a random few per artist so the scan stays cheap
        albums_data = call_api("artist-albums", sf, artist_id)
        if not albums_data or "data" not in albums_data:
            continue
        albums = [a for a in albums_data["data"]
                  if not a.get("attributes", {}).get("isSingle", False)
                  and not a.get("attributes", {}).get("isCompilation", False)
                  and not _REPEAT_ALBUM.search(a.get("attributes", {}).get("name", ""))]
        rng.shuffle(albums)

        # Artists you play more get a head start, as in the era strategy
        artist_weight = _artist_boost(artist)
        for album in albums[:DEEP_CUT_ALBUMS_PER_ARTIST]:
            album_attrs = album.get("attributes", {})
            album_tracks = get_album_tracks(sf, album["id"])
            last_position = max(len(album_tracks) - 1, 1)
            for position, track in enumerate(album_tracks):
                tid = track.get("id", "")
                attrs = track.get("attributes", {})
                name = attrs.get("name", "")
                key = (attrs.get("artistName", artist_name).lower(), _title_key(name))

                # Exclude: in library, disliked, top songs, alternate takes, repeats from another release
                if tid in library_ids or tid in disliked:
                    continue
                if key[1] in top_song_keys or _is_alt_version(name) or key in seen_titles:
                    continue
                seen_titles.add(key)

                track_num = attrs.get("trackNumber", position + 1)
                candidate = {
                    "id": tid,
                    "name": name,
                    "artist": attrs.get("artistName", artist_name),
                    "album": album_attrs.get("name", ""),
                    "genre": filter_generic_genres(attrs.get("genreNames", [])),
                    "duration_ms": attrs.get("durationInMillis"),
                    "explicit": attrs.get("contentRating") == "explicit",
                    "source": "deep_cut",
                    "reason": f"A deep cut from {artist_name} — album track you haven't heard.",
                    # later tracks score slightly higher
                    "_score": DEEP_CUT_BASE + artist_weight
                              + DEEP_CUT_POSITION_BONUS * min(max(track_num - 1, 0) / last_position, 1.0),
                }
                candidate = swap_explicit_for_clean(candidate, USER_FILTERS)
                if not passes_user_filters(candidate, USER_FILTERS):
                    continue
                candidates.append(candidate)
                per_album[(candidate["artist"], candidate["album"])] += 1

        # Enough candidates, and enough of them under the album (2) and artist caps to fill the list
        usable_per_artist: Counter = Counter()
        for (artist_key, _album), n in per_album.items():
            usable_per_artist[artist_key] += min(n, ALBUM_CAP)
        capacity = sum(min(n, cap) for n in usable_per_artist.values())
        if len(candidates) >= target_size * 3 and capacity >= target_size:
            break

    return _finish(candidates, target_size, cap=cap, rng=rng)
