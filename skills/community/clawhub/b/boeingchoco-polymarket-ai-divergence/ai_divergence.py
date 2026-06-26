#!/usr/bin/env python3
"""
Simmer AI Divergence Trader

Finds markets where Simmer's AI consensus diverges from the real market price,
then trades on the mispriced side using Kelly sizing.

Usage:
    python ai_divergence.py              # Scan only (dry run)
    python ai_divergence.py --live       # Scan + execute trades
    python ai_divergence.py --min 10     # Only >10% divergence
    python ai_divergence.py --bullish    # AI more bullish than market
    python ai_divergence.py --bearish    # AI more bearish than market
    python ai_divergence.py --json       # Machine-readable output
"""

import os
import sys
import json
import math
import argparse
from datetime import datetime, timezone
from pathlib import Path

# Force line-buffered stdout so output is visible in non-TTY environments (cron, Docker, OpenClaw)
sys.stdout.reconfigure(line_buffering=True)


# =============================================================================
# Configuration
# =============================================================================

_SIMMER_SDK_IMPORT_ERROR = None

try:
    from simmer_sdk.skill import load_config, update_config, get_config_path
except ImportError as exc:
    _SIMMER_SDK_IMPORT_ERROR = exc

    def _coerce_config_value(value, type_fn):
        try:
            return type_fn(value)
        except (ValueError, TypeError):
            return value

    def load_config(schema, _file, slug=None):
        """Minimal env/default config loader used until simmer-sdk is installed."""
        config = {}
        for key, spec in schema.items():
            env_name = spec.get("env")
            raw = os.environ.get(env_name) if env_name else None
            if raw is None:
                config[key] = spec.get("default")
                continue
            config[key] = _coerce_config_value(raw, spec.get("type", str))
        return config

    def get_config_path(file):
        slug = Path(file).stem.replace("_", "-")
        return Path.home() / ".config" / "simmer" / f"{slug}.json"

    def update_config(_updates, _file):
        raise RuntimeError("simmer-sdk not installed")

CONFIG_SCHEMA = {
    "min_divergence": {"env": "SIMMER_DIVERGENCE_MIN", "default": 5.0, "type": float},
    "default_direction": {"env": "SIMMER_DIVERGENCE_DIRECTION_FILTER", "default": "", "type": str},
    "max_bet_usd": {"env": "SIMMER_DIVERGENCE_MAX_BET_USD", "default": 5.0, "type": float},
    "max_trades_per_run": {"env": "SIMMER_DIVERGENCE_MAX_TRADES_PER_RUN", "default": 3, "type": int},
    "min_edge": {"env": "SIMMER_DIVERGENCE_MIN_EDGE", "default": 0.03, "type": float},
    "kelly_cap": {"env": "SIMMER_DIVERGENCE_KELLY_CAP", "default": 0.20, "type": float},
    "daily_budget": {"env": "SIMMER_DIVERGENCE_DAILY_BUDGET_USD", "default": 25.0, "type": float},
    # New v2.4 safeguards (research-backed)
    "ai_shrinkage": {"env": "SIMMER_DIVERGENCE_AI_SHRINKAGE", "default": 0.70, "type": float},
    "min_liquidity_usd": {"env": "SIMMER_DIVERGENCE_MIN_LIQUIDITY_USD", "default": 1000.0, "type": float},
    "min_volume_24h_usd": {"env": "SIMMER_DIVERGENCE_MIN_VOLUME_24H_USD", "default": 500.0, "type": float},
    "max_position_pct_liquidity": {"env": "SIMMER_DIVERGENCE_MAX_POS_PCT_LIQ", "default": 0.05, "type": float},
    "min_hours_to_resolve": {"env": "SIMMER_DIVERGENCE_MIN_HOURS_TO_RESOLVE", "default": 6.0, "type": float},
    "max_days_to_resolve": {"env": "SIMMER_DIVERGENCE_MAX_DAYS_TO_RESOLVE", "default": 180.0, "type": float},
    "max_divergence_sanity": {"env": "SIMMER_DIVERGENCE_MAX_DIV_SANITY", "default": 0.40, "type": float},
    "max_spread_pct_of_edge": {"env": "SIMMER_DIVERGENCE_MAX_SPREAD_PCT_EDGE", "default": 0.50, "type": float},
    "enable_spread_check": {"env": "SIMMER_DIVERGENCE_ENABLE_SPREAD_CHECK", "default": 1, "type": int},
    "enable_time_decay": {"env": "SIMMER_DIVERGENCE_ENABLE_TIME_DECAY", "default": 1, "type": int},
    "min_price": {"env": "SIMMER_DIVERGENCE_MIN_PRICE", "default": 0.03, "type": float},
    "max_price": {"env": "SIMMER_DIVERGENCE_MAX_PRICE", "default": 0.97, "type": float},
    "min_expected_profit_usd": {"env": "SIMMER_DIVERGENCE_MIN_EXPECTED_PROFIT_USD", "default": 0.10, "type": float},
    "enable_adaptive_shrinkage": {"env": "SIMMER_DIVERGENCE_ENABLE_ADAPTIVE_SHRINKAGE", "default": 1, "type": int},
    "adaptive_shrinkage_vol_mult": {"env": "SIMMER_DIVERGENCE_ADAPTIVE_SHRINK_VOL_MULT", "default": 1.25, "type": float},
    "oracle_shrinkage": {"env": "SIMMER_DIVERGENCE_ORACLE_SHRINKAGE", "default": 0.65, "type": float},
    "crowd_shrinkage": {"env": "SIMMER_DIVERGENCE_CROWD_SHRINKAGE", "default": 0.80, "type": float},
    "longshot_threshold": {"env": "SIMMER_DIVERGENCE_LONGSHOT_THRESHOLD", "default": 0.15, "type": float},
    "longshot_penalty_bps": {"env": "SIMMER_DIVERGENCE_LONGSHOT_PENALTY_BPS", "default": 75, "type": int},
    "slippage_buffer_pct": {"env": "SIMMER_DIVERGENCE_SLIPPAGE_BUFFER_PCT", "default": 0.01, "type": float},
    "min_top_book_depth_usd": {"env": "SIMMER_DIVERGENCE_MIN_TOP_BOOK_DEPTH_USD", "default": 250.0, "type": float},
    # v2.6: category-aware Kelly multiplier — politics/crypto are bot-heavy and
    # efficient, sports/niche markets have larger AI alpha. Per Kalshibench /
    # QuantPedia research, sizing down on efficient categories improves Sharpe.
    "category_multipliers_csv": {
        "env": "SIMMER_DIVERGENCE_CATEGORY_MULTIPLIERS",
        "default": "politics=0.60,crypto=0.60,sports=0.85,default=0.75",
        "type": str,
    },
    "enable_category_multiplier": {
        "env": "SIMMER_DIVERGENCE_ENABLE_CATEGORY_MULTIPLIER",
        "default": 1,
        "type": int,
    },
}

