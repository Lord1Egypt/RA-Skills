#!/usr/bin/env python3
"""
Crypto Funding Rate Harvester
==============================
ClawHub Skill — type: automaton | cron: */15 * * * *

Scans perpetual futures funding rates across Hyperliquid, Binance, and Bybit.
Identifies delta-neutral carry trade opportunities where funding is high enough
to profit by going long spot + short perp (collecting funding with no directional risk).

All APIs are free and public — no authentication required.

Output: /tmp/funding_opportunities.json
"""

import os
import json
import logging
from datetime import datetime, timezone

import requests

# ---------------------------------------------------------------------------
# Configuration (overridable via environment variables)
# ---------------------------------------------------------------------------

# Minimum annualized funding rate (%) to be considered an opportunity
MIN_ANNUALIZED_PCT = float(os.environ.get("MIN_ANNUALIZED_PCT", "20"))

# Minimum spread (%) between Binance and Bybit funding to flag cross-exchange arb
CROSS_EXCHANGE_SPREAD_THRESHOLD = float(
    os.environ.get("CROSS_EXCHANGE_SPREAD_THRESHOLD", "10")
)

# HTTP request timeout in seconds
REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", "10"))

# Output file path
OUTPUT_PATH = "/tmp/funding_opportunities.json"

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
log = logging.getLogger("funding-harvester")


# ---------------------------------------------------------------------------
# Funding rate normalisation
# ---------------------------------------------------------------------------

def annualize(funding_rate_8h: float) -> float:
    """
    Convert an 8-hour funding rate to an annualized percentage.

    There are 3 funding periods per day (every 8 hours), so:
        annualized = rate_8h * 3 * 365 * 100
    """
    return funding_rate_8h * 3 * 365 * 100


# ---------------------------------------------------------------------------
# Exchange fetchers
# ---------------------------------------------------------------------------

def fetch_hyperliquid() -> list[dict]:
    """
    Fetch funding rates from Hyperliquid via the /info endpoint.

    Uses POST with {"type": "metaAndAssetCtxs"} which returns metadata about
    all listed assets alongside live market context (including funding rates).

    Returns a list of dicts with keys:
        asset, exchange, funding_rate_8h, annualized_pct, current_price
    """
    url = "https://api.hyperliquid.xyz/info"
    payload = {"type": "metaAndAssetCtxs"}

    log.info("Fetching Hyperliquid funding rates...")
    try:
        resp = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        log.error("Hyperliquid request failed: %s", e)
        return []
    except json.JSONDecodeError as e:
        log.error("Hyperliquid response parse error: %s", e)
        return []

    # Response is a 2-element list: [meta, asset_contexts]
    # meta["universe"] is a list of asset metadata dicts (each has "name")
    # asset_contexts is a parallel list of live market data dicts
    try:
        meta_list = data[0]["universe"]   # list of {name, szDecimals, ...}
        ctx_list = data[1]                # list of {funding, markPx, ...}
    except (IndexError, KeyError, TypeError) as e:
        log.error("Unexpected Hyperliquid response structure: %s", e)
        return []

    results = []
    for meta, ctx in zip(meta_list, ctx_list):
        try:
            asset = meta["name"]
            # Hyperliquid returns funding as a decimal per 8h period (e.g. 0.0001)
            funding_8h = float(ctx.get("funding", 0))
            mark_price = float(ctx.get("markPx", 0))

            if mark_price <= 0:
                continue  # Skip assets with no price data

            ann = annualize(funding_8h)

            results.append({
                "asset": asset,
                "exchange": "hyperliquid",
                "funding_rate_8h": funding_8h,
                "annualized_pct": round(ann, 4),
                "current_price": mark_price,
            })
        except (KeyError, ValueError, TypeError) as e:
            log.debug("Skipping Hyperliquid asset due to parse error: %s", e)
            continue

    log.info("Hyperliquid: fetched %d assets", len(results))
    return results


