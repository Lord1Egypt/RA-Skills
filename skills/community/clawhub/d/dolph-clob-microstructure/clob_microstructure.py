#!/usr/bin/env python3
"""
CLOB Microstructure Scanner - Polymarket order book analysis for structural alpha.

Analyzes order book microstructure across active Polymarket markets, scoring each
on liquidity gaps, imbalance, whale activity, and fake breakout patterns.
Trades MEAN_REVERT (fade) signals via SimmerClient.

Author: Mibayy
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone, timedelta

import requests
from simmer_sdk import SimmerClient

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SKILL_SLUG = "polymarket-clob-microstructure"
TRADE_SOURCE = "sdk:polymarket-clob-microstructure"

_client = None
def get_client():
    global _client
    if _client is None:
        _client = SimmerClient(
            api_key=os.environ["SIMMER_API_KEY"],
            venue=os.environ.get("TRADING_VENUE", "sim")
        )
    return _client


def check_context(client, market_id, my_probability=None):
    """Check market context before trading (flip-flop, slippage, edge)."""
    try:
        params = {}
        if my_probability is not None:
            params["my_probability"] = my_probability
        ctx = client.get_market_context(market_id, **params)
        trading = ctx.get("trading", {})
        flip_flop = trading.get("flip_flop_warning")
        if flip_flop and "SEVERE" in flip_flop:
            return False, f"flip-flop: {flip_flop}"
        slippage = ctx.get("slippage", {})
        if slippage.get("slippage_pct", 0) > 0.15:
            return False, "slippage too high"
        edge = ctx.get("edge_analysis", {})
        if edge.get("recommendation") == "HOLD":
            return False, "edge below threshold"
        return True, "ok"
    except Exception:
        return True, "context unavailable"


CLOB_BOOK_URL = "https://clob.polymarket.com/book"
TRADES_URL = "https://data-api.polymarket.com/trades"

# Scoring thresholds
LIQUIDITY_GAP_THRESHOLD = float(os.environ.get('CLOB_LIQUIDITY_GAP', '0.03'))
IMBALANCE_THRESHOLD = float(os.environ.get('CLOB_IMBALANCE_THRESHOLD', '0.65'))
WHALE_ORDER_RATIO = 0.25            # single order > 25% of side depth
FAKE_BREAKOUT_REVERT_PCT = 0.04     # 4% revert after spike = fake breakout

# Trade parameters
MIN_INEFFICIENCY_SCORE = 60         # minimum score to consider trading
MEAN_REVERT_MIN_SCORE = 75          # raised from 70 - be more selective
MAX_POSITION_USD = 25.0             # max per-trade size
FADE_SIZE_USD = float(os.environ.get('CLOB_TRADE_SIZE', '10.0'))  # reduced from 15

MARKETS_TO_SCAN = int(os.environ.get('CLOB_MARKETS_TO_SCAN', '30'))

# Safety filters
MIN_TIME_TO_EXPIRY_HOURS = float(os.environ.get('CLOB_MIN_HOURS_TO_EXPIRY', '2.0'))
PRICE_FLOOR = 0.10   # skip markets where mid < 10% (basically resolved NO)
PRICE_CEILING = 0.90  # skip markets where mid > 90% (basically resolved YES)
MAX_TRADES_PER_RUN = int(os.environ.get('CLOB_MAX_TRADES', '3'))

# Market types to skip (no microstructure edge on coin-flips or ultra-short)
SKIP_PATTERNS = [
    "odd/even",
    "total rounds",
    "total kills",
    "handicap",
    "o/u 2.5",
    "o/u 3.5",
    "o/u 162",
    "o/u 1.5",
]

log = logging.getLogger(SKILL_SLUG)


# ---------------------------------------------------------------------------
# Market filtering
# ---------------------------------------------------------------------------
def should_skip_market(question: str, mid: float, resolves_at: str | None) -> str | None:
    """Return skip reason or None if market is tradeable."""
    q_lower = question.lower()

    # Skip coin-flip / pure-random markets
    for pattern in SKIP_PATTERNS:
        if pattern in q_lower:
            return f"skip pattern: {pattern}"

    # Skip near-resolved prices
    if mid < PRICE_FLOOR:
        return f"price too low ({mid:.3f})"
    if mid > PRICE_CEILING:
        return f"price too high ({mid:.3f})"

    # Skip near-expiry markets
    if resolves_at:
        try:
            expiry = datetime.fromisoformat(resolves_at.replace("Z", "+00:00"))
            hours_left = (expiry - datetime.now(timezone.utc)).total_seconds() / 3600
            if hours_left < MIN_TIME_TO_EXPIRY_HOURS:
                return f"expires in {hours_left:.1f}h"
        except (ValueError, TypeError):
            pass

    return None


# ---------------------------------------------------------------------------
# Order book fetching
# ---------------------------------------------------------------------------
def fetch_order_book(token_id: str) -> dict | None:
    """Fetch raw order book from Polymarket CLOB."""
    try:
        resp = requests.get(CLOB_BOOK_URL, params={"token_id": token_id}, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        log.debug("Failed to fetch book for %s: %s", token_id, e)
        return None


def fetch_recent_trades(token_id: str, limit: int = 50) -> list:
    """Fetch recent trades from Polymarket data API."""
    try:
        resp = requests.get(
            TRADES_URL,
            params={"asset_id": token_id, "limit": limit},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json() if isinstance(resp.json(), list) else []
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Scoring functions (each returns 0-25)
# ---------------------------------------------------------------------------
def score_liquidity_gaps(bids: list, asks: list) -> tuple[float, str]:
    """Score based on price gaps in the order book."""
    if len(bids) < 2 and len(asks) < 2:
        return 0.0, "insufficient depth"

    max_gap = 0.0
    gap_location = "none"

    for side, name in [(bids, "bid"), (asks, "ask")]:
        prices = sorted([float(o["price"]) for o in side], reverse=(name == "bid"))
        for i in range(1, len(prices)):
            gap = abs(prices[i] - prices[i - 1])
            if gap > max_gap:
                max_gap = gap
                gap_location = f"{name}@{prices[i-1]:.2f}"

    if max_gap < LIQUIDITY_GAP_THRESHOLD:
        return 5.0, f"tight book, max_gap={max_gap:.3f}"

    score = min(25.0, (max_gap / LIQUIDITY_GAP_THRESHOLD) * 12.5)
    return score, f"gap={max_gap:.3f} at {gap_location}"


def score_imbalance(bids: list, asks: list) -> tuple[float, str]:
    """Score bid/ask volume imbalance."""
    bid_vol = sum(float(o.get("size", 0)) for o in bids)
    ask_vol = sum(float(o.get("size", 0)) for o in asks)
    total = bid_vol + ask_vol

    if total < 1.0:
        return 0.0, "no volume"

    ratio = max(bid_vol, ask_vol) / total
    if ratio < IMBALANCE_THRESHOLD:
        return 5.0, f"balanced {ratio:.2f}"

    score = min(25.0, ((ratio - 0.5) / 0.5) * 25.0)
    heavier = "bid" if bid_vol > ask_vol else "ask"
    return score, f"{heavier}-heavy {ratio:.2f} (b={bid_vol:.0f}/a={ask_vol:.0f})"


def score_whale_activity(bids: list, asks: list) -> tuple[float, str]:
    """Score presence of whale-sized orders."""
    max_ratio = 0.0
    whale_detail = "none"

    for side, name in [(bids, "bid"), (asks, "ask")]:
        if not side:
            continue
        sizes = [float(o.get("size", 0)) for o in side]
        total = sum(sizes)
        if total < 1.0:
            continue
        biggest = max(sizes)
        ratio = biggest / total
        if ratio > max_ratio:
            max_ratio = ratio
            whale_detail = f"{name} whale {ratio:.1%} of depth"

    if max_ratio < WHALE_ORDER_RATIO:
        return 3.0, "no whales"

    score = min(25.0, (max_ratio / WHALE_ORDER_RATIO) * 12.5)
    return score, whale_detail


def score_fake_breakout(trades: list, current_mid: float) -> tuple[float, str]:
    """Detect fake breakouts from recent trade history."""
    if len(trades) < 10 or current_mid <= 0:
        return 0.0, "insufficient trade history"

    prices = []
    for t in trades[:30]:
        p = float(t.get("price", 0))
        if p > 0:
            prices.append(p)

    if len(prices) < 10:
        return 0.0, "no valid prices"

    recent_high = max(prices[:5])
    recent_low = min(prices[:5])
    older_mean = sum(prices[10:]) / max(len(prices[10:]), 1) if len(prices) > 10 else current_mid

    spike_up = recent_high - older_mean
    spike_down = older_mean - recent_low
    max_spike = max(spike_up, spike_down)

    revert = abs(current_mid - (older_mean + max_spike if spike_up > spike_down else older_mean - max_spike))

    if max_spike < FAKE_BREAKOUT_REVERT_PCT:
        return 2.0, "no spike detected"

    if revert > max_spike * 0.5:
        score = min(25.0, (revert / max_spike) * 25.0)
        direction = "up" if spike_up > spike_down else "down"
        return score, f"fake breakout {direction}, spike={max_spike:.3f} revert={revert:.3f}"

    return 5.0, f"spike={max_spike:.3f} but not reverting yet"


# ---------------------------------------------------------------------------
# Signal generation
# ---------------------------------------------------------------------------
def generate_signal(total_score: float, components: dict) -> str:
    """Map inefficiency score to trading signal."""
    fake_score = components.get("fake_breakout", (0, ""))[0]

    if fake_score >= 15 and total_score >= MEAN_REVERT_MIN_SCORE:
        return "MEAN_REVERT"
    if total_score >= MIN_INEFFICIENCY_SCORE:
        return "REDUCE_SIZE"
    if total_score >= 40:
        return "ENTRY_OK"
    return "SKIP"


def get_mid_price(bids: list, asks: list) -> float:
    """Calculate mid price from order book."""
    best_bid = max((float(o["price"]) for o in bids), default=0)
    best_ask = min((float(o["price"]) for o in asks), default=1)
    if best_bid <= 0 or best_ask >= 1:
        return 0.5
    return (best_bid + best_ask) / 2


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------
def run(live: bool = False, quiet: bool = False):
    """Main scan and trade loop."""
    client = get_client()

    # Discover active markets
    log.info("Fetching active markets...")
    try:
        markets = client.get_markets(limit=MARKETS_TO_SCAN, status="active")
    except Exception as e:
        log.error("Failed to fetch markets: %s", e)
        return

    if not markets:
        log.warning("No active markets found")
        return

    log.info("Scanning %d markets for microstructure signals...", len(markets))
    signals = []
    skipped = {"pattern": 0, "price": 0, "expiry": 0, "no_token": 0, "no_book": 0}

    for market in markets:
        market_id = market.id
        question = market.question

        # Use polymarket_token_id (YES outcome typically)
        token_id = market.polymarket_token_id
        if not token_id:
            skipped["no_token"] += 1
            continue

        # Fetch order book
        book = fetch_order_book(token_id)
        if not book:
            skipped["no_book"] += 1
            continue

        bids = book.get("bids", [])
        asks = book.get("asks", [])

        if len(bids) < 2 or len(asks) < 2:
            skipped["no_book"] += 1
            continue

        mid = get_mid_price(bids, asks)

        # Apply safety filters BEFORE scoring
        skip_reason = should_skip_market(question, mid, market.resolves_at)
        if skip_reason:
            category = "pattern" if "skip pattern" in skip_reason else (
                "price" if "price" in skip_reason else "expiry"
            )
            skipped[category] += 1
            log.debug("SKIP %s: %s", skip_reason, question[:50])
            continue

        # Fetch recent trades
        trades = fetch_recent_trades(token_id)

        # Score all dimensions
        components = {
            "liquidity_gaps": score_liquidity_gaps(bids, asks),
            "imbalance": score_imbalance(bids, asks),
            "whale_activity": score_whale_activity(bids, asks),
            "fake_breakout": score_fake_breakout(trades, mid),
        }

        total = sum(v[0] for v in components.values())
        signal = generate_signal(total, components)

        if signal != "SKIP":
            signals.append({
                "market_id": market_id,
                "question": question,
                "token_id": token_id,
                "mid": mid,
                "score": total,
                "signal": signal,
                "components": {k: {"score": v[0], "detail": v[1]} for k, v in components.items()},
            })

        log.debug("[%s] score=%.0f signal=%s mid=%.3f q=%s", signal, total, signal, mid, question[:60])
        time.sleep(0.3)  # rate limiting

    # Report
    log.info(
        "Scan: %d markets, %d signals, skipped: %s",
        len(markets), len(signals),
        ", ".join(f"{k}={v}" for k, v in skipped.items() if v > 0)
    )

    # Trade MEAN_REVERT signals only, sorted by score (best first)
    mean_revert = sorted(
        [s for s in signals if s["signal"] == "MEAN_REVERT"],
        key=lambda s: s["score"],
        reverse=True,
    )

    if not mean_revert:
        log.info("No MEAN_REVERT signals - nothing to trade")
        return

    trades_placed = 0
    for sig in mean_revert:
        if trades_placed >= MAX_TRADES_PER_RUN:
            log.info("Max trades per run (%d) reached", MAX_TRADES_PER_RUN)
            break

        mid = sig["mid"]
        # Fade direction: if book is bid-heavy, sell (price will drop); ask-heavy, buy
        imb_detail = sig["components"]["imbalance"]["detail"]
        if "bid-heavy" in imb_detail:
            side = "no"
        else:
            side = "yes"

        # Dynamic sizing: smaller on lower-conviction scores
        size = FADE_SIZE_USD
        if sig["score"] < 80:
            size = FADE_SIZE_USD * 0.6  # reduce for weaker signals

        reasoning = (
            f"MEAN_REVERT fade: inefficiency_score={sig['score']:.0f}/100. "
            f"Fake breakout detected ({sig['components']['fake_breakout']['detail']}). "
            f"Imbalance: {imb_detail}. "
            f"Fading {side.lower()} at mid={mid:.3f}."
        )

        log.info("TRADE: %s $%.0f %s @ ~%.3f - %s", side, size, sig["question"][:50], mid, reasoning)

        ok, reason = check_context(client, sig["market_id"])
        if not ok:
            log.warning("Skipping trade: %s", reason)
            continue

        if live:
            try:
                result = client.trade(
                    market_id=sig["market_id"],
                    side=side,
                    amount=size,
                    source=TRADE_SOURCE,
                    skill_slug=SKILL_SLUG,
                    reasoning=reasoning,
                )
                log.info("Order placed: %s", json.dumps(result, default=str)[:200])
                trades_placed += 1
            except Exception as e:
                log.error("Order failed for %s: %s", sig["market_id"], e)
        else:
            log.info("[DRY RUN] Would %s $%.0f on %s", side, size, sig["question"][:50])
            trades_placed += 1

    if not quiet:
        print(f"\n{'='*60}")
        print(f"CLOB Microstructure Scan Complete - {datetime.now(timezone.utc).isoformat()}")
        print(f"Markets scanned: {len(markets)}")
        print(f"Actionable signals: {len(signals)}")
        print(f"MEAN_REVERT trades: {trades_placed}")
        print(f"Mode: {'LIVE' if live else 'DRY RUN'}")
        print(f"{'='*60}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="CLOB Microstructure Scanner")
    parser.add_argument("--live", action="store_true", help="Execute real trades (default: dry run)")
    parser.add_argument("--quiet", action="store_true", help="Suppress summary output (for cron)")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    level = logging.DEBUG if args.debug else (logging.WARNING if args.quiet else logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    if not os.environ.get("SIMMER_API_KEY"):
        log.error("SIMMER_API_KEY not set")
        sys.exit(1)

    try:
        run(live=args.live, quiet=args.quiet)
    except KeyboardInterrupt:
        log.info("Interrupted")
    except Exception as e:
        log.error("Fatal: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
