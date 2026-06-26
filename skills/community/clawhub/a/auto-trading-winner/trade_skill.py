import argparse
import os
import sys
from dataclasses import dataclass
from typing import Any, Optional

from simmer_sdk import SimmerClient
from simmer_sdk.sizing import size_position


SKILL_SLUG = "auto-trading-winner"
TRADE_SOURCE = f"sdk:{SKILL_SLUG}"
_CLIENT: Optional[SimmerClient] = None


@dataclass
class Config:
    venue: str
    run_mode: str
    market_query: str
    min_price: float
    max_price: float
    max_markets: int
    candidate_limit: int
    fair_probability: float
    min_edge: float
    max_slippage_pct: float
    live: bool
    selected_candidate: Optional[int]
    auto_confirm_live: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cross-venue manual-selection trading skill")
    parser.add_argument("--live", action="store_true", help="Enable live or paper trades for this run")
    return parser.parse_args()


def getenv_str(name: str, default: str) -> str:
    value = os.getenv(name)
    return value.strip() if value is not None else default


def getenv_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None:
        return default
    return float(raw)


def getenv_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    return int(raw)


def getenv_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def maybe_int(name: str) -> Optional[int]:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return None
    return int(raw)


def load_config() -> Config:
    args = parse_args()
    venue = getenv_str("TRADING_VENUE", "sim").lower()
    if venue not in {"sim", "kalshi", "polymarket"}:
        raise ValueError("TRADING_VENUE must be one of 'sim', 'kalshi', or 'polymarket'")

    run_mode = getenv_str("RUN_MODE", "manual").lower()
    if run_mode not in {"manual", "auto"}:
        raise ValueError("RUN_MODE must be either 'manual' or 'auto'")

    min_price = getenv_float("MIN_PRICE", 0.30)
    max_price = getenv_float("MAX_PRICE", 0.70)
    if not 0.0 < min_price < max_price < 1.0:
        raise ValueError("MIN_PRICE and MAX_PRICE must satisfy 0 < MIN_PRICE < MAX_PRICE < 1")

    max_markets = getenv_int("MAX_MARKETS", 50)
    candidate_limit = getenv_int("CANDIDATE_LIMIT", 5)
    fair_probability = getenv_float("FAIR_PROBABILITY", 0.55)
    min_edge = getenv_float("MIN_EDGE", 0.03)
    max_slippage_pct = getenv_float("MAX_SLIPPAGE_PCT", 0.15)
    live = args.live or getenv_bool("SIMMER_ENABLE_LIVE", False)

    return Config(
        venue=venue,
        run_mode=run_mode,
        market_query=getenv_str("MARKET_QUERY", ""),
        min_price=min_price,
        max_price=max_price,
        max_markets=max_markets,
        candidate_limit=candidate_limit,
        fair_probability=fair_probability,
        min_edge=min_edge,
        max_slippage_pct=max_slippage_pct,
        live=live,
        selected_candidate=maybe_int("SELECT_CANDIDATE"),
        auto_confirm_live=getenv_bool("AUTO_CONFIRM_LIVE", False),
    )


def get_client(venue: str) -> SimmerClient:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = SimmerClient(api_key=os.environ["SIMMER_API_KEY"], venue=venue)
    return _CLIENT


def read_value(item: Any, key: str, default: Any = None) -> Any:
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)


def format_probability(value: float) -> str:
    return f"{value * 100:.1f}%"


def format_amount(value: float, venue: str) -> str:
    return f"{value:.2f} $SIM" if venue == "sim" else f"${value:.2f}"


def run_auto_redeem(client: SimmerClient) -> None:
    for result in client.auto_redeem():
        if result.get("success"):
            print(f"redeemed market={result.get('market_id')} tx={result.get('tx_hash')}")


def estimate_bankroll(client: SimmerClient, venue: str) -> float:
    briefing = client.get_briefing()
    venue_data = (briefing.get("venues") or {}).get(venue) or {}
    balance = venue_data.get("balance")
    if isinstance(balance, (int, float)):
        return float(balance)

    portfolio = client.get_portfolio(venue=venue)
    if isinstance(portfolio, dict):
        nested = portfolio.get(venue)
        if isinstance(nested, dict):
            nested_balance = nested.get("balance")
            if isinstance(nested_balance, (int, float)):
                return float(nested_balance)
        direct_balance = portfolio.get("balance")
        if isinstance(direct_balance, (int, float)):
            return float(direct_balance)

    return 10000.0 if venue == "sim" else 100.0