def fetch_binance() -> list[dict]:
    """
    Fetch funding rates from Binance USDT-Margined Futures via premiumIndex.

    Endpoint: GET https://fapi.binance.com/fapi/v1/premiumIndex
    Returns all active perpetual contracts with their current funding rates.

    We only keep USDT-settled pairs (symbol ends with USDT) to avoid
    mixing in coin-margined contracts or quarterly futures.

    Returns a list of dicts with keys:
        asset, exchange, funding_rate_8h, annualized_pct, current_price
    """
    url = "https://fapi.binance.com/fapi/v1/premiumIndex"

    log.info("Fetching Binance funding rates...")
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        log.error("Binance request failed: %s", e)
        return []
    except json.JSONDecodeError as e:
        log.error("Binance response parse error: %s", e)
        return []

    results = []
    for item in data:
        try:
            symbol = item.get("symbol", "")

            # Only process USDT-settled perps (skip BUSD pairs, coin-margined, etc.)
            if not symbol.endswith("USDT"):
                continue

            # Strip the USDT suffix to get the base asset name (e.g. BTCUSDT -> BTC)
            asset = symbol[:-4]

            funding_8h = float(item.get("lastFundingRate", 0))
            mark_price = float(item.get("markPrice", 0))

            if mark_price <= 0:
                continue

            ann = annualize(funding_8h)

            results.append({
                "asset": asset,
                "exchange": "binance",
                "funding_rate_8h": funding_8h,
                "annualized_pct": round(ann, 4),
                "current_price": mark_price,
            })
        except (KeyError, ValueError, TypeError) as e:
            log.debug("Skipping Binance symbol %s due to parse error: %s", symbol, e)
            continue

    log.info("Binance: fetched %d assets", len(results))
    return results


def fetch_bybit() -> list[dict]:
    """
    Fetch funding rates from Bybit linear (USDT-settled) perpetuals.

    Endpoint: GET https://api.bybit.com/v5/market/tickers?category=linear
    Returns tickers for all linear perpetual contracts including funding rate.

    We filter to USDT-settled pairs only (symbol ends with USDT).

    Returns a list of dicts with keys:
        asset, exchange, funding_rate_8h, annualized_pct, current_price
    """
    url = "https://api.bybit.com/v5/market/tickers"
    params = {"category": "linear"}

    log.info("Fetching Bybit funding rates...")
    try:
        resp = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        log.error("Bybit request failed: %s", e)
        return []
    except json.JSONDecodeError as e:
        log.error("Bybit response parse error: %s", e)
        return []

    # Bybit wraps results in: {"result": {"list": [...]}}
    try:
        tickers = data["result"]["list"]
    except (KeyError, TypeError) as e:
        log.error("Unexpected Bybit response structure: %s", e)
        return []

    results = []
    for item in tickers:
        try:
            symbol = item.get("symbol", "")

            # Only process USDT-settled perps (skip USDC pairs, inverse contracts, etc.)
            if not symbol.endswith("USDT"):
                continue

            asset = symbol[:-4]

            funding_8h = float(item.get("fundingRate", 0))
            mark_price = float(item.get("markPrice", 0))

            if mark_price <= 0:
                continue

            ann = annualize(funding_8h)

            results.append({
                "asset": asset,
                "exchange": "bybit",
                "funding_rate_8h": funding_8h,
                "annualized_pct": round(ann, 4),
                "current_price": mark_price,
            })
        except (KeyError, ValueError, TypeError) as e:
            log.debug("Skipping Bybit symbol %s due to parse error: %s", symbol, e)
            continue

    log.info("Bybit: fetched %d assets", len(results))
    return results


# ---------------------------------------------------------------------------
# Opportunity filtering and ranking
# ---------------------------------------------------------------------------

def filter_opportunities(all_rates: list[dict]) -> list[dict]:
    """
    Filter funding rate data to only include carry trade opportunities.

    Criteria:
    1. Positive funding rate — longs pay shorts, so shorting the perp collects funding.
       Negative funding means shorts pay longs (not profitable for this strategy).
    2. Annualized rate > MIN_ANNUALIZED_PCT — must be worth the transaction costs.

    Returns filtered list sorted by annualized_pct descending (best first).
    """
    opportunities = [
        r for r in all_rates
        if r["funding_rate_8h"] > 0 and r["annualized_pct"] > MIN_ANNUALIZED_PCT
    ]

    # Rank by annualized rate, highest first
    opportunities.sort(key=lambda x: x["annualized_pct"], reverse=True)

    log.info(
        "Filtered to %d opportunities (min %.1f%% annualized, positive funding only)",
        len(opportunities),
        MIN_ANNUALIZED_PCT,
    )
    return opportunities


# ---------------------------------------------------------------------------
# Cross-exchange spread detection
# ---------------------------------------------------------------------------