_config = load_config(CONFIG_SCHEMA, __file__, slug="boeingchoco-polymarket-ai-divergence")


def require_simmer_sdk():
    """Exit with a concise setup hint when the SDK is unavailable."""
    if _SIMMER_SDK_IMPORT_ERROR is None:
        return
    print("Error: simmer-sdk not installed. Run: python -m pip install 'simmer-sdk>=0.11.1'")
    sys.exit(1)


def normalize_direction_filter(value: str):
    """Return canonical direction filter: bullish, bearish, or None."""
    direction = (value or "").strip().lower()
    aliases = {
        "": None,
        "all": None,
        "any": None,
        "both": None,
        "none": None,
        "bull": "bullish",
        "bullish": "bullish",
        "yes": "bullish",
        "yes_only": "bullish",
        "yes-only": "bullish",
        "buy_yes": "bullish",
        "buy-yes": "bullish",
        "bear": "bearish",
        "bearish": "bearish",
        "no": "bearish",
        "no_only": "bearish",
        "no-only": "bearish",
        "buy_no": "bearish",
        "buy-no": "bearish",
    }
    return aliases.get(direction)


def market_passes_direction(market: dict, direction: str = None) -> bool:
    direction = normalize_direction_filter(direction)
    if direction is None:
        return True
    div = market.get("divergence") or 0
    if direction == "bullish":
        return div > 0
    if direction == "bearish":
        return div < 0
    return True

DEFAULT_MIN_DIVERGENCE = _config["min_divergence"]
DEFAULT_DIRECTION = normalize_direction_filter(_config["default_direction"])
MAX_BET_USD = _config["max_bet_usd"]
_automaton_max = os.environ.get("AUTOMATON_MAX_BET")
if _automaton_max:
    MAX_BET_USD = min(MAX_BET_USD, float(_automaton_max))
MAX_TRADES_PER_RUN = _config["max_trades_per_run"]
MIN_EDGE = _config["min_edge"]
KELLY_CAP = _config["kelly_cap"]
DAILY_BUDGET = _config["daily_budget"]

# v2.4 safeguard knobs
AI_SHRINKAGE = max(0.0, min(1.0, _config["ai_shrinkage"]))
MIN_LIQUIDITY_USD = _config["min_liquidity_usd"]
MIN_VOLUME_24H_USD = _config["min_volume_24h_usd"]
MAX_POSITION_PCT_LIQUIDITY = _config["max_position_pct_liquidity"]
MIN_HOURS_TO_RESOLVE = _config["min_hours_to_resolve"]
MAX_DAYS_TO_RESOLVE = _config["max_days_to_resolve"]
MAX_DIVERGENCE_SANITY = _config["max_divergence_sanity"]
MAX_SPREAD_PCT_OF_EDGE = _config["max_spread_pct_of_edge"]
ENABLE_SPREAD_CHECK = bool(_config["enable_spread_check"])
ENABLE_TIME_DECAY = bool(_config["enable_time_decay"])
MIN_PRICE = max(0.0, min(1.0, _config["min_price"]))
MAX_PRICE = max(0.0, min(1.0, _config["max_price"]))
MIN_EXPECTED_PROFIT_USD = max(0.0, _config["min_expected_profit_usd"])
ENABLE_ADAPTIVE_SHRINKAGE = bool(_config["enable_adaptive_shrinkage"])
ADAPTIVE_SHRINKAGE_VOL_MULT = _config["adaptive_shrinkage_vol_mult"]
ORACLE_SHRINKAGE = max(0.0, min(1.0, _config["oracle_shrinkage"]))
CROWD_SHRINKAGE = max(0.0, min(1.0, _config["crowd_shrinkage"]))
LONGSHOT_THRESHOLD = max(0.01, min(0.49, _config["longshot_threshold"]))
LONGSHOT_PENALTY_BPS = max(0, int(_config["longshot_penalty_bps"]))
SLIPPAGE_BUFFER_PCT = max(0.0, _config["slippage_buffer_pct"])
MIN_TOP_BOOK_DEPTH_USD = max(0.0, _config["min_top_book_depth_usd"])
ENABLE_CATEGORY_MULTIPLIER = bool(_config["enable_category_multiplier"])


def _parse_category_csv(csv_str: str) -> dict:
    """Parse 'politics=0.6,crypto=0.6,sports=0.85,default=0.75' → dict."""
    out = {}
    for pair in (csv_str or "").split(","):
        if "=" not in pair:
            continue
        key, val = pair.split("=", 1)
        try:
            out[key.strip().lower()] = max(0.0, min(2.0, float(val.strip())))
        except ValueError:
            continue
    return out


CATEGORY_MULTIPLIERS = _parse_category_csv(_config["category_multipliers_csv"])

TRADE_SOURCE = "sdk:divergence"
SKILL_SLUG = "boeingchoco-polymarket-ai-divergence"
_automaton_reported = False
MIN_SHARES_PER_ORDER = 5.0


# =============================================================================
# SimmerClient singleton
# =============================================================================

_client = None


def get_client(live=True):
    """Lazy-init SimmerClient singleton."""
    global _client
    if _client is None:
        require_simmer_sdk()
        try:
            from simmer_sdk import SimmerClient
        except ImportError:
            print("Error: simmer-sdk not installed. Run: python -m pip install 'simmer-sdk>=0.11.1'")
            sys.exit(1)
        api_key = os.environ.get("SIMMER_API_KEY")
        if not api_key:
            print("Error: SIMMER_API_KEY environment variable not set")
            print("Get your API key from: simmer.markets/dashboard -> SDK tab")
            sys.exit(1)
        venue = os.environ.get("TRADING_VENUE", "polymarket")
        _client = SimmerClient(api_key=api_key, venue=venue, live=live)
    return _client


