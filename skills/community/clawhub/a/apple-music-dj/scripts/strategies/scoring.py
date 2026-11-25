"""Tunable numbers shared by the playlist strategies, in one place."""

# ── Scoring weights (every strategy's tunable numbers, in one place) ──
# Scores are compared within one strategy only; what matters is each term's size
# relative to the others and to JITTER.

JITTER = 0.1            # random 0-JITTER added to every score, so equal tracks vary between runs

ARTIST_CAP = 3          # max tracks per artist

TASTE_WEIGHT = 0.3      # x taste_affinity: how much your own genres lift a candidate (seed, era)

OWN_ARTIST_BOOST = 0.1  # artists you already play (mood, seed)

PLAY_WEIGHT_SCALE, PLAY_WEIGHT_MAX = 2, 0.3  # head start for artists you play more (deep cuts, era)

DEEP_CUT_BASE = 0.5

DEEP_CUT_POSITION_BONUS = 0.15  # the last track of an album gets this much over the first

MOOD_GENRE_WEIGHT, MOOD_ENERGY_WEIGHT, MOOD_TASTE_WEIGHT = 0.5, 0.35, 0.15

MIN_ENERGY_FIT = 0.5  # mood candidates further than this from the target energy are dropped

TREND_KNOWN_ARTIST_MATCH = 0.8  # floor on taste match for an artist already in your top list

TREND_RANK_SPREAD = 0.3         # chart #1 scores x1.0, the last chart entry x(1 - this)

TREND_WILDCARDS = 3

CONSTELLATION_SPLIT = (0.3, 0.45)  # familiar, expansion shares; frontier gets the rest

REFRESH_ARTIST_SCORE = 0.7  # "new from" an artist already in the playlist; chart picks score their genre match

SEED_MATCH_WEIGHT = 0.6  # x genre match to the seed artist/song

SEED_BASE = {"top": 0.5, "album": 0.55, "similar": 0.3, "genre_fallback": 0.2}

ERA_BASE = {"artist": 0.5, "chart": 0.4, "search": 0.3}

BLEND_MAX_SHARE = 0.6  # neither listener may supply more than this share of the tracks

BLEND_SHARED_SCORE, BLEND_LOVED_SCORE = 1.0, 0.6

BLEND_SIDE_BASE, BLEND_SIDE_MATCH = 0.4, 0.5  # a listener's own artist: base + this x fit to the other's taste


def _artist_boost(artist: dict) -> float:
    """Head start for an artist by how much you play them."""
    return min(artist.get("play_weight", 0) * PLAY_WEIGHT_SCALE, PLAY_WEIGHT_MAX)

REMIX_KEEP_MIN = 0.3         # taste fit an original track needs to be kept (taste_affinity, plus the own-artist boost)
REMIX_KEEP_BASE = 0.8        # kept originals outrank swaps: the playlist is the starting point
REMIX_SWAP_BASE = 0.4
REMIX_MAX_LOOKUPS = 12       # dropped tracks we look a replacement up for (each costs a few API calls)
