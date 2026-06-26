#!/usr/bin/env python3
"""
Polymarket Market Maker - Places GTC limit orders on both sides of liquid markets.

Usage:
    python market_maker.py              # Dry run
    python market_maker.py --live       # Real trades
    python market_maker.py --positions  # Show positions
    python market_maker.py --config     # Show config
    python market_maker.py --set KEY=VALUE  # Set config value

Requires:
    SIMMER_API_KEY environment variable
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# Force line-buffered stdout (required for cron/Docker/OpenClaw visibility)
sys.stdout.reconfigure(line_buffering=True)

# ---------------------------------------------------------------------------
# Config System
# ---------------------------------------------------------------------------
from simmer_sdk.skill import load_config, update_config, get_config_path

SKILL_SLUG = "simmer-market-maker"

CONFIG_SCHEMA = {
    "max_order_usd":          {"env": "SIMMER_MM_MAX_ORDER_USD",         "default": 5.0,    "type": float},
    "max_markets":            {"env": "SIMMER_MM_MAX_MARKETS",           "default": 3,      "type": int},
    "min_vol_24h":            {"env": "SIMMER_MM_MIN_VOL_24H",           "default": 10000,  "type": float},
    "spread_offset":          {"env": "SIMMER_MM_SPREAD_OFFSET",         "default": 0.02,   "type": float},
    "min_price":              {"env": "SIMMER_MM_MIN_PRICE",             "default": 0.15,   "type": float},
    "max_price":              {"env": "SIMMER_MM_MAX_PRICE",             "default": 0.85,   "type": float},
    "min_hours_to_resolve":   {"env": "SIMMER_MM_MIN_HOURS_TO_RESOLVE",  "default": 4,      "type": float},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug=SKILL_SLUG)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
TRADE_SOURCE = "sdk:marketmaker"

MIN_SHARES_PER_ORDER = 5.0
MIN_TICK_SIZE = 0.01
SLIPPAGE_MAX_PCT = 0.15

CLOB_BASE = "https://clob.polymarket.com"

# Unpack config to module-level
MAX_ORDER_USD         = _config["max_order_usd"]
MAX_MARKETS           = _config["max_markets"]
MIN_VOL_24H           = _config["min_vol_24h"]
SPREAD_OFFSET         = _config["spread_offset"]
MIN_PRICE             = _config["min_price"]
MAX_PRICE             = _config["max_price"]
MIN_HOURS_TO_RESOLVE  = _config["min_hours_to_resolve"]

# ---------------------------------------------------------------------------
# SimmerClient singleton
# ---------------------------------------------------------------------------
_client = None

def get_client(live=True):
    """Lazy-init SimmerClient singleton."""
    global _client
    if _client is None:
        try:
            from simmer_sdk import SimmerClient
        except ImportError:
            print("Error: simmer-sdk not installed. Run: pip install simmer-sdk")
            sys.exit(1)
        api_key = os.environ.get("SIMMER_API_KEY")
        if not api_key:
            print("Error: SIMMER_API_KEY environment variable not set")
            print("Get your API key from: simmer.markets/dashboard -> SDK tab")
            sys.exit(1)
        venue = os.environ.get("TRADING_VENUE", "polymarket")
        _client = SimmerClient(api_key=api_key, venue=venue, live=live)
    return _client


# ---------------------------------------------------------------------------
# SDK Wrappers
# ---------------------------------------------------------------------------
def get_portfolio():
    try:
        return get_client().get_portfolio()
    except Exception as e:
        print(f"  Portfolio fetch failed: {e}")
        return None


def get_positions():
    try:
        client = get_client()
        positions = client.get_positions(venue=client.venue)
        from dataclasses import asdict
        return [asdict(p) for p in positions]
    except Exception as e:
        print(f"  Error fetching positions: {e}")
        return []


def get_market_context(market_id):
    try:
        return get_client().get_market_context(market_id)
    except Exception:
        return None


def check_context_safeguards(context):
    """Check context for deal-breakers. Returns (should_trade, reasons)."""
    if not context:
        return True, []

    reasons = []
    warnings = context.get("warnings", [])
    discipline = context.get("discipline", {})
    slippage = context.get("slippage", {})

    for warning in warnings:
        if "MARKET RESOLVED" in str(warning).upper():
            return False, ["Market already resolved"]

    warning_level = discipline.get("warning_level", "none")
    if warning_level == "severe":
        return False, [f"Severe flip-flop warning: {discipline.get('flip_flop_warning', '')}"]
    elif warning_level == "mild":
        reasons.append("Mild flip-flop warning (proceed with caution)")

    estimates = slippage.get("estimates", []) if slippage else []
    if estimates:
        slippage_pct = estimates[0].get("slippage_pct", 0)
        if slippage_pct > SLIPPAGE_MAX_PCT:
            return False, [f"Slippage too high: {slippage_pct:.1%}"]

    return True, reasons


def execute_limit_order(market_id, side, amount, price, reasoning=""):
    """Place a GTC limit order via SimmerClient.trade()."""
    try:
        result = get_client().trade(
            market_id=market_id,
            side=side,
            amount=amount,
            order_type="GTC",
            price=price,
            source=TRADE_SOURCE,
            reasoning=reasoning,
        )
        return {
            "success": result.success,
            "trade_id": result.trade_id,
            "shares_bought": getattr(result, "shares_bought", None),
            "error": result.error,
            "simulated": result.simulated,
            "skip_reason": getattr(result, "skip_reason", None),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ---------------------------------------------------------------------------
# Market Data
# ---------------------------------------------------------------------------
def fetch_markets():
    """Fetch active markets from Simmer API sorted by volume."""
    try:
        result = get_client()._request("GET", "/api/sdk/markets", params={
            "status": "active",
            "sort": "volume",
            "limit": 200,
        })
        return result.get("markets", [])
    except Exception as e:
        print(f"  Failed to fetch markets: {e}")
        return []


def fetch_clob_midpoint(token_id):
    """Fetch live CLOB midpoint for a Polymarket token. Returns float or None."""
    if not token_id:
        return None
    url = f"{CLOB_BASE}/midpoint?token_id={token_id}"
    try:
        req = Request(url, headers={"User-Agent": "simmer-market-maker/1.0"})
        with urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            mid = data.get("mid")
            if mid is not None:
                return float(mid)
    except (HTTPError, URLError, json.JSONDecodeError, ValueError):
        pass
    return None


def cancel_open_orders(dry_run=True):
    """Cancel all existing open orders via DELETE /api/sdk/orders."""
    if dry_run:
        print("  [DRY RUN] Would cancel open orders")
        return True
    try:
        get_client()._request("DELETE", "/api/sdk/orders")
        print("  ✓ Cancelled existing open orders")
        return True
    except Exception as e:
        print(f"  Warning: Could not cancel orders: {e}")
        return False


def parse_resolves_at(resolves_at_str):
    """Parse resolves_at string to datetime. Returns None if unparseable."""
    if not resolves_at_str:
        return None
    try:
        # Try ISO format with Z suffix
        ts = resolves_at_str.replace("Z", "+00:00")
        return datetime.fromisoformat(ts)
    except (ValueError, AttributeError):
        pass
    try:
        # Try as unix timestamp
        return datetime.fromtimestamp(float(resolves_at_str), tz=timezone.utc)
    except (ValueError, TypeError):
        pass
    return None


# ---------------------------------------------------------------------------
# Main Strategy
# ---------------------------------------------------------------------------
def run_strategy(dry_run=True, positions_only=False, show_config=False,
                 use_safeguards=True):
    """Run the market making strategy."""
    print("📊 Polymarket Market Maker")
    print("=" * 55)

    # Validate API key early
    get_client(live=not dry_run)

    if dry_run:
        print("\n  [PAPER MODE] Use --live for real trades.\n")

    if show_config:
        print(f"  max_order_usd:        ${MAX_ORDER_USD:.2f}")
        print(f"  max_markets:          {MAX_MARKETS}")
        print(f"  min_vol_24h:          ${MIN_VOL_24H:,.0f}")
        print(f"  spread_offset:        {SPREAD_OFFSET:.3f} ({SPREAD_OFFSET*100:.1f}¢)")
        print(f"  min_price:            {MIN_PRICE}")
        print(f"  max_price:            {MAX_PRICE}")
        print(f"  min_hours_to_resolve: {MIN_HOURS_TO_RESOLVE}h")
        return

    if positions_only:
        print("\n📋 Open Positions")
        positions = get_positions()
        if not positions:
            print("  No positions found.")
        for p in positions:
            if p.get("status") != "active":
                continue
            print(f"  {p.get('question', 'N/A')[:60]}")
            print(f"    YES={p.get('shares_yes',0):.1f} NO={p.get('shares_no',0):.1f}  "
                  f"value=${p.get('current_value',0):.2f}  pnl=${p.get('pnl',0):.2f}")
        return

    # --- Strategy ---
    print(f"  Config: max_order=${MAX_ORDER_USD}  offset={SPREAD_OFFSET:.2f}  "
          f"vol_min=${MIN_VOL_24H:,.0f}  max_mkts={MAX_MARKETS}")
    print()

    markets = fetch_markets()
    print(f"  Fetched {len(markets)} active markets")

    now = datetime.now(timezone.utc)
    min_resolve_delta = timedelta(hours=MIN_HOURS_TO_RESOLVE)

    # Filter markets
    candidates = []
    for m in markets:
        # Skip paid markets (10% fee kills edge)
        if m.get("is_paid"):
            continue

        # Skip Kalshi markets (not supported for real trading via Simmer)
        if m.get("import_source") == "kalshi":
            continue

        # Volume filter
        vol = m.get("volume_24h", 0) or 0
        if vol < MIN_VOL_24H:
            continue

        # Price filter
        price = m.get("current_probability", 0.5) or 0.5
        if price < MIN_PRICE or price > MAX_PRICE:
            continue

        # Time-to-resolution filter
        resolves_at = parse_resolves_at(m.get("resolves_at"))
        if resolves_at:
            time_left = resolves_at - now
            if time_left < min_resolve_delta:
                continue
        # If no resolves_at, skip (we can't verify it has time left)
        else:
            continue

        candidates.append(m)

    print(f"  Candidates after filter: {len(candidates)}")

    if not candidates:
        print("\n  No qualifying markets found.")
        if os.environ.get("AUTOMATON_MANAGED"):
            print(json.dumps({"automaton": {
                "signals": 0, "trades_attempted": 0, "trades_executed": 0,
                "skip_reason": "no_qualifying_markets"
            }}))
        return

    # Sort by volume (descending) and cap
    candidates.sort(key=lambda m: m.get("volume_24h", 0), reverse=True)
    candidates = candidates[:MAX_MARKETS]

    print(f"  Trading top {len(candidates)} markets by volume\n")

    # Cancel existing open orders before placing new ones
    cancel_open_orders(dry_run=dry_run)
    print()

    signals_found = len(candidates)
    trades_attempted = 0
    trades_executed = 0
    skip_reasons = []
    execution_errors = []

    for i, market in enumerate(candidates, 1):
        market_id = market.get("id")
        question = market.get("question", "N/A")[:60]
        price = market.get("current_probability", 0.5)
        vol = market.get("volume_24h", 0)
        token_id = market.get("polymarket_token_id")

        print(f"  [{i}] {question}")
        print(f"      price={price:.3f}  vol_24h=${vol:,.0f}")

        # Fetch CLOB midpoint
        mid = fetch_clob_midpoint(token_id)
        if mid is None:
            print(f"      ⚠ Could not fetch CLOB midpoint — using Simmer price as fallback")
            mid = price
        else:
            print(f"      CLOB mid={mid:.3f}")

        # Calculate limit prices — round to 2 decimal places (Polymarket 0.01 tick size)
        POLY_FEE = 0.02
        yes_bid = round(max(mid - SPREAD_OFFSET, MIN_TICK_SIZE), 2)
        no_mid = 1.0 - mid
        no_bid = round(max(no_mid - SPREAD_OFFSET, MIN_TICK_SIZE), 2)

        # Net cost after fees (fee applies on fill)
        total_cost = yes_bid + no_bid
        fee_cost   = yes_bid * POLY_FEE + no_bid * POLY_FEE
        net_profit_pct = (1.0 - total_cost - fee_cost) * 100
        print(f"      YES limit @ {yes_bid:.2f}  |  NO limit @ {no_bid:.2f}")
        print(f"      Net profit if both fill: {net_profit_pct:.1f}% (cost={total_cost:.2f} + fees={fee_cost:.3f})")
        if total_cost + fee_cost >= 1.0:
            print(f"      ⚠ Skip: no edge after fees (total={total_cost + fee_cost:.3f} >= 1.00)")
            skip_reasons.append("no edge after fees")
            continue

        # Min shares check: need at least 5 shares, so bid must be <= max_order / 5
        if yes_bid > MAX_ORDER_USD / MIN_SHARES_PER_ORDER:
            reason = f"YES bid too high for min order at ${MAX_ORDER_USD}"
            print(f"      ⚠ Skip YES: {reason}")
            skip_reasons.append(reason)
        else:
            # Safeguards
            if use_safeguards:
                context = get_market_context(market_id)
                should_trade, reasons = check_context_safeguards(context)
                if not should_trade:
                    reason = "; ".join(reasons)
                    print(f"      🛡 Safeguard blocked YES: {reason}")
                    skip_reasons.append(reason)
                    print()
                    continue
                if reasons:
                    print(f"      ⚠ Safeguard warning: {'; '.join(reasons)}")

            reasoning = (
                f"Market making YES bid: mid={mid:.3f}, quoting {yes_bid:.2f} "
                f"({SPREAD_OFFSET:.2f} below mid), vol_24h=${vol:,.0f}"
            )

            if dry_run:
                print(f"      [DRY RUN] Would place YES GTC limit @ {yes_bid:.2f} for ${MAX_ORDER_USD}")
                trades_attempted += 1
                trades_executed += 1
            else:
                trades_attempted += 1
                result = execute_limit_order(market_id, "yes", MAX_ORDER_USD, yes_bid, reasoning)
                if result.get("success"):
                    trades_executed += 1
                    print(f"      ✓ YES limit placed @ {yes_bid:.2f}  id={result.get('trade_id')}")
                elif result.get("skip_reason"):
                    skip_reasons.append(result["skip_reason"])
                    print(f"      ⚠ YES skipped: {result['skip_reason']}")
                else:
                    err = result.get("error", "unknown error")
                    execution_errors.append(err)
                    print(f"      ✗ YES failed: {err}")

        # NO side
        if no_bid > MAX_ORDER_USD / MIN_SHARES_PER_ORDER:
            reason = f"NO bid too high for min order at ${MAX_ORDER_USD}"
            print(f"      ⚠ Skip NO: {reason}")
            skip_reasons.append(reason)
        else:
            reasoning = (
                f"Market making NO bid: mid(NO)={no_mid:.3f}, quoting {no_bid:.2f} "
                f"({SPREAD_OFFSET:.2f} below NO mid), vol_24h=${vol:,.0f}"
            )

            if dry_run:
                print(f"      [DRY RUN] Would place NO GTC limit @ {no_bid:.2f} for ${MAX_ORDER_USD}")
                trades_attempted += 1
                trades_executed += 1
            else:
                trades_attempted += 1
                result = execute_limit_order(market_id, "no", MAX_ORDER_USD, no_bid, reasoning)
                if result.get("success"):
                    trades_executed += 1
                    print(f"      ✓ NO  limit placed @ {no_bid:.2f}  id={result.get('trade_id')}")
                elif result.get("skip_reason"):
                    skip_reasons.append(result["skip_reason"])
                    print(f"      ⚠ NO  skipped: {result['skip_reason']}")
                else:
                    err = result.get("error", "unknown error")
                    execution_errors.append(err)
                    print(f"      ✗ NO  failed: {err}")

        print()

    # Summary
    print("=" * 55)
    print(f"  Summary: {signals_found} signals  |  "
          f"{trades_attempted} attempted  |  {trades_executed} executed")
    if skip_reasons:
        unique_skips = list(dict.fromkeys(skip_reasons))
        print(f"  Skips: {', '.join(unique_skips)}")
    if execution_errors:
        print(f"  Errors: {'; '.join(execution_errors)}")

    # Automaton report
    if os.environ.get("AUTOMATON_MANAGED"):
        report = {
            "signals": signals_found,
            "trades_attempted": trades_attempted,
            "trades_executed": trades_executed,
        }
        if skip_reasons:
            report["skip_reason"] = ", ".join(dict.fromkeys(skip_reasons))
        if execution_errors:
            report["execution_errors"] = execution_errors
        print(json.dumps({"automaton": report}))


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Polymarket Market Maker — GTC limit orders on both sides of liquid markets"
    )
    parser.add_argument("--live", action="store_true", help="Execute real trades (default: dry run)")
    parser.add_argument("--dry-run", action="store_true", help="Paper trading (default)")
    parser.add_argument("--positions", action="store_true", help="Show open positions")
    parser.add_argument("--config", action="store_true", help="Show current config")
    parser.add_argument("--set", action="append", metavar="KEY=VALUE",
                        help="Set a config value (e.g. --set max_order_usd=10.0)")
    parser.add_argument("--smart-sizing", action="store_true",
                        help="Use portfolio-based position sizing")
    parser.add_argument("--no-safeguards", action="store_true",
                        help="Disable pre-trade safeguard checks")

    args = parser.parse_args()

    # Handle --set
    if args.set:
        updates = {}
        for item in args.set:
            if "=" in item:
                key, value = item.split("=", 1)
                if key in CONFIG_SCHEMA:
                    type_fn = CONFIG_SCHEMA[key].get("type", str)
                    try:
                        value = type_fn(value)
                    except (ValueError, TypeError):
                        pass
                updates[key] = value
        if updates:
            update_config(updates, __file__)
            print(f"Config updated: {updates}")
            print(f"Saved to: {get_config_path(__file__)}")
            _config = load_config(CONFIG_SCHEMA, __file__, slug=SKILL_SLUG)
            MAX_ORDER_USD        = _config["max_order_usd"]
            MAX_MARKETS          = _config["max_markets"]
            MIN_VOL_24H          = _config["min_vol_24h"]
            SPREAD_OFFSET        = _config["spread_offset"]
            MIN_PRICE            = _config["min_price"]
            MAX_PRICE            = _config["max_price"]
            MIN_HOURS_TO_RESOLVE = _config["min_hours_to_resolve"]

    dry_run = not args.live

    run_strategy(
        dry_run=dry_run,
        positions_only=args.positions,
        show_config=args.config,
        use_safeguards=not args.no_safeguards,
    )

    # Fallback automaton report (covers early-return paths)
    if os.environ.get("AUTOMATON_MANAGED"):
        print(json.dumps({"automaton": {
            "signals": 0, "trades_attempted": 0, "trades_executed": 0,
            "skip_reason": "no_signal"
        }}))
