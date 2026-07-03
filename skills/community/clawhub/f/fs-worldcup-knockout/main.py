#!/usr/bin/env python3
"""
FunctionSpace World Cup Knockout Trader — Simmer ClawHub skill.

Competition format: each round, pick 1 FWD + 1 MID + 1 DEF. Those 3 markets
are locked until round settlement (after that round's fixtures complete).

Strategy:
  1. Fetch all open WC player markets for the target round.
  2. For each market, take FS's own expected score (metadata.expectedPts) as
     the base, then apply a sentiment adjustment from expert fantasy articles
     (±15% shift from scripts/enrich_from_web.py).
  3. Build a multimodal density belief (appearance cluster + return cluster)
     over the market buckets, matching the shape of propSPACE player markets.
  4. Compute edge: |our belief mean − current market consensus mean|.
  5. In 3-pick mode (default): rank markets per position, buy best 1 FWD + 1
     MID + 1 DEF. In --all-markets mode: buy all above FS_MIN_EDGE threshold.

Dry-run by default. Pass --live to execute propSPACE play-money trades.

Usage:
    python main.py                     # dry run: pick best FWD/MID/DEF
    python main.py --live              # execute 3 play-money picks
    python main.py --list-markets      # list open markets with positions
    python main.py --market 312        # target a single market
    python main.py --inspect 312       # show consensus vs our belief
    python main.py --all-markets       # trade all markets above edge threshold
    python main.py --round MD3         # override which round to trade

Environment:
    FS_BASE_URL         FunctionSpace engine URL
    FS_USERNAME         Agent username (auto-created on first run)
    FS_PASSWORD         Agent password (min 6 chars; set once, reused)
    FS_ROUND            Round to trade, e.g. "MD3" (default: highest open round)
    FS_MAX_COLLATERAL   Max play-money per trade (default: 333 = $1000/3)
    FS_MIN_EDGE         Min edge for --all-markets mode (default: 0.05)
    FS_MARKET_FILTER    Title keyword filter (default: "" = all markets)
    FS_RECIPE_SHAPE     Belief recipe shape: multimodal (default) or normal
    BRAVE_API_KEY       For scripts/enrich_from_web.py (optional)
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path

from fs_client import FSClient, FSHTTPError

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BASE_URL       = os.environ.get("FS_BASE_URL", "https://fs-engine-api-mech-v0-4.onrender.com")
USERNAME       = os.environ.get("FS_USERNAME")
PASSWORD       = os.environ.get("FS_PASSWORD", "simmer-wc-bot")
ROUND_FILTER   = os.environ.get("FS_ROUND", "")          # e.g. "MD3"; empty = auto
MAX_COLLATERAL = float(os.environ.get("FS_MAX_COLLATERAL", 333))
MIN_EDGE       = float(os.environ.get("FS_MIN_EDGE", 0.05))
MARKET_FILTER  = os.environ.get("FS_MARKET_FILTER", "")
RECIPE_SHAPE   = os.environ.get("FS_RECIPE_SHAPE", "multimodal").lower()

DATA_DIR  = Path(__file__).parent / "data"
TOKEN_DIR = Path(__file__).parent / ".auth"

# ---------------------------------------------------------------------------
# FIFA World Cup Fantasy scoring table (from propSPACE integration guide §9)
#
# Used to derive position-aware spread estimates. The base expected score comes
# from metadata.expectedPts (FS's calibrated model), so we don't need to
# recompute the full formula — but we do need position-specific variance.
# ---------------------------------------------------------------------------

# Point values per action by position (for spread derivation)
GOAL_PTS   = {"FWD": 5, "MID": 6, "DEF": 7}
ASSIST_PTS = 3         # same across all outfield positions
CS_PTS     = {"FWD": 0, "MID": 1, "DEF": 5}   # clean sheet bonus (60+ mins)

# Approximate fantasy-points spread by position (actual pts, not normalized).
# Used for baseline normal recipes and the return cluster width in multimodal mode.
# The base expected score comes from FS metadata; these constants control belief
# shape rather than the mean projection itself.
POSITION_SPREAD_PTS = {
    "FWD": 4.5,
    "MID": 3.2,
    "DEF": 4.8,
    "GK":  3.5,
}

# ---------------------------------------------------------------------------
# Position constants
# ---------------------------------------------------------------------------

POSITION_MAP = {
    "FW": "FWD", "FWD": "FWD", "FORWARD": "FWD",
    "MF": "MID", "MID": "MID", "MIDFIELDER": "MID",
    "DF": "DEF", "DEF": "DEF", "DEFENDER": "DEF",
    "GK": "GK",  "GKP": "GK",  "GOALKEEPER": "GK",
}
COMP_POSITIONS = ["FWD", "MID", "DEF"]

# ---------------------------------------------------------------------------
# Player data (for sentiment enrichment)
# ---------------------------------------------------------------------------

def _load_player_data() -> list[dict]:
    path = DATA_DIR / "player_data.json"
    if not path.exists():
        return []
    with open(path) as f:
        return json.load(f)

PLAYER_DATA = _load_player_data()


def _normalize_str(s: str) -> str:
    import unicodedata
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(
        c for c in s if unicodedata.category(c) != "Mn" and (c.isalpha() or c.isspace())
    ).strip()


def _find_player(name: str) -> dict | None:
    """Match a player name (from market metadata or title) to player_data.json."""
    t = _normalize_str(name)
    for p in PLAYER_DATA:
        candidates = [p["name"]] + p.get("aliases", [])
        if any(_normalize_str(c) in t or t in _normalize_str(c) for c in candidates):
            return p
    return None


# ---------------------------------------------------------------------------
# Market filtering helpers
# ---------------------------------------------------------------------------

def is_wc_player_market(m: dict) -> bool:
    """True if this market is a WC player prop (not a team/match market)."""
    md = m.get("metadata") or {}
    scope = (md.get("scope") or "") + " " + " ".join(md.get("categories") or [])
    return (
        ("World Cup" in scope or "WC" in scope)
        and md.get("position") in ("FWD", "MID", "DEF")
    )


def market_round(m: dict) -> str:
    """Return the round string (e.g. 'MD3') from market metadata."""
    return (m.get("metadata") or {}).get("round", "")


def _active_round(markets: list[dict]) -> str:
    """Pick the highest round string among open WC markets (e.g. MD3 > MD2 > MD1)."""
    rounds = sorted(set(market_round(m) for m in markets if is_wc_player_market(m)))
    return rounds[-1] if rounds else ""


# ---------------------------------------------------------------------------
# Strategy
# ---------------------------------------------------------------------------

def _normal_pdf(x: float, mu: float, sigma: float) -> float:
    """Unnormalized normal density; sigma is in fantasy points."""
    sigma = max(0.05, sigma)
    z = (x - mu) / sigma
    return math.exp(-0.5 * z * z)


def _normalize_density(weights: list[float]) -> list[float]:
    total = sum(max(0.0, w) for w in weights)
    if total <= 0:
        return [1.0 / len(weights)] * len(weights)
    return [max(0.0, w) / total for w in weights]


def _market_bucket_centers(market: dict) -> list[float]:
    lower, upper, n = market["lower_bound"], market["upper_bound"], market["num_buckets"]
    width = (upper - lower) / n
    return [lower + (i + 0.5) * width for i in range(n)]


def build_multimodal_density(market: dict, expected_pts: float, pos: str | None) -> list[float]:
    """
    Build a propSPACE-style player fantasy distribution: a low appearance / low-return
    cluster plus a higher return cluster. The mixture is intentionally simple and
    explainable; it is closer to FS pricing shape than a single symmetric Gaussian.
    """
    lower = float(market["lower_bound"])
    upper = float(market["upper_bound"])
    span = max(upper - lower, 1e-6)
    centers = _market_bucket_centers(market)

    expected_pts = max(lower, min(upper, expected_pts))

    # Appearance/no-return cluster near the lower part of the range, but never above
    # the expected value. Defenders get a slightly wider low cluster because clean-sheet
    # outcomes create more binary mass; attackers get a sharper low-return cluster.
    app_mean = lower + 0.18 * span
    app_mean = min(app_mean, expected_pts - 0.08 * span)
    app_mean = max(lower + 0.03 * span, app_mean)

    app_weight_by_pos = {"FWD": 0.42, "MID": 0.48, "DEF": 0.52, "GK": 0.56}
    app_weight = app_weight_by_pos.get(pos or "", 0.48)

    # Choose return-cluster mean so the mixture mean remains near expectedPts.
    ret_weight = 1.0 - app_weight
    ret_mean = (expected_pts - app_weight * app_mean) / max(ret_weight, 1e-6)
    if ret_mean > upper - 0.03 * span:
        ret_mean = upper - 0.03 * span
        app_weight = max(0.20, min(0.70, (ret_mean - expected_pts) / max(ret_mean - app_mean, 1e-6)))
        ret_weight = 1.0 - app_weight
    ret_mean = max(app_mean + 0.08 * span, min(upper - 0.03 * span, ret_mean))

    base_spread = POSITION_SPREAD_PTS.get(pos or "", 3.5)
    app_sigma = max(span / market["num_buckets"], base_spread * 0.35)
    ret_sigma = max(span / market["num_buckets"], base_spread * 0.55)

    weights = [
        app_weight * _normal_pdf(x, app_mean, app_sigma)
        + ret_weight * _normal_pdf(x, ret_mean, ret_sigma)
        for x in centers
    ]
    return [round(v, 8) for v in _normalize_density(weights)]


def build_recipe(market: dict, expected_pts: float, pos: str | None) -> dict:
    """Build the configured FS position recipe."""
    lower, upper = market["lower_bound"], market["upper_bound"]
    mean_norm = FSClient.normalize(expected_pts, market)

    if RECIPE_SHAPE == "normal":
        spread_pts = POSITION_SPREAD_PTS.get(pos, 3.5)
        std_norm = spread_pts / (upper - lower)
        std_norm = min(std_norm, min(mean_norm, 1.0 - mean_norm) + 0.01)
        return {
            "position_type": "normal",
            "position_params": {
                "mean": round(mean_norm, 4),
                "std_dev": round(std_norm, 4),
            },
        }

    density = build_multimodal_density(market, expected_pts, pos)
    return {
        "position_type": "density",
        "position_params": {"density": density},
    }


def recipe_mean_norm(recipe: dict, market: dict) -> float:
    """Return the normalized mean implied by any recipe type used by this skill."""
    ptype = recipe.get("position_type")
    params = recipe.get("position_params") or {}
    if ptype == "normal":
        return float(params["mean"])
    if ptype == "density":
        density = params.get("density") or []
        centers = _market_bucket_centers(market)
        total = sum(density)
        if total > 0 and len(density) == len(centers):
            pts = sum(w * x for w, x in zip(density, centers)) / total
            return FSClient.normalize(pts, market)
    if ptype == "box":
        return (float(params["lower"]) + float(params["upper"])) / 2.0
    return 0.5


def strategy_for_market(market: dict) -> tuple[dict | None, str | None, float, str]:
    """
    Returns (recipe, position, our_expected_pts, description) or
            (None, None, 0.0, reason_string).

    recipe = {"position_type": "normal", "position_params": {"mean": .., "std_dev": ..}}
    position = "FWD" | "MID" | "DEF" | None
    """
    meta   = market.get("metadata") or {}
    pos_raw = meta.get("position", "")
    pos    = POSITION_MAP.get(pos_raw.upper())
    lower  = market["lower_bound"]
    upper  = market["upper_bound"]

    # Base expected score from FS's model (FIFA-calibrated, per player per fixture)
    base_expected = meta.get("expectedPts") or meta.get("line")
    if base_expected is None:
        return None, pos, 0.0, "no expectedPts in market metadata"

    base_expected = float(base_expected)

    # Sentiment adjustment from expert fantasy articles
    player_name = meta.get("player") or market.get("title", "")
    player      = _find_player(player_name)
    sentiment   = player.get("sentiment_score") if player else None
    sources     = player.get("sentiment_sources", 0) if player else 0

    source_parts = [f"FS line={base_expected:.1f}pts"]

    if sentiment is not None and sources >= 3:
        expected = base_expected * (1.0 + 0.15 * sentiment)
        arrow    = "↑" if sentiment > 0.1 else ("↓" if sentiment < -0.1 else "→")
        source_parts.append(f"sentiment {arrow}{sentiment:+.2f} ({sources} src)")
    else:
        expected = base_expected
        if player is None:
            source_parts.append("player not in DB — using FS line as-is")
        elif sentiment is None:
            source_parts.append("no sentiment — run enrich_from_web.py")

    expected = max(lower, min(upper, expected))

    recipe = build_recipe(market, expected, pos)
    shape_note = "multimodal density" if recipe["position_type"] == "density" else "normal"

    player_label = meta.get("player") or "?"
    team_label   = meta.get("team") or ""
    desc = (
        f"{player_label} ({team_label}) [{pos}]: "
        f"E={expected:.1f}pts  [{' + '.join(source_parts)}; recipe={shape_note}]"
    )
    return recipe, pos, expected, desc


# ---------------------------------------------------------------------------
# Trade execution
# ---------------------------------------------------------------------------

def _execute_trade(
    client: FSClient,
    market: dict,
    recipe: dict,
    expected_pts: float,
    desc: str,
    dry_run: bool,
    username: str,
    password: str,
) -> bool:
    """Print trade details and execute (or simulate). Returns True if traded."""
    cmean  = FSClient.consensus_mean(market)
    mnorm  = recipe_mean_norm(recipe, market)
    our_pts = FSClient.denormalize(mnorm, market)
    edge   = abs(mnorm - FSClient.normalize(cmean, market))

    print(f"  [{market['market_id']}] {market.get('title', '')[:55]}")
    print(f"    {desc}")
    print(f"    Our E: {our_pts:.2f}pts  Consensus: {cmean:.2f}pts  Edge: {edge*100:.1f}%")

    if dry_run:
        print(f"    → WOULD BUY collateral={MAX_COLLATERAL} (dry run)\n")
        return False

    def _buy_once() -> dict:
        return client.buy(
            market["market_id"],
            recipe["position_type"],
            recipe["position_params"],
            MAX_COLLATERAL,
            metadata={"skill": "fs-worldcup-knockout", "expected_pts": expected_pts},
        )

    try:
        result = _buy_once()
    except FSHTTPError as e:
        if e.code != 401:
            print(f"    ERROR {e.code}: {e.body[:120]}\n")
            return False
        print("    ERROR 401 — token expired; re-login and retry once.")
        try:
            client.relogin(username, password)
            result = _buy_once()
            print("    401 retry succeeded.")
        except FSHTTPError as retry_error:
            print(f"    ERROR after re-login {retry_error.code}: {retry_error.body[:120]}\n")
            return False

    pos_id     = result.get("position_id")
    trade_size = result.get("trade_size", "?")
    print(
        f"    → BOUGHT market_id={market['market_id']} "
        f"position_id={pos_id} trade_size={trade_size}\n"
    )
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="FS World Cup Knockout trader")
    parser.add_argument("--live",         action="store_true", help="Execute real trades (default: dry run)")
    parser.add_argument("--list-markets", action="store_true", help="List open WC markets with positions")
    parser.add_argument("--market",       type=int, default=None, help="Target a single market ID")
    parser.add_argument("--inspect",      type=int, default=None, help="Inspect consensus vs our belief")
    parser.add_argument("--all-markets",  action="store_true", help="Trade ALL markets above edge threshold")
    parser.add_argument("--round",        type=str, default=None, help="Target a specific round (e.g. MD3)")
    args = parser.parse_args()

    if not USERNAME:
        print("ERROR: FS_USERNAME is required.")
        sys.exit(1)

    dry_run = not args.live
    if dry_run:
        print("[DRY RUN] Pass --live to execute propSPACE play-money trades.\n")

    token_path = TOKEN_DIR / f"{USERNAME}.json"
    client = FSClient(base_url=BASE_URL, token_store=token_path)

    # Auth — try stored token first via me(), fall back to signup/login
    try:
        user = client.me()
    except FSHTTPError:
        user = client.signup_or_login(USERNAME, PASSWORD)

    balance = user.get("wallet_value", "?")
    print(f"Authenticated as {user.get('username', USERNAME)}  balance={balance}\n")

    # -----------------------------------------------------------------------
    # Single-market modes
    # -----------------------------------------------------------------------

    if args.market or args.inspect:
        mid = args.market or args.inspect
        m   = client.market_state(mid)
        recipe, pos, expected, desc = strategy_for_market(m)
        cmean = FSClient.consensus_mean(m)

        print(f"Market {mid}: {m.get('title', '')}")
        meta = m.get("metadata") or {}
        print(f"  Round: {meta.get('round', '?')}  Position: {pos}  "
              f"Range: {m['lower_bound']}–{m['upper_bound']}  Buckets: {m['num_buckets']}")
        print(f"  FS expected: {meta.get('expectedPts', '?')}pts  "
              f"Consensus mean: {cmean:.2f}pts")

        if recipe:
            mnorm  = recipe_mean_norm(recipe, m)
            our_pts = FSClient.denormalize(mnorm, m)
            edge   = abs(mnorm - FSClient.normalize(cmean, m))
            print(f"  Our belief:  {our_pts:.2f}pts  Edge: {edge*100:.1f}%")
            print(f"  Recipe:      {recipe}")
            print(f"  {desc}")
            # Show payout curve for the "at our expected score" outcome
            bucket = min(m["num_buckets"] - 1, max(0, int(
                (expected - m["lower_bound"]) / (m["upper_bound"] - m["lower_bound"]) * m["num_buckets"]
            )))
            print(f"  Winning bucket if our prediction is right: {bucket}")
        else:
            print(f"  No strategy: {desc}")

        if args.live and recipe and not dry_run:
            _execute_trade(client, m, recipe, expected, desc, dry_run=False, username=USERNAME, password=PASSWORD)
        return

    # -----------------------------------------------------------------------
    # Discover markets
    # -----------------------------------------------------------------------

    all_markets = client.list_markets(status="open")

    # Filter to WC player markets
    wc_markets = [m for m in all_markets if is_wc_player_market(m)]

    # Round filter: CLI arg > FS_ROUND env > auto-detect highest open round
    target_round = args.round or ROUND_FILTER or _active_round(wc_markets)
    if target_round:
        wc_markets = [m for m in wc_markets if market_round(m) == target_round]

    # Optional title keyword filter
    if MARKET_FILTER:
        wc_markets = [m for m in wc_markets if MARKET_FILTER.lower() in m.get("title", "").lower()]

    # -----------------------------------------------------------------------
    # --list-markets
    # -----------------------------------------------------------------------

    if args.list_markets:
        print(f"Open WC markets  round={target_round or 'all'}  ({len(wc_markets)} markets)\n")
        for m in sorted(wc_markets, key=lambda x: (x.get("metadata", {}).get("position", ""), x.get("title", ""))):
            meta   = m.get("metadata") or {}
            pos    = meta.get("position", "???")
            player = meta.get("player") or m.get("title", "?")[:30]
            team   = meta.get("team", "?")
            ep     = meta.get("expectedPts", "?")
            cmean  = FSClient.consensus_mean(m)
            in_db  = "✓" if _find_player(player) else "✗"
            print(f"  [{m['market_id']:4d}] {pos:3s} {in_db}  "
                  f"{player:<28} {team:<12} "
                  f"FS={ep}  consensus={cmean:.1f}pts")
        return

    if not wc_markets:
        print(f"No open WC markets found for round '{target_round}'. "
              f"Use --list-markets to see what's available.")
        return

    print(f"Processing {len(wc_markets)} market(s) for round={target_round or 'auto'}...\n")

    # -----------------------------------------------------------------------
    # 3-pick mode (default) vs --all-markets
    # -----------------------------------------------------------------------

    if args.all_markets:
        print("All-markets mode: trading all above edge threshold.\n")
        traded = 0
        for m in wc_markets:
            recipe, pos, expected, desc = strategy_for_market(m)
            if recipe is None:
                print(f"[SKIP] [{m['market_id']}] {m.get('title', '')[:55]} — {desc}")
                continue
            cmean  = FSClient.consensus_mean(m)
            mnorm  = recipe_mean_norm(recipe, m)
            edge   = abs(mnorm - FSClient.normalize(cmean, m))
            if edge < MIN_EDGE:
                print(f"[SKIP] [{m['market_id']}] {m.get('title', '')[:55]} — edge {edge*100:.1f}% < {MIN_EDGE*100:.1f}%")
                continue
            if _execute_trade(client, m, recipe, expected, desc, dry_run, USERNAME, PASSWORD):
                traded += 1
        print(f"\nDone. Trades executed: {traded}/{len(wc_markets)}")
        return

    # 3-pick mode: best 1 per position by edge
    print("3-pick mode: finding best FWD / MID / DEF...\n")

    # candidate: {edge, market, recipe, expected_pts, desc}
    candidates: dict[str, dict] = {}
    skipped: list[str] = []

    for m in wc_markets:
        recipe, pos, expected, desc = strategy_for_market(m)
        if recipe is None or pos not in COMP_POSITIONS:
            skipped.append(f"[{m['market_id']}] {m.get('title','')[:40]} — {desc}")
            continue

        cmean  = FSClient.consensus_mean(m)
        mnorm  = recipe_mean_norm(recipe, m)
        edge   = abs(mnorm - FSClient.normalize(cmean, m))

        if pos not in candidates or edge > candidates[pos]["edge"]:
            candidates[pos] = {
                "edge": edge, "market": m, "recipe": recipe,
                "expected_pts": expected, "desc": desc,
            }

    if skipped:
        print(f"  ({len(skipped)} markets skipped — no strategy or position out of scope)")

    traded = 0
    for pos in COMP_POSITIONS:
        if pos not in candidates:
            print(f"[{pos}] No candidate found — add more players to player_data.json "
                  f"or check market titles\n")
            continue

        c = candidates[pos]
        print(f"[{pos}] Best pick  edge={c['edge']*100:.1f}%")
        if _execute_trade(
            client, c["market"], c["recipe"], c["expected_pts"], c["desc"],
            dry_run, USERNAME, PASSWORD,
        ):
            traded += 1

    print(f"\nDone. Picks selected: {len(candidates)}/3  Trades executed: {traded}/3")

    if len(candidates) < 3:
        missing = [p for p in COMP_POSITIONS if p not in candidates]
        print(f"WARNING: Missing positions: {', '.join(missing)}")
        print("  → Expand player_data.json to cover these positions, "
              "or markets for those positions haven't opened yet.")


if __name__ == "__main__":
    main()