# =============================================================================
# Daily spend tracking
# =============================================================================

def _get_spend_path():
    return Path(__file__).parent / "daily_spend.json"


def _load_daily_spend():
    """Load today's spend. Resets if date != today (UTC)."""
    spend_path = _get_spend_path()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if spend_path.exists():
        try:
            with open(spend_path) as f:
                data = json.load(f)
            if data.get("date") == today:
                return data
        except (json.JSONDecodeError, IOError):
            pass
    return {"date": today, "spent": 0.0, "trades": 0}


def _save_daily_spend(spend_data):
    with open(_get_spend_path(), "w") as f:
        json.dump(spend_data, f, indent=2)


# =============================================================================
# Trading helpers
# =============================================================================

def execute_trade(market_id, side, amount, signal_data=None):
    """Execute a buy trade via Simmer SDK with source tagging."""
    try:
        result = get_client().trade(
            market_id=market_id,
            side=side,
            amount=amount,
            source=TRADE_SOURCE, skill_slug=SKILL_SLUG,
            signal_data=signal_data,
        )
        return {
            "success": result.success,
            "trade_id": result.trade_id,
            "shares_bought": result.shares_bought,
            "shares": result.shares_bought,
            "error": result.error,
            "simulated": result.simulated,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_positions():
    """Get current positions as list of dicts, filtered by venue."""
    try:
        client = get_client()
        positions = client.get_positions(venue=client.venue)
        from dataclasses import asdict
        return [asdict(p) for p in positions]
    except Exception:
        return []


def get_market_context(market_id):
    """Fetch market context (includes fee_rate_bps and safeguards)."""
    try:
        return get_client()._request("GET", f"/api/sdk/context/{market_id}")
    except Exception:
        return None


def calculate_kelly_size(edge, price, max_bet, kelly_cap):
    """Kelly criterion position sizing.

    kelly_fraction = edge / (1 - price) for YES side
    Capped at kelly_cap fraction of max_bet.
    """
    if price <= 0 or price >= 1:
        return 0
    kelly = edge / (1 - price)
    kelly = max(0, min(kelly, kelly_cap))
    return round(kelly * max_bet, 2)


# =============================================================================
# Calibration / safeguard helpers (v2.4)
# =============================================================================

def calibrated_edge(raw_divergence: float, shrinkage: float = AI_SHRINKAGE) -> float:
    """Shrink the AI edge toward zero to correct for AI overconfidence.

    LLM forecasters are systematically overconfident (Kalshibench: even
    Claude Opus shows ECE ≈ 0.12; most models score worse than base rates).
    A multiplicative shrinkage on the divergence is the simplest fix that
    keeps the trading direction correct but trims the size.

    shrinkage=1.0 → trust AI fully (legacy v2.3 behavior)
    shrinkage=0.0 → ignore AI entirely (paper-only)
    """
    return raw_divergence * shrinkage


def adaptive_shrinkage_for_market(base_shrinkage: float, market: dict) -> float:
    """Adjust shrinkage by market quality / stress regime.

    Rationale:
    - Wider spread relative to edge tends to indicate weaker executable alpha.
    - Higher 1d price-change magnitude tends to mark event-volatility regimes.
    In both cases we shrink edge harder (lower effective shrinkage).
    """
    if not ENABLE_ADAPTIVE_SHRINKAGE:
        return base_shrinkage

    s = base_shrinkage
    vol_1d = abs(float(market.get("gamma_one_day_price_change") or 0.0))
    if vol_1d >= 0.10:
        s *= 0.85
    if vol_1d >= 0.20:
        s *= 0.80

    # Liquidity stress penalty: lower liquidity gets stronger shrink.
    liq = float(market.get("gamma_liquidity") or 0.0)
    if 0 < liq < (MIN_LIQUIDITY_USD * ADAPTIVE_SHRINKAGE_VOL_MULT):
        s *= 0.90

    return max(0.20, min(1.0, s))


def source_shrinkage(signal_source: str) -> float:
    """Per-signal shrinkage to handle heterogeneous alpha quality."""
    src = (signal_source or "").lower()
    if src == "oracle":
        return ORACLE_SHRINKAGE
    if src == "crowd":
        return CROWD_SHRINKAGE
    return AI_SHRINKAGE


def effective_shrinkage_for_market(market: dict) -> float:
    """Combine source-aware and adaptive shrinkage for a market."""
    return adaptive_shrinkage_for_market(
        source_shrinkage(market.get("signal_source")),
        market,
    )


def calibrated_edge_for_market(market: dict) -> float:
    """Return signed divergence after all configured shrinkage."""
    return calibrated_edge(
        market.get("divergence") or 0,
        shrinkage=effective_shrinkage_for_market(market),
    )


def category_kelly_multiplier(market: dict) -> float:
    """Scale position by per-category efficiency.

    Research (Kalshibench, QuantPedia 2025): politics and crypto markets are
    dominated by professional bot flow → smaller AI alpha persists → we size
    smaller. Sports markets have more retail noise → larger alpha → larger
    multiplier. Niche / long-tail markets (default bucket) are where AI most
    outperforms market consensus.
    """
    if not ENABLE_CATEGORY_MULTIPLIER:
        return 1.0
    if not CATEGORY_MULTIPLIERS:
        return 1.0
    category = (market.get("gamma_category") or "").strip().lower()
    if category and category in CATEGORY_MULTIPLIERS:
        return CATEGORY_MULTIPLIERS[category]
    return CATEGORY_MULTIPLIERS.get("default", 1.0)


def hours_to_resolution(resolves_at) -> float:
    """Return hours until resolution, or +inf if unknown/unparseable."""
    if not resolves_at:
        return float("inf")
    try:
        # Accept ISO strings ('2026-06-01T12:00:00Z' or '+00:00') and datetimes
        if isinstance(resolves_at, str):
            s = resolves_at.replace("Z", "+00:00")
            dt = datetime.fromisoformat(s)
        else:
            dt = resolves_at
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        delta = (dt - datetime.now(timezone.utc)).total_seconds() / 3600.0
        return delta
    except (ValueError, TypeError):
        return float("inf")


def time_decay_multiplier(resolves_at, scale_days: float = 30.0) -> float:
    """Scale position by sqrt(days_to_resolve / scale_days), capped at 1.0.

    Empirical guidance from Polymarket bot research: near-resolution markets
    have terminal volatility and oracle risk that bias outcomes against
    divergence trades. Long-dated markets carry capital-opportunity cost.
    """
    hours = hours_to_resolution(resolves_at)
    if hours == float("inf"):
        return 1.0  # unknown → no penalty
    days = max(hours / 24.0, 0.0)
    return min(1.0, math.sqrt(days / scale_days))


def get_clob_book_summary(token_id: str):
    """Lazily fetch CLOB orderbook summary. Returns None on any failure."""
    if not token_id:
        return None
    try:
        from clob_api import ClobClient
    except ImportError:
        return None
    try:
        return ClobClient().book_summary(str(token_id))
    except Exception:
        return None


def extract_yes_token_id(gamma_meta: dict):
    """Pull the YES side's CLOB token id from Gamma metadata if available."""
    if not isinstance(gamma_meta, dict):
        return None
    tokens = gamma_meta.get("clob_token_ids") or []
    if isinstance(tokens, list) and tokens:
        return tokens[0]
    return None


# =============================================================================
# Market data
# =============================================================================

def get_markets() -> list:
    """Fetch markets with divergence between LMSR pool price and external venue price.

    Divergence sources:
    - 'oracle': AI multi-model forecast (activated markets)
    - 'crowd': Sim agent trading activity against LMSR pool (tracking markets)
    """
    data = get_client()._request("GET", "/api/sdk/markets/opportunities", params={"limit": 50, "min_divergence": 0.01})
    return [
        {
            "id": m.get("id"),
            "question": m.get("question"),
            "current_probability": m.get("current_probability"),
            "external_price_yes": m.get("external_price_yes"),
            "divergence": m.get("divergence"),
            "import_source": m.get("import_source"),
            "resolves_at": m.get("resolves_at"),
            "opportunity_score": m.get("opportunity_score"),
            "recommended_side": m.get("recommended_side"),
            "signal_source": m.get("signal_source", "crowd"),
        }
        for m in data.get("opportunities", [])
    ]


def _norm_question(q: str) -> str:
    """Normalize a question for fuzzy lookup (lowercase, collapse whitespace, strip punct)."""
    if not q:
        return ""
    out = "".join(c.lower() if c.isalnum() or c.isspace() else " " for c in q)
    return " ".join(out.split())


def enrich_with_gamma(markets: list, candidate_only: bool = False) -> list:
    """Enrich market list with Polymarket metadata from Gamma API.

    Adds description, category, volume_24h, liquidity, clob_token_ids and
    raw gamma payload from Polymarket's Gamma API. Only enriches
    polymarket-sourced markets. Failures are non-blocking — markets are
    returned unchanged on error.

    When ``candidate_only`` is True, only enriches markets whose absolute
    divergence is already over ``MIN_EDGE`` (saves a lot of Gamma calls
    when scanning a large opportunity list).
    """
    poly_markets = [
        m for m in markets
        if m.get("import_source") == "polymarket"
        and (not candidate_only or abs(m.get("divergence") or 0) >= MIN_EDGE)
    ]
    if not poly_markets:
        return markets

    try:
        # Local helper, lives next to this skill (was in simmer_sdk pre-0.9.21)
        from gamma_api import GammaClient
    except ImportError:
        return markets

    gamma = GammaClient()

    # Build a normalized lookup so question-text minor differences still match
    gamma_lookup = {}
    seen_queries = set()
    for m in poly_markets:
        q = m.get("question", "")
        # Use first 6 significant words as search query (more specific than 5)
        words = q.split()[:6]
        query = " ".join(words)
        if not query or query in seen_queries:
            continue
        seen_queries.add(query)

        try:
            results = gamma.search(query, pages=1)
            for event in results:
                for gm in event.get("markets", []):
                    gamma_lookup[_norm_question(gm.get("question", ""))] = gm
        except Exception:
            continue

    # Merge Gamma metadata into our markets
    for m in markets:
        gm = gamma_lookup.get(_norm_question(m.get("question", "")))
        if gm:
            m["gamma_description"] = gm.get("description", "")
            m["gamma_category"] = gm.get("category", "")
            m["gamma_volume_24h"] = gm.get("volume_24h", 0)
            m["gamma_liquidity"] = gm.get("liquidity", 0)
            m["gamma_tags"] = gm.get("tags", [])
            m["gamma_neg_risk"] = gm.get("neg_risk", False)
            m["gamma_one_day_price_change"] = gm.get("one_day_price_change", 0)
            m["gamma_clob_token_ids"] = gm.get("clob_token_ids", [])
            m["gamma_meta"] = gm

    return markets


# =============================================================================
# Scanner display
# =============================================================================

def format_divergence(markets: list, min_div: float = 0, direction: str = None) -> None:
    """Display divergence table."""
    direction = normalize_direction_filter(direction)
    filtered = []
    for m in markets:
        div = m.get("divergence") or 0
        if abs(div) < min_div / 100:
            continue
        if not market_passes_direction(m, direction):
            continue
        filtered.append(m)

    filtered.sort(key=lambda m: abs(m.get("divergence") or 0), reverse=True)

    if not filtered:
        print("No markets match your filters.")
        return

    print()
    print(f"🔮 AI Divergence Scanner  (source/adaptive calibration enabled)")
    print("=" * 82)
    print(f"{'Market':<36} {'LMSR':>7} {'Venue':>7} {'Div':>7} {'Cal':>7} {'Source':>6} {'Signal':>8}")
    print("-" * 82)

    for m in filtered[:20]:
        q = m.get("question", "")[:34]
        simmer = m.get("current_probability") or 0
        poly = m.get("external_price_yes") or 0
        div = m.get("divergence") or 0
        cal = calibrated_edge_for_market(m)
        src = m.get("signal_source", "crowd")[:5]

        is_polymarket = m.get("import_source") in ("polymarket", "kalshi")
        if abs(cal) >= MIN_EDGE:
            signal = "🟡 AI>MKT" if (is_polymarket and cal > 0) else (
                     "🟡 AI<MKT" if is_polymarket else (
                     "🟢 BUY" if cal > 0 else "🔴 SELL"))
        else:
            signal = "⚪ HOLD"

        print(f"{q:<36} {simmer:>6.1%} {poly:>6.1%} {div:>+6.1%} {cal:>+6.1%} {src:>6} {signal:>8}")

    print("-" * 82)
    print(f"Showing {len(filtered[:20])} of {len(filtered)} markets with divergence")
    print()

    bullish = len([m for m in filtered if (m.get("divergence") or 0) > 0])
    bearish = len([m for m in filtered if (m.get("divergence") or 0) < 0])
    tradeable = len([m for m in filtered if abs(calibrated_edge_for_market(m)) >= MIN_EDGE])
    avg_div = sum(abs(m.get("divergence") or 0) for m in filtered) / len(filtered) if filtered else 0

    print(f"📊 Summary: {bullish} bullish, {bearish} bearish, avg divergence {avg_div:.1%}")
    print(f"   {tradeable} pass min_edge {MIN_EDGE:.1%} after calibration shrinkage")


def show_opportunities(markets: list, direction: str = None) -> None:
    """Show actionable high-conviction opportunities."""
    print()
    print("💡 Top Opportunities (>10% divergence)")
    print("=" * 75)

    opps = [
        m for m in markets
        if abs(m.get("divergence") or 0) > 0.10
        and market_passes_direction(m, direction)
    ]
    opps.sort(key=lambda m: abs(m.get("divergence") or 0), reverse=True)

    if not opps:
        print("No high-divergence opportunities right now.")
        return

    for m in opps[:5]:
        q = m.get("question", "")
        simmer = m.get("current_probability") or 0
        poly = m.get("external_price_yes") or 0
        div = m.get("divergence") or 0
        resolves = m.get("resolves_at", "Unknown")

        is_external = m.get("import_source") in ("polymarket", "kalshi")
        venue_name = "Kalshi" if m.get("import_source") == "kalshi" else "Polymarket"
        if is_external:
            action = f"Simmer AI: {simmer:.0%} vs {venue_name}: {poly:.0%} — do your own research before trading"
        elif div > 0:
            action = f"AI says BUY YES (AI: {simmer:.0%} vs Market: {poly:.0%})"
        else:
            action = f"AI says BUY NO (AI: {simmer:.0%} vs Market: {poly:.0%})"

        print(f"\n📌 {q[:70]}")
        print(f"   {action}")
        print(f"   Divergence: {div:+.1%} | Resolves: {resolves[:10] if resolves else 'TBD'}")


# =============================================================================
# Trade execution
# =============================================================================

def run_divergence_trades(markets, dry_run=True, quiet=False, direction: str = None):
    """Scan for divergence opportunities and execute trades.

    Returns (signals_found, trades_attempted, trades_executed, skip_reasons,
    total_usd_spent, execution_errors).
    """
    def log(msg, force=False):
        if not quiet or force:
            print(msg)

    # Filter to tradeable candidates (apply calibration shrinkage to qualify edges
    # the same way trading does, so the candidate count matches what we'd actually trade).
    candidates = [
        m for m in markets
        if m.get("id") and abs(calibrated_edge_for_market(m)) >= MIN_EDGE
        and market_passes_direction(m, direction)
    ]
    candidates.sort(key=lambda m: abs(calibrated_edge_for_market(m)), reverse=True)

    signals_found = len(candidates)
    skip_reasons = []
    execution_errors = []
    if not candidates:
        log("  No markets above min edge threshold (after source/adaptive calibration)")
        return signals_found, 0, 0, skip_reasons, 0.0, []

    # Enrich just the candidates with Gamma metadata so liquidity / volume /
    # token_ids are available for the safeguard checks below.
    candidates = enrich_with_gamma(candidates)
    candidates = [
        m for m in candidates
        if abs(calibrated_edge_for_market(m)) >= MIN_EDGE
    ]
    candidates.sort(key=lambda m: abs(calibrated_edge_for_market(m)), reverse=True)
    signals_found = len(candidates)
    if not candidates:
        log("  No markets above min edge threshold (after source/adaptive calibration)")
        return signals_found, 0, 0, skip_reasons, 0.0, []

    # Load daily spend
    daily_spend = _load_daily_spend()
    remaining_budget = DAILY_BUDGET - daily_spend["spent"]
    if remaining_budget <= 0:
        log(f"  Daily budget exhausted (${daily_spend['spent']:.2f}/${DAILY_BUDGET:.2f})", force=True)
        skip_reasons.append("daily budget exhausted")
        return signals_found, 0, 0, skip_reasons, 0.0, []

    # Get existing positions to avoid doubling up
    positions = get_positions()
    held_market_ids = {p.get("market_id") for p in positions if (p.get("shares_yes") or 0) > 0 or (p.get("shares_no") or 0) > 0}

    trades_attempted = 0
    trades_executed = 0
    total_usd_spent = 0.0

    log(f"\n{'=' * 50}")
    log(f"  🎯 Divergence Trading (v2.5: source/adaptive calibration, liquidity-gated)")
    log(f"  min_edge={MIN_EDGE:.1%}  kelly_cap={KELLY_CAP:.0%}  slip={SLIPPAGE_BUFFER_PCT:.1%}")
    log(f"{'=' * 50}")

    # Check a wide margin so liquidity / spread skips don't prematurely empty the run
    for m in candidates[:max(MAX_TRADES_PER_RUN * 3, MAX_TRADES_PER_RUN + 5)]:
        if trades_executed >= MAX_TRADES_PER_RUN:
            break
        if remaining_budget < 0.50:
            log(f"  Budget remaining ${remaining_budget:.2f} < $0.50 — stopping")
            break

        market_id = m["id"]
        raw_div = m.get("divergence") or 0
        question = m.get("question", "Unknown")[:50]

        # ── Safeguard 1: skip already-held positions ─────────────────────
        if market_id in held_market_ids:
            log(f"  ⏭️  {question}... — already holding position")
            skip_reasons.append("already holding")
            continue

        # ── Safeguard 2: sanity-cap on extreme divergence ────────────────
        # Divergences > 40% on a sub-second basis are almost always stale data,
        # broken oracles, or markets about to resolve. Skip rather than chase.
        if abs(raw_div) > MAX_DIVERGENCE_SANITY:
            log(f"  ⏭️  {question}... — extreme divergence {raw_div:+.1%} > {MAX_DIVERGENCE_SANITY:.0%} (likely stale)")
            skip_reasons.append("extreme divergence (sanity)")
            continue

        # ── Safeguard 3: time-to-resolution band ─────────────────────────
        hours = hours_to_resolution(m.get("resolves_at"))
        if hours != float("inf"):
            if hours < MIN_HOURS_TO_RESOLVE:
                log(f"  ⏭️  {question}... — resolves in {hours:.1f}h < {MIN_HOURS_TO_RESOLVE:.0f}h floor")
                skip_reasons.append("resolves too soon")
                continue
            if hours / 24 > MAX_DAYS_TO_RESOLVE:
                log(f"  ⏭️  {question}... — resolves in {hours/24:.0f}d > {MAX_DAYS_TO_RESOLVE:.0f}d ceiling")
                skip_reasons.append("resolves too far out")
                continue

        # ── Safeguard 4: liquidity / volume gates (polymarket-sourced only) ──
        is_polymarket = m.get("import_source") == "polymarket"
        liquidity_usd = m.get("gamma_liquidity") or 0
        volume_24h_usd = m.get("gamma_volume_24h") or 0
        if is_polymarket and m.get("gamma_meta"):
            if liquidity_usd < MIN_LIQUIDITY_USD:
                log(f"  ⏭️  {question}... — liquidity ${liquidity_usd:,.0f} < ${MIN_LIQUIDITY_USD:,.0f}")
                skip_reasons.append("liquidity below floor")
                continue
            if volume_24h_usd < MIN_VOLUME_24H_USD:
                log(f"  ⏭️  {question}... — 24h volume ${volume_24h_usd:,.0f} < ${MIN_VOLUME_24H_USD:,.0f}")
                skip_reasons.append("volume below floor")
                continue

        # Fetch context for fee rate + flip-flop discipline
        context = get_market_context(market_id)
        if not context:
            log(f"  ⏭️  {question}... — context fetch failed")
            continue

        ctx_market = context.get("market", {})
        fee_rate_bps = ctx_market.get("fee_rate_bps", 0)
        fee_pct = fee_rate_bps / 10000  # e.g. 1000bps = 10%

        # ── Safeguard 5: flip-flop discipline ────────────────────────────
        discipline = context.get("discipline", {})
        warning_level = discipline.get("warning_level", "none")
        if warning_level == "severe":
            log(f"  ⏭️  {question}... — flip-flop warning (severe)")
            skip_reasons.append("safeguard: flip-flop severe")
            continue

        # Determine side and apply calibration shrinkage to the edge
        side = "yes" if raw_div > 0 else "no"
        base_shrinkage = source_shrinkage(m.get("signal_source"))
        effective_shrinkage = adaptive_shrinkage_for_market(base_shrinkage, m)
        cal_edge = abs(calibrated_edge(raw_div, shrinkage=effective_shrinkage))

        # Subtract fee + conservative slippage buffer before trading.
        # This is intentionally simple: if edge cannot survive realistic
        # friction, the trade should be skipped.
        net_edge = cal_edge - fee_pct - SLIPPAGE_BUFFER_PCT
        if net_edge < MIN_EDGE:
            log(f"  ⏭️  {question}... — raw {abs(raw_div):.1%} × shrink {effective_shrinkage:.2f} → cal {cal_edge:.1%} - fee {fee_pct:.1%} - slip {SLIPPAGE_BUFFER_PCT:.1%} = {net_edge:.1%} < {MIN_EDGE:.1%}")
            skip_reasons.append(f"net edge too low after calibration + {fee_rate_bps}bps fee + slippage buffer")
            continue
        edge = net_edge

        # Price we're buying at (external price for the side we're trading)
        if side == "yes":
            price = m.get("external_price_yes") or 0.5
        else:
            price = 1 - (m.get("external_price_yes") or 0.5)

        # ── Safeguard 6: CLOB spread check (polymarket only, opt-out) ────
        book_summary = None
        if ENABLE_SPREAD_CHECK and is_polymarket:
            token_id = extract_yes_token_id(m.get("gamma_meta") or {})
            if token_id:
                # For NO side, use the second token in the pair
                if side == "no":
                    token_ids = (m.get("gamma_meta") or {}).get("clob_token_ids") or []
                    if len(token_ids) > 1:
                        token_id = token_ids[1]
                book_summary = get_clob_book_summary(token_id)
                if book_summary:
                    spread = book_summary["spread"]
                    book_depth_usd = book_summary["ask_depth_usd"]
                    if book_depth_usd < MIN_TOP_BOOK_DEPTH_USD:
                        log(f"  ⏭️  {question}... — top-of-book depth ${book_depth_usd:,.0f} < ${MIN_TOP_BOOK_DEPTH_USD:,.0f}")
                        skip_reasons.append("top-of-book depth below floor")
                        continue
                    spread_share_of_edge = (spread / 2) / max(edge, 1e-6)
                    if spread_share_of_edge > MAX_SPREAD_PCT_OF_EDGE:
                        log(f"  ⏭️  {question}... — half-spread {spread/2:.1%} eats {spread_share_of_edge:.0%} of edge {edge:.1%}")
                        skip_reasons.append("spread too wide vs edge")
                        continue
                    # Use the actual ask we'd cross for the token being bought.
                    crossing_price = book_summary["best_ask"]
                    if 0 < crossing_price < 1:
                        price = crossing_price

        # Safeguard: avoid longshot/favorite tails where prices are noisier and upside is asymmetric
        if price <= MIN_PRICE or price >= MAX_PRICE:
            log(f"  ⏭️  {question}... — price {price:.1%} outside [{MIN_PRICE:.0%}, {MAX_PRICE:.0%}]")
            skip_reasons.append("price outside tradable band")
            continue

        # Optional longshot penalty (favorite-longshot bias defense):
        # low-probability contracts tend to be structurally overpriced.
        is_longshot = price <= LONGSHOT_THRESHOLD
        if is_longshot and LONGSHOT_PENALTY_BPS > 0:
            longshot_penalty = LONGSHOT_PENALTY_BPS / 10000
            edge -= longshot_penalty
            if edge < MIN_EDGE:
                log(f"  ⏭️  {question}... — longshot penalty {longshot_penalty:.2%} reduces edge to {edge:.1%} < {MIN_EDGE:.1%}")
                skip_reasons.append("longshot penalty reduced edge below floor")
                continue

        # Kelly sizing on the calibrated, fee-adjusted edge
        position_size = calculate_kelly_size(edge, price, MAX_BET_USD, KELLY_CAP)

        # Category-aware Kelly multiplier (research: smaller alpha in
        # politics/crypto → size down). Applied BEFORE expected-profit /
        # liquidity / depth checks so they see the realistic sizing.
        cat_mult = category_kelly_multiplier(m)
        if cat_mult < 0.99:
            scaled = round(position_size * cat_mult, 2)
            cat_label = (m.get("gamma_category") or "default")[:20]
            log(f"  📂 Category '{cat_label}' multiplier {cat_mult:.2f} → ${scaled:.2f}")
            position_size = scaled

        expected_profit_usd = position_size * edge
        if expected_profit_usd < MIN_EXPECTED_PROFIT_USD:
            log(f"  ⏭️  {question}... — expected edge ${expected_profit_usd:.2f} < ${MIN_EXPECTED_PROFIT_USD:.2f}")
            skip_reasons.append("expected edge too small")
            continue

        if position_size < 0.50:
            log(f"  ⏭️  {question}... — Kelly size ${position_size:.2f} too small")
            skip_reasons.append("position too small")
            continue

        # ── Safeguard 7: cap to fraction of available liquidity ──────────
        if is_polymarket and liquidity_usd > 0:
            liq_cap = liquidity_usd * MAX_POSITION_PCT_LIQUIDITY
            if position_size > liq_cap:
                log(f"  📉 Capping ${position_size:.2f} → ${liq_cap:.2f} ({MAX_POSITION_PCT_LIQUIDITY:.0%} of ${liquidity_usd:,.0f} liquidity)")
                position_size = round(liq_cap, 2)

        # Cap to top-of-book depth (avoid moving the market against ourselves)
        if book_summary:
            depth_usd = book_summary["ask_depth_usd"]
            if depth_usd > 0:
                depth_cap = depth_usd * 0.20  # take at most 20% of top-level depth
                if position_size > depth_cap:
                    log(f"  📉 Capping ${position_size:.2f} → ${depth_cap:.2f} (20% of top-of-book ${depth_usd:,.0f})")
                    position_size = round(depth_cap, 2)

        # ── Time-decay sizing: scale down for near/far-dated markets ─────
        if ENABLE_TIME_DECAY:
            decay = time_decay_multiplier(m.get("resolves_at"))
            if decay < 0.99:
                scaled = round(position_size * decay, 2)
                log(f"  ⏱️  Time-decay scale {decay:.2f} → ${scaled:.2f}")
                position_size = scaled

        if position_size < 0.50:
            log(f"  ⏭️  {question}... — final size ${position_size:.2f} below $0.50 floor")
            skip_reasons.append("position too small after sizing")
            continue

        # Cap to remaining budget
        position_size = min(position_size, remaining_budget)

        trades_attempted += 1

        if dry_run:
            log(f"  🔒 [PAPER] {side.upper()} ${position_size:.2f} on {question}...")
            log(f"     Raw div: {raw_div:+.1%} | Cal edge: {edge:.1%} | Price: ${price:.3f}")
            continue

        # Execute trade
        log(f"  🎯 Trading {side.upper()} ${position_size:.2f} on {question}...")
        log(f"     Raw div: {raw_div:+.1%} | Cal edge: {edge:.1%} | Price: ${price:.3f}")
        _signal_data = {
            "edge": round(edge, 4),
            "raw_divergence": round(raw_div, 4),
            "calibration_shrinkage": round(AI_SHRINKAGE, 3),
            "source_shrinkage": round(base_shrinkage, 3),
            "effective_shrinkage": round(effective_shrinkage, 3),
            "confidence": round(min(0.95, edge * 2 + 0.5), 2),
            "signal_source": m.get("signal_source", "crowd"),
            "ai_forecast": round(m.get("current_probability") or 0, 4),
            "market_price": round(m.get("external_price_yes") or 0, 4),
            "divergence_pct": round(abs(raw_div) * 100, 2),
            "liquidity_usd": round(liquidity_usd, 2),
            "volume_24h_usd": round(volume_24h_usd, 2),
            "hours_to_resolve": round(hours, 1) if hours != float("inf") else None,
        }
        result = execute_trade(market_id, side, position_size, signal_data=_signal_data)

        if result and result.get("success"):
            trades_executed += 1
            total_usd_spent += position_size
            shares = result.get("shares_bought") or result.get("shares") or 0
            simulated = result.get("simulated", False)
            prefix = "[PAPER] " if simulated else ""
            log(f"  ✅ {prefix}Bought {shares:.1f} {side.upper()} shares", force=True)

            if not simulated:
                daily_spend["spent"] += position_size
                daily_spend["trades"] += 1
                _save_daily_spend(daily_spend)
                remaining_budget -= position_size
        else:
            error = result.get("error", "Unknown error") if result else "No response"
            log(f"  ❌ Trade failed: {error}", force=True)
            execution_errors.append(error[:120])

    log(f"\n  Signals: {signals_found} | Attempted: {trades_attempted} | Executed: {trades_executed}")
    if dry_run:
        log("  [PAPER MODE — use --live for real trades]")

    return signals_found, trades_attempted, trades_executed, skip_reasons, total_usd_spent, execution_errors


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Simmer AI Divergence Trader")
    parser.add_argument("--live", action="store_true", help="Execute real trades (default is dry-run)")
    parser.add_argument("--dry-run", action="store_true", help="(Default) Show opportunities without trading")
    parser.add_argument("--min", type=float, default=DEFAULT_MIN_DIVERGENCE,
                        help=f"Minimum divergence %% for scanner (default: {DEFAULT_MIN_DIVERGENCE})")
    parser.add_argument("--bullish", action="store_true", help="Only bullish divergence (Simmer > Poly)")
    parser.add_argument("--bearish", action="store_true", help="Only bearish divergence (Simmer < Poly)")
    parser.add_argument("--opportunities", "-o", action="store_true", help="Show top opportunities only")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--config", action="store_true", help="Show configuration")
    parser.add_argument("--quiet", "-q", action="store_true", help="Only output on trades/errors")
    parser.add_argument("--enrich", action="store_true",
                        help="Enrich results with Polymarket metadata via Gamma API")
    parser.add_argument("--set", action="append", metavar="KEY=VALUE",
                        help="Set config value (e.g., --set min_edge=0.03)")
    args = parser.parse_args()

    # Handle --set config updates
    if args.set:
        require_simmer_sdk()
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
            print(f"✅ Config updated: {updates}")
            print(f"   Saved to: {get_config_path(__file__)}")

    # Show config
    if args.config:
        config_path = get_config_path(__file__)
        print("🔮 AI Divergence Trader Configuration")
        print("=" * 40)
        for key, spec in CONFIG_SCHEMA.items():
            val = _config.get(key, spec.get("default"))
            print(f"  {key:<22} = {val}")
        print(f"\nConfig file: {config_path}")
        print(f"Config exists: {'Yes' if config_path.exists() else 'No'}")
        return

    # Validate API key by initializing client
    dry_run = not args.live
    client = get_client(live=not dry_run)

    # Redeem any winning positions before starting the cycle
    try:
        redeemed = client.auto_redeem()
        for r in redeemed:
            if r.get("success"):
                print(f"  💰 Redeemed {r['market_id'][:8]}... ({r.get('side', '?')})")
    except Exception:
        pass  # Non-critical — don't block trading

    # Balance pre-flight: skip cleanly when wallet is underfunded instead of
    # looping on rejected trades. Helper is collateral-agnostic — checks pUSD
    # on V2, USDC.e on V1 per server's exchange_version.
    global MAX_BET_USD, _automaton_reported
    is_paper_venue_pre = os.environ.get("TRADING_VENUE", "polymarket") == "sim"
    if not dry_run and not is_paper_venue_pre:
        _preflight = client.ensure_can_trade(min_usd=1.0)
        if not _preflight["ok"]:
            print(f"  ⏸️  insufficient_balance: ${_preflight['balance']:.2f} {_preflight['collateral']} "
                  f"(need ≥ $1.00) — skip")
            if os.environ.get("AUTOMATON_MANAGED"):
                print(json.dumps({"automaton": {
                    "signals": 0, "trades_attempted": 0, "trades_executed": 0,
                    "skip_reason": _preflight["reason"],
                    "balance_usd": round(_preflight["balance"], 2),
                }}))
                _automaton_reported = True
            return
        if _preflight["max_safe_size"] < MAX_BET_USD:
            print(f"  💰 Capping max bet ${MAX_BET_USD:.2f} → ${_preflight['max_safe_size']:.2f} "
                  f"(balance ${_preflight['balance']:.2f} {_preflight['collateral']})")
            MAX_BET_USD = _preflight["max_safe_size"]

    direction = DEFAULT_DIRECTION
    if args.bullish:
        direction = "bullish"
    elif args.bearish:
        direction = "bearish"

    markets = get_markets()
    markets = [m for m in markets if m.get('is_live_now', True) is not False]  # skip not-yet-open markets (no-op if field absent)

    # Always enrich candidates with Gamma metadata so liquidity / volume / spread
    # safeguards can run during display and trading. --enrich kept for backward
    # compatibility (full-list enrichment).
    if args.enrich:
        markets = enrich_with_gamma(markets)
    else:
        markets = enrich_with_gamma(markets, candidate_only=True)

    if args.json:
        filtered = [
            m for m in markets
            if abs(m.get("divergence") or 0) >= args.min / 100
            and market_passes_direction(m, direction)
        ]
        filtered.sort(key=lambda m: abs(m.get("divergence") or 0), reverse=True)
        print(json.dumps(filtered, indent=2))
        return

    # Scanner display
    if not args.quiet:
        if args.opportunities:
            show_opportunities(markets, direction)
        else:
            format_divergence(markets, args.min, direction)
            show_opportunities(markets, direction)

    # Trade execution
    skip_reasons = []
    is_paper_venue = os.environ.get("TRADING_VENUE", "polymarket") == "sim"
    if args.live or is_paper_venue:
        effective_dry_run = dry_run and not is_paper_venue
        signals, attempted, executed, skip_reasons, total_usd_spent, execution_errors = run_divergence_trades(markets, dry_run=effective_dry_run, quiet=args.quiet, direction=direction)
    else:
        signals = len([
            m for m in markets
            if abs(calibrated_edge_for_market(m)) >= MIN_EDGE
            and market_passes_direction(m, direction)
        ])
        attempted = 0
        executed = 0
        total_usd_spent = 0.0
        execution_errors = []

    # Structured report for automaton
    if os.environ.get("AUTOMATON_MANAGED"):
        report = {"signals": signals, "trades_attempted": attempted, "trades_executed": executed, "amount_usd": round(total_usd_spent, 2)}
        if signals > 0 and executed == 0 and skip_reasons:
            report["skip_reason"] = ", ".join(dict.fromkeys(skip_reasons))
        # Always include skip-reason counts when any markets were filtered,
        # so operators can tune the right knob (e.g., loosen liquidity floor
        # if 'liquidity below floor' dominates).
        if skip_reasons:
            counts = {}
            for r in skip_reasons:
                counts[r] = counts.get(r, 0) + 1
            report["skip_reason_counts"] = counts
        if execution_errors:
            report["execution_errors"] = execution_errors
        print(json.dumps({"automaton": report}))
        _automaton_reported = True


if __name__ == "__main__":
    main()

    # Fallback report for automaton if main() returned early (no signal)
    if os.environ.get("AUTOMATON_MANAGED") and not _automaton_reported:
        print(json.dumps({"automaton": {"signals": 0, "trades_attempted": 0, "trades_executed": 0, "skip_reason": "no_signal"}}))
