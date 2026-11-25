"""Strategy: constellation discovery (gradual drift from familiar to frontier)."""

import random
import sys

from _common import SUBGENRE_PROXIMITY, apply_user_filters, best_genre_match, call_api, filter_generic_genres, search_artist
from strategies.candidates import USER_FILTERS, _first_data, _similar_artists
from strategies.scoring import CONSTELLATION_SPLIT


# ── Strategy: Constellation Discovery ────────────────────────────

def strategy_constellation(profile: dict, sf: str, target_size: int = 25,
                           rng: random.Random | None = None) -> list[dict]:
    """Gradual discovery: familiar → expansion → frontier."""
    top_artists = profile.get("top_artists", [])[:5]
    user_genres = [g["genre"] for g in profile.get("genre_distribution", [])[:10]]
    library_ids = set(profile.get("library_song_ids", []))
    library_artists = {a["name"].lower() for a in profile.get("top_artists", [])}
    disliked = set(profile.get("disliked_song_ids", []))

    # Discover adjacent artists
    discovered = []
    visited_ids = set()

    for artist in top_artists:
        artist_name = artist.get("name", "")
        print(f"  Exploring from {artist_name}...", file=sys.stderr)

        # Apple's similar artists when the catalog has them; otherwise search by name + genre
        candidates = _similar_artists(sf, artist["id"]) if artist.get("id") else []
        if not candidates:
            artist_obj = search_artist(sf, artist_name)
            if not artist_obj:
                continue
            artist_genres = [g for g in artist_obj.get("attributes", {}).get("genreNames", [])
                             if g.lower() != "music"]
            search_query = f"{artist_name} {' '.join(artist_genres[:2])}"
            candidates = _first_data(call_api("search", sf, search_query, "artists"), "artists")

        for c in candidates:
            cid = c.get("id", "")
            cname = c.get("attributes", {}).get("name", "")
            if cid in visited_ids or cname.lower() in library_artists:
                continue
            visited_ids.add(cid)

            c_genres = [g for g in c.get("attributes", {}).get("genreNames", [])
                        if g.lower() != "music"]
            proximity = best_genre_match(c_genres, user_genres)

            # Classify zone: your genres or their sub-genres are familiar, the same family expands
            if proximity >= SUBGENRE_PROXIMITY:
                zone = "familiar"
            elif proximity >= 0.4:
                zone = "expansion"
            else:
                zone = "frontier"

            discovered.append({
                "artist_id": cid,
                "artist_name": cname,
                "genres": c_genres,
                "proximity": proximity,
                "zone": zone,
                "seed_artist": artist_name,
            })

    # Fetch top songs from discovered artists
    all_tracks = []
    for disc in discovered:
        top_data = call_api("artist-top", sf, disc["artist_id"])
        if not top_data or "data" not in top_data:
            continue
        for ad in top_data["data"]:
            views = ad.get("views", {})
            for ts in views.get("top-songs", {}).get("data", [])[:3]:
                tid = ts.get("id", "")
                if tid in library_ids or tid in disliked:
                    continue
                attrs = ts.get("attributes", {})
                all_tracks.append({
                    "id": tid,
                    "name": attrs.get("name", ""),
                    "artist": disc["artist_name"],
                    "album": "",
                    "genre": filter_generic_genres(attrs.get("genreNames", [])),
                    "duration_ms": attrs.get("durationInMillis"),
                    "explicit": attrs.get("contentRating") == "explicit",
                    "source": "constellation",
                    "zone": disc["zone"],
                    "reason": f"Discovered via {disc['seed_artist']} — {disc['zone']} zone.",
                    "_proximity": disc["proximity"],
                    "_score": 0.0,  # only the user filters' preferred-genre boost ranks within a zone
                })

    # Build gradient: familiar first, then expansion, then frontier
    all_tracks = apply_user_filters(all_tracks, USER_FILTERS)
    familiar = [t for t in all_tracks if t.get("zone") == "familiar"]
    expansion = [t for t in all_tracks if t.get("zone") == "expansion"]
    frontier = [t for t in all_tracks if t.get("zone") == "frontier"]

    # Allocate proportionally to target:  ~30% familiar, ~45% expansion, ~25% frontier
    # (no max(1, ...): for tiny sizes that made the frontier quota negative, and a negative
    # slice returns almost the whole zone)
    fam_count = int(target_size * CONSTELLATION_SPLIT[0])
    exp_count = int(target_size * CONSTELLATION_SPLIT[1])
    fro_count = max(target_size - fam_count - exp_count, 0)

    rng = rng or random.Random()
    zones = {"familiar": familiar, "expansion": expansion, "frontier": frontier}
    for tracks in zones.values():
        rng.shuffle(tracks)  # random order among equally preferred tracks
        tracks.sort(key=lambda t: t["_score"], reverse=True)  # stable: preferred genres first
    picked = {"familiar": familiar[:fam_count], "expansion": expansion[:exp_count],
              "frontier": frontier[:fro_count]}

    # A short zone is backfilled from the others' leftovers, middle zone first,
    # so the playlist still reaches its length and keeps the gradient order
    short = target_size - sum(len(t) for t in picked.values())
    for zone in ("expansion", "familiar", "frontier"):
        if short <= 0:
            break
        extra = zones[zone][len(picked[zone]):][:short]
        picked[zone] += extra
        short -= len(extra)

    selected = picked["familiar"] + picked["expansion"] + picked["frontier"]

    # Clean internal fields
    for c in selected:
        c.pop("_proximity", None)
        c.pop("_score", None)

    # Don't re-sequence — the gradient order IS the sequence
    return selected