def detect_cross_exchange_spreads(all_rates: list[dict]) -> list[dict]:
    """
    Detect assets where Binance funding rate is significantly higher than Bybit.

    A large spread between exchanges suggests a potential cross-exchange arbitrage:
    - Short the perp on the high-funding exchange (Binance) — collect high funding
    - Long the perp on the low-funding exchange (Bybit) — pay low funding
    - Net yield = spread between the two rates
    - This eliminates even the need for spot exposure

    Only flags pairs where:
    - Both exchanges list the asset
    - Spread >= CROSS_EXCHANGE_SPREAD_THRESHOLD
    - Binance rate is higher than Bybit (directional — Binance as primary)

    Returns a list of spread dicts, sorted by spread descending.
    """
    # Index rates by (asset, exchange) for quick lookup
    binance_rates = {
        r["asset"]: r for r in all_rates if r["exchange"] == "binance"
    }
    bybit_rates = {
        r["asset"]: r for r in all_rates if r["exchange"] == "bybit"
    }

    spreads = []
    for asset in set(binance_rates.keys()) & set(bybit_rates.keys()):
        b_ann = binance_rates[asset]["annualized_pct"]
        bb_ann = bybit_rates[asset]["annualized_pct"]
        spread = b_ann - bb_ann

        if spread >= CROSS_EXCHANGE_SPREAD_THRESHOLD:
            spreads.append({
                "asset": asset,
                "binance_annualized_pct": round(b_ann, 4),
                "bybit_annualized_pct": round(bb_ann, 4),
                "spread_pct": round(spread, 4),
                "note": (
                    f"Binance funding significantly higher than Bybit — "
                    f"potential cross-exchange arb (short Binance perp, long Bybit perp)"
                ),
            })

    spreads.sort(key=lambda x: x["spread_pct"], reverse=True)

    log.info(
        "Detected %d cross-exchange spreads (Binance vs Bybit, threshold %.1f%%)",
        len(spreads),
        CROSS_EXCHANGE_SPREAD_THRESHOLD,
    )
    return spreads


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    log.info("=== Crypto Funding Rate Harvester starting ===")
    log.info(
        "Config: min_annualized=%.1f%%, spread_threshold=%.1f%%, timeout=%ds",
        MIN_ANNUALIZED_PCT,
        CROSS_EXCHANGE_SPREAD_THRESHOLD,
        REQUEST_TIMEOUT,
    )

    # 1. Fetch raw funding rate data from all exchanges
    all_rates = []
    all_rates.extend(fetch_hyperliquid())
    all_rates.extend(fetch_binance())
    all_rates.extend(fetch_bybit())

    log.info("Total assets fetched across all exchanges: %d", len(all_rates))

    if not all_rates:
        log.warning("No data fetched from any exchange. Check connectivity.")

    # 2. Filter to profitable opportunities and rank by annualized rate
    opportunities = filter_opportunities(all_rates)

    # 3. Detect cross-exchange funding spread opportunities
    spreads = detect_cross_exchange_spreads(all_rates)

    # 4. Build output payload
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "opportunities": opportunities,
        "cross_exchange_spreads": spreads,
        "summary": {
            "total_opportunities": len(opportunities),
            "total_assets_scanned": len(all_rates),
            "exchanges_scanned": ["hyperliquid", "binance", "bybit"],
            "min_annualized_threshold_pct": MIN_ANNUALIZED_PCT,
            "cross_exchange_spread_threshold_pct": CROSS_EXCHANGE_SPREAD_THRESHOLD,
        },
    }

    # 5. Save to output file
    try:
        with open(OUTPUT_PATH, "w") as f:
            json.dump(output, f, indent=2)
        log.info("Results saved to %s", OUTPUT_PATH)
    except OSError as e:
        log.error("Failed to write output file: %s", e)

    # 6. Print summary to stdout
    log.info("=== Summary ===")
    log.info("Opportunities found: %d", len(opportunities))
    log.info("Cross-exchange spreads detected: %d", len(spreads))

    if opportunities:
        top = opportunities[0]
        log.info(
            "Top opportunity: %s on %s — %.2f%% annualized (%.6f per 8h) @ $%.2f",
            top["asset"],
            top["exchange"],
            top["annualized_pct"],
            top["funding_rate_8h"],
            top["current_price"],
        )

    if spreads:
        top_spread = spreads[0]
        log.info(
            "Top cross-exchange spread: %s — Binance %.2f%% vs Bybit %.2f%% (spread %.2f%%)",
            top_spread["asset"],
            top_spread["binance_annualized_pct"],
            top_spread["bybit_annualized_pct"],
            top_spread["spread_pct"],
        )

    log.info("=== Done ===")


if __name__ == "__main__":
    main()