def should_skip_context(context: dict[str, Any], max_slippage_pct: float) -> str | None:
    discipline = context.get("discipline") or {}
    flip_flop_warning = discipline.get("flip_flop_warning")
    if isinstance(flip_flop_warning, str) and discipline.get("warning_level") == "severe":
        return flip_flop_warning

    slippage = context.get("slippage") or {}
    spread_pct = slippage.get("spread_pct", 0) or 0
    estimates = slippage.get("estimates") or []
    worst_slippage = max((estimate.get("slippage_pct", 0) or 0) for estimate in estimates) if estimates else 0
    if spread_pct > max_slippage_pct:
        return f"spread too high: {spread_pct:.2%}"
    if worst_slippage > max_slippage_pct:
        return f"slippage too high: {worst_slippage:.2%}"

    edge = context.get("edge") or {}
    if edge.get("recommendation") in {"SKIP", "HOLD"}:
        return f"edge recommends {edge.get('recommendation')}"

    warnings = context.get("warnings") or []
    for warning in warnings:
        if "RESOLVED" in str(warning).upper():
            return str(warning)
    return None


def decide_trade(current_yes_price: float, fair_yes_probability: float, min_edge: float) -> tuple[str | None, float, float]:
    yes_edge = fair_yes_probability - current_yes_price
    no_price = 1.0 - current_yes_price
    fair_no_probability = 1.0 - fair_yes_probability
    no_edge = fair_no_probability - no_price

    if yes_edge >= min_edge and yes_edge >= no_edge:
        return "yes", current_yes_price, yes_edge
    if no_edge >= min_edge:
        return "no", no_price, no_edge
    return None, 0.0, 0.0


def build_reasoning(question: str, side: str, market_price: float, fair_probability: float, volume_value: float) -> str:
    fair_side_probability = fair_probability if side == "yes" else 1.0 - fair_probability
    return (
        f"Volume-ranked candidate on '{question}': market price is {format_probability(market_price)}; "
        f"my fair value for {side.upper()} is {format_probability(fair_side_probability)}; "
        f"24h volume score is {volume_value:.2f}."
    )


def volume_value(market: Any) -> float:
    for key in ("volume_24h", "volume", "volume_usd", "liquidity"):
        value = read_value(market, key)
        if isinstance(value, (int, float)):
            return float(value)
    return 0.0


def ensure_kalshi_market_indexed(client: SimmerClient, ticker: str, url: str, cache: dict[str, str]) -> tuple[str | None, str | None]:
    if ticker in cache:
        return cache[ticker], None

    check = client.check_market_exists(ticker=ticker)
    market_id = check.get("market_id")
    if market_id:
        cache[ticker] = market_id
        return market_id, None

    result = client.import_kalshi_market(url)
    if result.get("status") in {"imported", "already_exists"} and result.get("market_id"):
        market_id = result["market_id"]
        cache[ticker] = market_id
        return market_id, None

    return None, result.get("error") or f"import status={result.get('status')}"


def discover_markets(client: SimmerClient, config: Config) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []

    if config.venue == "kalshi":
        discovered = client.list_importable_markets(venue="kalshi", q=config.market_query or None, limit=config.max_markets)
        for market in discovered:
            current_yes_price = float(read_value(market, "current_price", 0.0) or 0.0)
            if not (config.min_price <= current_yes_price <= config.max_price):
                continue
            candidates.append(
                {
                    "market_id": None,
                    "ticker": read_value(market, "ticker"),
                    "url": read_value(market, "url"),
                    "question": read_value(market, "question", "unknown market"),
                    "current_yes_price": current_yes_price,
                    "volume_value": volume_value(market),
                }
            )
        return candidates

    discovered = client.find_markets(config.market_query)
    for market in discovered[: config.max_markets]:
        market_id = read_value(market, "id") or read_value(market, "market_id")
        if not market_id:
            continue
        current_yes_price = read_value(market, "current_probability")
        if current_yes_price is None:
            current_yes_price = read_value(market, "external_price_yes", 0.0)
        current_yes_price = float(current_yes_price or 0.0)
        if not (config.min_price <= current_yes_price <= config.max_price):
            continue
        candidates.append(
            {
                "market_id": market_id,
                "ticker": read_value(market, "ticker"),
                "url": read_value(market, "url"),
                "question": read_value(market, "question", "unknown market"),
                "current_yes_price": current_yes_price,
                "volume_value": volume_value(market),
            }
        )
    return candidates


