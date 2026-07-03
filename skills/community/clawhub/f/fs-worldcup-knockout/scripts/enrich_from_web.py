#!/usr/bin/env python3
"""
Enrich player_data.json with fantasy-pick sentiment from web articles.

Player list is pulled dynamically from the live FS market API — no need to
maintain a static list. player_data.json becomes a sentiment cache: players
are added/updated from live markets, sentiment fields are written back.

Sentiment scoring: keyword-match titles + snippets from Brave Search results.
  +1.0 = universally bullish (captain, must-start, top pick)
  -1.0 = universally bearish (injured, suspended, avoid)

Main trader (main.py) reads sentiment_score and sentiment_sources to adjust
the FS expected-score line ±15%.

Requires:
  BRAVE_API_KEY  — Brave Search API key (same one oracle.py uses).
                   Free tier: 2,000 queries/month.
  FS_USERNAME    — Used to authenticate to FS API for the player list.
  FS_BASE_URL    — Engine URL (optional, defaults to mech-v0-4).
  FS_ROUND       — Round to pull players for, e.g. "MD3" (default: all open).

Usage:
    export BRAVE_API_KEY=...
    export FS_USERNAME=simmer_agent_1
    python3 scripts/enrich_from_web.py
    python3 scripts/enrich_from_web.py --player "Kylian Mbappé"
    python3 scripts/enrich_from_web.py --round "round of 32"
    python3 scripts/enrich_from_web.py --dry-run
"""

import json
import os
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# Allow importing fs_client from the parent skill directory
sys.path.insert(0, str(Path(__file__).parent.parent))
from fs_client import FSClient

DATA_PATH = Path(__file__).parent.parent / "data" / "player_data.json"
FS_BASE_URL = os.environ.get("FS_BASE_URL", "https://fs-engine-api-mech-v0-4.onrender.com")
FS_ROUND    = os.environ.get("FS_ROUND", "")

DRY_RUN    = "--dry-run" in sys.argv
PLAYER_ARG = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--player"), None)
ROUND_ARG  = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--round"), "knockout")

# ---------------------------------------------------------------------------
# Sentiment keyword lists
# ---------------------------------------------------------------------------

POSITIVE = {
    "captain", "vc", "vice-captain", "must-start", "must start", "must-own",
    "essential", "differential", "start", "pick", "recommend", "recommended",
    "brilliant", "in form", "in-form", "brace", "hat-trick", "key player",
    "clinical", "unstoppable", "best bet", "top pick", "great shout",
    "good pick", "love him", "back him", "go for", "triple up",
}

NEGATIVE = {
    "avoid", "injury", "injured", "doubt", "doubtful", "suspended",
    "suspension", "bench", "benched", "struggle", "poor form", "out of form",
    "miss", "questionable", "fitness concern", "drop", "sell", "transfer out",
    "not guaranteed", "rotation risk", "unlikely to start", "poor choice",
    "ban", "banned", "red card",
}

# ---------------------------------------------------------------------------
# FS market player list (live, dynamic)
# ---------------------------------------------------------------------------

def _players_from_fs(round_filter: str = "") -> list[dict]:
    """
    Pull the current WC player list from live FS markets.
    Returns a list of {name, position, team} dicts — one per unique player.
    """
    client = FSClient(base_url=FS_BASE_URL)
    markets = client.list_markets(status="open")

    seen: set[str] = set()
    players: list[dict] = []
    for m in markets:
        md = m.get("metadata") or {}
        scope = (md.get("scope") or "") + " " + " ".join(md.get("categories") or [])
        if not (("World Cup" in scope or "WC" in scope) and md.get("position") in ("FWD", "MID", "DEF")):
            continue
        if round_filter and md.get("round") != round_filter:
            continue
        name = md.get("player")
        if not name or name in seen:
            continue
        seen.add(name)
        players.append({
            "name":     name,
            "position": md.get("position", ""),
            "team":     md.get("team", ""),
        })

    return sorted(players, key=lambda p: (p["position"], p["name"]))


# ---------------------------------------------------------------------------
# Brave Search
# ---------------------------------------------------------------------------

