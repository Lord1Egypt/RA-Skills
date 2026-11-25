"""Strategy: trend radar (what's charting, filtered through your taste)."""

import random
import sys

from _common import apply_user_filters, call_api, filter_generic_genres, taste_affinity
from strategies.candidates import USER_FILTERS, _cap_per_artist
from strategies.scoring import ARTIST_CAP, TREND_KNOWN_ARTIST_MATCH, TREND_RANK_SPREAD, TREND_WILDCARDS
from strategies.sequencing import sequence_tracks


# ── Strategy: Trend Radar ────────────────────────────────────────

def strategy_trend(profile: dict, sf: str, target_size: int = 20,
                   rng: random.Random | None = None) -> list[dict]:
    """Trending tracks filtered through user's taste, with wildcards."""
    user_genres = profile.get("genre_distribution", [])
    user_artist_names = {a["name"].lower() for a in profile.get("top_artists", [])[:15]}
    library_ids = set(profile.get("library_song_ids", []))
    disliked = set(profile.get("disliked_song_ids", []))

    candidates = []
    seen_ids = set()

    # Fetch overall charts
    print("  Fetching overall charts...", file=sys.stderr)
    charts = call_api("charts", sf)
    if charts:
        for section in charts.get("results", {}).values():
            if isinstance(section, list):
                for chart in section:
                    chart_items = chart.get("data", [])
                    for rank, item in enumerate(chart_items):
                        attrs = item.get("attributes", {})
                        tid = item.get("id", "")
                        if not tid or tid in library_ids or tid in disliked or tid in seen_ids:
                            continue
                        seen_ids.add(tid)
                        item_genres = filter_generic_genres(attrs.get("genreNames", []))
                        artist_name = attrs.get("artistName", "")

                        taste_match = taste_affinity(item_genres, user_genres)
                        if artist_name.lower() in user_artist_names:
                            taste_match = max(taste_match, TREND_KNOWN_ARTIST_MATCH)

                        rank_weight = 1.0 - (rank / len(chart_items)) * TREND_RANK_SPREAD
                        score = taste_match * rank_weight

                        candidates.append({
                            "id": tid,
                            "name": attrs.get("name", ""),
                            "artist": artist_name,
                            "album": "",
                            "genre": item_genres,
                            "duration_ms": attrs.get("durationInMillis"),
                            "explicit": attrs.get("contentRating") == "explicit",
                            "source": "trending",
                            "reason": "Trending and matches your taste.",
                            "_score": score,
                            "_is_wildcard": taste_match == 0,
                        })

    # Separate wildcards (zero taste match) and matched
    candidates = apply_user_filters(candidates, USER_FILTERS)
    matched = [c for c in candidates if not c.get("_is_wildcard")]
    wildcards = [c for c in candidates if c.get("_is_wildcard")]

    # Sort matched by score
    matched.sort(key=lambda c: c["_score"], reverse=True)

    # Pick main tracks (max 3 per artist) + 2-3 wildcards
    wildcard_count = min(TREND_WILDCARDS, len(wildcards), max(target_size, 0))
    main_count = target_size - wildcard_count
    selected = _cap_per_artist(matched, main_count, ARTIST_CAP)

    if wildcards:
        (rng or random.Random()).shuffle(wildcards)
        selected.extend(wildcards[:wildcard_count])

    for c in selected:
        c.pop("_score", None)
        c.pop("_is_wildcard", None)
        if c in wildcards[:wildcard_count]:
            c["reason"] = "A wildcard pick — something outside your usual taste."

    return sequence_tracks(selected)