def choose_candidate_index(displayed_candidates: list[dict[str, Any]], config: Config) -> Optional[int]:
    if not displayed_candidates:
        return None

    print("Top candidates:")
    for index, candidate in enumerate(displayed_candidates, start=1):
        print(
            f"{index}. {candidate['question']} | price={format_probability(candidate['current_yes_price'])} | "
            f"volume={candidate['volume_value']:.2f} | ticker={candidate.get('ticker')} | market={candidate.get('market_id')}"
        )

    if config.selected_candidate is not None:
        chosen_index = config.selected_candidate
    elif config.run_mode == "auto":
        chosen_index = 1
    elif sys.stdin.isatty():
        raw = input("Choose a candidate to trade (1-5, blank to skip): ").strip()
        if not raw:
            return None
        chosen_index = int(raw)
    else:
        return None

    if chosen_index < 1 or chosen_index > len(displayed_candidates):
        raise ValueError(f"SELECT_CANDIDATE must be between 1 and {len(displayed_candidates)}")
    return chosen_index - 1


def validate_execution_mode(config: Config) -> None:
    if config.live and config.run_mode == "auto" and config.venue != "sim" and not config.auto_confirm_live:
        raise RuntimeError(
            "Automatic live execution is disabled for real-money venues. "
            "Use RUN_MODE=manual, or keep RUN_MODE=auto with dry-run, or explicitly set AUTO_CONFIRM_LIVE=true."
        )


def main() -> None:
    config = load_config()
    validate_execution_mode(config)
    client = get_client(config.venue)
    index_cache: dict[str, str] = {}

    print(f"skill={SKILL_SLUG} venue={config.venue} mode={config.run_mode} live={config.live}")
    print(
        f"query={config.market_query!r} price_band={config.min_price:.2f}-{config.max_price:.2f} "
        f"candidate_limit={config.candidate_limit}"
    )

    run_auto_redeem(client)
    bankroll = estimate_bankroll(client, config.venue)
    print(f"bankroll={format_amount(bankroll, config.venue)}")

    candidates = discover_markets(client, config)
    candidates.sort(key=lambda item: item["volume_value"], reverse=True)

    if not candidates:
        print("No candidates matched the price-band and volume filters.")
        return

    displayed_candidates = candidates[: config.candidate_limit]
    if len(candidates) > len(displayed_candidates):
        print(f"displaying top {len(displayed_candidates)} of {len(candidates)} ranked candidates")

    selected_index = choose_candidate_index(displayed_candidates, config)
    if selected_index is None:
        print("No candidate selected. Set RUN_MODE=auto or SELECT_CANDIDATE to enable unattended runs.")
        return

    for rank, selected in enumerate(candidates[selected_index:], start=selected_index + 1):
        market_id = selected.get("market_id")
        try:
            if config.venue == "kalshi":
                ticker = selected.get("ticker")
                url = selected.get("url")
                if not ticker or not url:
                    raise ValueError("Selected Kalshi candidate is missing ticker or url")
                market_id, error = ensure_kalshi_market_indexed(client, ticker, url, index_cache)
                if not market_id:
                    raise RuntimeError(f"Could not index Kalshi market: {error}")

            if not market_id:
                raise RuntimeError("Selected market has no market_id")

            context = client.get_market_context(market_id, venue=config.venue, my_probability=config.fair_probability)
            skip_reason = should_skip_context(context, config.max_slippage_pct)
            if skip_reason:
                raise RuntimeError(skip_reason)

            market_data = context.get("market") or {}
            live_yes_price = market_data.get("current_price")
            if live_yes_price is None:
                live_yes_price = market_data.get("current_probability")
            live_yes_price = float(live_yes_price if live_yes_price is not None else selected["current_yes_price"])

            side, market_price, edge = decide_trade(live_yes_price, config.fair_probability, config.min_edge)
            if side is None:
                raise RuntimeError("market no longer meets the minimum edge threshold")

            p_win = config.fair_probability if side == "yes" else 1.0 - config.fair_probability
            amount = round(
                float(size_position(p_win=p_win, market_price=market_price, bankroll=bankroll, min_ev=config.min_edge)),
                2,
            )
            if amount <= 0:
                raise RuntimeError("sizing returned zero")

            reasoning = build_reasoning(selected["question"], side, market_price, config.fair_probability, selected["volume_value"])
            print(
                f"selected rank={rank} market={market_id} side={side} amount={format_amount(amount, config.venue)} "
                f"price={format_probability(market_price)} edge={format_probability(edge)}"
            )

            if not config.live:
                print(f"dry-run trade reasoning={reasoning}")
                return

            result = client.trade(
                market_id=market_id,
                side=side,
                amount=amount,
                venue=config.venue,
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                reasoning=reasoning,
            )
            shares = read_value(result, "shares_bought", 0)
            print(f"executed market={market_id} shares={shares}")
            return
        except Exception as exc:
            print(f"candidate rank={rank} skipped: {exc}")

    print("No selectable candidates passed indexing and safeguard checks.")


if __name__ == "__main__":
    main()