def _search_brave(query: str, api_key: str, num_results: int = 8) -> list[dict]:
    params = urllib.parse.urlencode({
        "q":              query,
        "count":          num_results,
        "freshness":      "pm",
        "extra_snippets": "true",
    })
    url = f"https://api.search.brave.com/res/v1/web/search?{params}"
    req = urllib.request.Request(url, headers={
        "Accept":               "application/json",
        "Accept-Encoding":      "gzip",
        "X-Subscription-Token": api_key,
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            data = json.loads(res.read())
        results = data.get("web", {}).get("results", [])
        return [
            {
                "title":       r.get("title", ""),
                "description": " ".join([r.get("description", ""), *r.get("extra_snippets", [])]),
            }
            for r in results
        ]
    except Exception as e:
        print(f"    Brave search error: {e}")
        return []


def _score_text(text: str) -> tuple[int, int]:
    t = text.lower()
    return sum(1 for kw in POSITIVE if kw in t), sum(1 for kw in NEGATIVE if kw in t)


def _sentiment(results: list[dict]) -> tuple[float, int]:
    total_pos = total_neg = 0
    seen: set[str] = set()
    for r in results:
        key = r["title"][:60]
        if key in seen:
            continue
        seen.add(key)
        p, n = _score_text(r["title"] + " " + r["description"])
        total_pos += p
        total_neg += n
    sources = len(seen)
    if total_pos + total_neg == 0:
        return 0.0, sources
    score = (total_pos - total_neg) / (total_pos + total_neg + 1)
    return round(max(-1.0, min(1.0, score)), 3), sources


def _normalize(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn").strip()


def _build_queries(player: dict, round_context: str) -> list[str]:
    name = player["name"]
    team = player.get("team", "")
    return [
        f'"{name}" World Cup 2026 fantasy football pick',
        f'"{name}" {team} WC 2026 fantasy {round_context} recommendation',
    ]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    brave_key = os.environ.get("BRAVE_API_KEY")
    if not brave_key:
        print("ERROR: BRAVE_API_KEY is required.")
        print("  Get a free key at https://api.search.brave.com/")
        sys.exit(1)

    # Pull live player list from FS API
    round_filter = FS_ROUND
    print(f"Fetching player list from FS API ({FS_BASE_URL})...")
    live_players = _players_from_fs(round_filter=round_filter)
    print(f"  {len(live_players)} unique players found"
          + (f" for round={round_filter}" if round_filter else " (all open rounds)"))

    if not live_players:
        print("No WC player markets found. Is the competition live?")
        sys.exit(1)

    # Load existing sentiment cache (keyed by name)
    existing: dict[str, dict] = {}
    if DATA_PATH.exists():
        for p in json.loads(DATA_PATH.read_text()):
            existing[p["name"]] = p

    # Merge: live player identities + existing sentiment cache
    players: list[dict] = []
    for lp in live_players:
        record = dict(existing.get(lp["name"], {}))
        record.update({k: v for k, v in lp.items() if v})  # refresh position/team
        if "name" not in record:
            record["name"] = lp["name"]
        players.append(record)

    # Also retain players from cache who aren't in this round's markets
    # (they may appear in later rounds)
    live_names = {p["name"] for p in live_players}
    for name, record in existing.items():
        if name not in live_names:
            players.append(record)

    # Apply --player filter
    targets = players
    if PLAYER_ARG:
        targets = [p for p in players if _normalize(PLAYER_ARG) in _normalize(p["name"])]
        if not targets:
            print(f"No players found matching '{PLAYER_ARG}'")
            sys.exit(1)

    print(f"\nEnriching {len(targets)} player(s) for round context: '{ROUND_ARG}'")
    print(f"Brave API key: {brave_key[:6]}…\n")

    now = datetime.now(timezone.utc).isoformat()
    updated = 0

    for player in targets:
        name    = player["name"]
        pos     = player.get("position", "?")
        team    = player.get("team", "")
        queries = _build_queries(player, ROUND_ARG)

        all_results: list[dict] = []
        for q in queries:
            results = _search_brave(q, brave_key)
            all_results.extend(results)
            time.sleep(0.35)

        score, sources = _sentiment(all_results)
        arrow = "↑" if score > 0.1 else ("↓" if score < -0.1 else "→")
        print(f"  {name:<28} [{pos}] {team:<14} {arrow} {score:+.2f}  ({sources} results)")

        player["sentiment_score"]   = score
        player["sentiment_sources"] = sources
        player["sentiment_updated"] = now
        updated += 1

    # Report
    scored = sorted(targets, key=lambda p: p.get("sentiment_score", 0), reverse=True)
    print(f"\nTop 3 bullish:")
    for p in scored[:3]:
        print(f"  {p['name']} [{p.get('position','?')}]: {p.get('sentiment_score', 0):+.2f}")
    print("Top 3 bearish:")
    for p in scored[-3:]:
        print(f"  {p['name']} [{p.get('position','?')}]: {p.get('sentiment_score', 0):+.2f}")

    if DRY_RUN:
        print(f"\n[DRY RUN] {updated} players scored — no changes written.")
        return

    # Merge updated targets back into full player list and write
    name_to_updated = {p["name"]: p for p in targets}
    out = [name_to_updated.get(p["name"], p) for p in players]
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\nUpdated {updated} players → {DATA_PATH}")


if __name__ == "__main__":
    main()
