#!/usr/bin/env python3
"""
Crypto CLI - Command-line interface for crypto data and technical analysis.

Usage:
    python cli.py <command> [options]

Commands:
    candles <inst_id> [--bar BAR] [--limit LIMIT]
        Get K-line/OHLCV data

    funding-rate <inst_id> [--limit LIMIT]
        Get funding rate for perpetual contracts

    open-interest <inst_id> [--period PERIOD] [--limit LIMIT]
        Get open interest data

    long-short-ratio <ccy> [--period PERIOD] [--limit LIMIT]
        Get elite trader long/short account ratio

    liquidation <inst_id> [--state STATE] [--limit LIMIT]
        Get liquidation orders

    top-trader-ratio <inst_id> [--period PERIOD] [--limit LIMIT]
        Get top 5% traders long/short position ratio

    option-ratio <ccy> [--period PERIOD]
        Get option call/put OI and volume ratio

    fear-greed [--days DAYS]
        Get Fear and Greed Index

    indicators <inst_id> [--bar BAR] [--limit LIMIT] [--last-n N]
        Get complete technical indicators (MA, RSI, MACD, KDJ, etc.)

    summary <inst_id> [--bar BAR] [--limit LIMIT]
        Get technical analysis summary

    support-resistance <inst_id> [--bar BAR] [--limit LIMIT] [--window N]
        Get support/resistance levels and Fibonacci retracement

Examples:
    python cli.py candles BTC-USDT --bar 1H --limit 100
    python cli.py funding-rate BTC-USDT-SWAP --limit 50
    python cli.py indicators ETH-USDT --bar 4H --last-n 5
    python cli.py fear-greed --days 30
"""

import argparse
import json
import sys
import math
from typing import Any, Dict, List, Optional

from crypto_data import (
    get_okx_candles,
    get_okx_funding_rate,
    get_okx_open_interest,
    get_long_short_ratio,
    get_okx_liquidation,
    get_top_trader_long_short_position_ratio,
    get_option_open_interest_volume_ratio,
    get_fear_greed_index,
)

from technical_analysis import TechnicalAnalysis, _analyze_single_asset


# ==============================================================================
# Utility functions
# ==============================================================================


def _clean_value(v: Any) -> Any:
    """Convert any value to JSON-serializable Python native type."""
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if hasattr(v, "item"):
        v = v.item()
    if isinstance(v, float):
        if math.isnan(v) or math.isinf(v):
            return None
        return round(v, 8)
    if isinstance(v, (int, str, bool)):
        return v
    return str(v)


def _clean_record(record: dict) -> dict:
    """Clean a single dict row."""
    return {k: _clean_value(v) for k, v in record.items()}


def _clean_df_to_records(df) -> List[dict]:
    """DataFrame -> list[dict], full cleaning."""
    if df is None or df.empty:
        return []
    return [_clean_record(row) for row in df.to_dict(orient="records")]


def _clean_any(obj: Any) -> Any:
    """Recursively clean any nested structure."""
    if isinstance(obj, dict):
        return {k: _clean_any(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_clean_any(i) for i in obj]
    return _clean_value(obj)


def output_json(data: Any) -> None:
    """Output JSON to stdout."""
    print(json.dumps(_clean_any(data), indent=2, ensure_ascii=False))


def output_error(message: str) -> None:
    """Output error as JSON."""
    print(json.dumps({"error": message}, indent=2))


# ==============================================================================
# Command handlers
# ==============================================================================


def cmd_candles(args) -> None:
    """Get K-line data."""
    df = get_okx_candles(
        inst_id=args.inst_id,
        bar=args.bar,
        limit=args.limit,
    )
    if df is not None:
        records = _clean_df_to_records(df)
        output_json(records)
    else:
        output_error(f"Failed to fetch candle data for {args.inst_id}")


def cmd_funding_rate(args) -> None:
    """Get funding rate."""
    df = get_okx_funding_rate(
        inst_id=args.inst_id,
        limit=args.limit,
    )
    if df is not None:
        records = _clean_df_to_records(df)
        output_json(records)
    else:
        output_error(f"Failed to fetch funding rate for {args.inst_id}")


def cmd_open_interest(args) -> None:
    """Get open interest."""
    df = get_okx_open_interest(
        inst_id=args.inst_id,
        period=args.period,
        limit=args.limit,
    )
    if df is not None:
        records = _clean_df_to_records(df)
        output_json(records)
    else:
        output_error(f"Failed to fetch open interest for {args.inst_id}")


def cmd_long_short_ratio(args) -> None:
    """Get long/short ratio."""
    df = get_long_short_ratio(
        ccy=args.ccy,
        period=args.period,
        limit=args.limit,
    )
    if df is not None:
        records = _clean_df_to_records(df)
        output_json(records)
    else:
        output_error(f"Failed to fetch long/short ratio for {args.ccy}")


def cmd_liquidation(args) -> None:
    """Get liquidation orders."""
    df = get_okx_liquidation(
        inst_id=args.inst_id,
        state=args.state,
        limit=args.limit,
    )
    if df is not None:
        records = _clean_df_to_records(df)
        output_json(records)
    else:
        output_error(f"Failed to fetch liquidation data for {args.inst_id}")


def cmd_top_trader_ratio(args) -> None:
    """Get top trader position ratio."""
    df = get_top_trader_long_short_position_ratio(
        inst_id=args.inst_id,
        period=args.period,
        limit=args.limit,
    )
    if df is not None:
        records = _clean_df_to_records(df)
        output_json(records)
    else:
        output_error(f"Failed to fetch top trader ratio for {args.inst_id}")


def cmd_option_ratio(args) -> None:
    """Get option OI/volume ratio."""
    df = get_option_open_interest_volume_ratio(
        ccy=args.ccy,
        period=args.period,
        limit=args.limit,
    )
    if df is not None:
        records = _clean_df_to_records(df)
        output_json(records)
    else:
        output_error(f"Failed to fetch option ratio for {args.ccy}")


def cmd_fear_greed(args) -> None:
    """Get Fear and Greed Index."""
    df = get_fear_greed_index(days=args.days)
    if df is not None:
        records = _clean_df_to_records(df)
        output_json(records)
    else:
        output_error("Failed to fetch Fear and Greed Index")


def cmd_indicators(args) -> None:
    """Get complete technical indicators."""
    # Fetch candles first
    df = get_okx_candles(
        inst_id=args.inst_id,
        bar=args.bar,
        limit=args.limit,
    )
    if df is None or df.empty:
        output_error(f"Failed to fetch candle data for {args.inst_id}")
        return

    # Convert to records for TechnicalAnalysis
    kline_data = df.to_dict(orient="records")
    for row in kline_data:
        row["datetime"] = str(row["datetime"])

    # Calculate indicators
    ta = TechnicalAnalysis(kline_data=kline_data, inst_id=args.inst_id, bar=args.bar)
    if ta.data.empty:
        output_error(f"K-line data for {args.inst_id} is empty")
        return

    indicators_df = ta.get_all_indicators()
    if args.last_n > 0:
        indicators_df = indicators_df.tail(args.last_n)

    records = _clean_df_to_records(indicators_df)
    output_json(records)


def cmd_summary(args) -> None:
    """Get technical analysis summary."""
    # Fetch candles first
    df = get_okx_candles(
        inst_id=args.inst_id,
        bar=args.bar,
        limit=args.limit,
    )
    if df is None or df.empty:
        output_error(f"Failed to fetch candle data for {args.inst_id}")
        return

    # Convert to records for TechnicalAnalysis
    kline_data = df.to_dict(orient="records")
    for row in kline_data:
        row["datetime"] = str(row["datetime"])

    # Calculate and summarize
    ta = TechnicalAnalysis(kline_data=kline_data, inst_id=args.inst_id, bar=args.bar)
    if ta.data.empty:
        output_error(f"K-line data for {args.inst_id} is empty")
        return

    result = _analyze_single_asset(ta, args.inst_id)
    if result is None:
        output_error("Analysis failed, insufficient data")
        return

    output_json(result)


def cmd_support_resistance(args) -> None:
    """Get support/resistance levels."""
    # Fetch candles first
    df = get_okx_candles(
        inst_id=args.inst_id,
        bar=args.bar,
        limit=args.limit,
    )
    if df is None or df.empty:
        output_error(f"Failed to fetch candle data for {args.inst_id}")
        return

    # Convert to records for TechnicalAnalysis
    kline_data = df.to_dict(orient="records")
    for row in kline_data:
        row["datetime"] = str(row["datetime"])

    # Calculate support/resistance
    ta = TechnicalAnalysis(kline_data=kline_data, inst_id=args.inst_id, bar=args.bar)
    if ta.data.empty:
        output_error(f"K-line data for {args.inst_id} is empty")
        return

    support, resistance = ta.find_support_resistance(window=args.window)
    high_price = float(ta.data["high"].max())
    low_price = float(ta.data["low"].min())
    curr_price = float(ta.data["close"].iloc[-1])
    fib = ta.calculate_fibonacci_retracement(high_price, low_price)

    result = {
        "inst_id": args.inst_id,
        "bar": args.bar,
        "current_price": _clean_value(curr_price),
        "support_levels": [_clean_value(v) for v in sorted(support, reverse=True)],
        "resistance_levels": [
            _clean_value(v) for v in sorted(resistance, reverse=True)
        ],
        "fibonacci_retracement": {k: _clean_value(v) for k, v in fib.items()},
        "price_range": {
            "high": _clean_value(high_price),
            "low": _clean_value(low_price),
        },
    }
    output_json(result)


# ==============================================================================
# Main CLI
# ==============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Crypto Data CLI - Fetch market data and technical analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s candles BTC-USDT --bar 1H --limit 100
  %(prog)s funding-rate BTC-USDT-SWAP --limit 50
  %(prog)s indicators ETH-USDT --bar 4H --last-n 5
  %(prog)s fear-greed --days 30
  %(prog)s support-resistance BTC-USDT --bar 1D
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # candles
    p_candles = subparsers.add_parser("candles", help="Get K-line/OHLCV data")
    p_candles.add_argument("inst_id", help="Trading pair, e.g., BTC-USDT")
    p_candles.add_argument(
        "--bar",
        default="1H",
        help="K-line period: 1m,5m,15m,30m,1H,4H,1D,1W (default: 1H)",
    )
    p_candles.add_argument(
        "--limit", type=int, default=100, help="Number of data points (default: 100)"
    )
    p_candles.set_defaults(func=cmd_candles)

    # funding-rate
    p_funding = subparsers.add_parser(
        "funding-rate", help="Get funding rate for perpetual contracts"
    )
    p_funding.add_argument("inst_id", help="Perpetual contract, e.g., BTC-USDT-SWAP")
    p_funding.add_argument(
        "--limit", type=int, default=100, help="Number of data points (default: 100)"
    )
    p_funding.set_defaults(func=cmd_funding_rate)

    # open-interest
    p_oi = subparsers.add_parser("open-interest", help="Get open interest data")
    p_oi.add_argument("inst_id", help="Perpetual contract, e.g., BTC-USDT-SWAP")
    p_oi.add_argument(
        "--period", default="1H", help="Time granularity: 5m,1H,1D (default: 1H)"
    )
    p_oi.add_argument(
        "--limit", type=int, default=100, help="Number of data points (default: 100)"
    )
    p_oi.set_defaults(func=cmd_open_interest)

    # long-short-ratio
    p_ls = subparsers.add_parser(
        "long-short-ratio", help="Get elite trader long/short account ratio"
    )
    p_ls.add_argument("ccy", help="Currency, e.g., BTC, ETH")
    p_ls.add_argument(
        "--period", default="1H", help="Time granularity: 5m,1H,1D (default: 1H)"
    )
    p_ls.add_argument(
        "--limit", type=int, default=100, help="Number of data points (default: 100)"
    )
    p_ls.set_defaults(func=cmd_long_short_ratio)

    # liquidation
    p_liq = subparsers.add_parser("liquidation", help="Get liquidation orders")
    p_liq.add_argument("inst_id", help="Perpetual contract, e.g., BTC-USDT-SWAP")
    p_liq.add_argument(
        "--state",
        default="filled",
        help="Order state: filled, unfilled (default: filled)",
    )
    p_liq.add_argument(
        "--limit", type=int, default=100, help="Number of data points (default: 100)"
    )
    p_liq.set_defaults(func=cmd_liquidation)

    # top-trader-ratio
    p_top = subparsers.add_parser(
        "top-trader-ratio", help="Get top 5%% traders long/short position ratio"
    )
    p_top.add_argument("inst_id", help="Perpetual contract, e.g., BTC-USDT-SWAP")
    p_top.add_argument("--period", default="5m", help="Time granularity (default: 5m)")
    p_top.add_argument(
        "--limit", type=int, default=100, help="Number of data points (default: 100)"
    )
    p_top.set_defaults(func=cmd_top_trader_ratio)

    # option-ratio
    p_opt = subparsers.add_parser(
        "option-ratio", help="Get option call/put OI and volume ratio"
    )
    p_opt.add_argument("ccy", help="Currency, e.g., BTC, ETH")
    p_opt.add_argument(
        "--period", default="8H", help="Time granularity: 8H,1D (default: 8H)"
    )
    p_opt.add_argument(
        "--limit", type=int, default=100, help="Number of data points (default: 100)"
    )
    p_opt.set_defaults(func=cmd_option_ratio)

    # fear-greed
    p_fg = subparsers.add_parser("fear-greed", help="Get Fear and Greed Index")
    p_fg.add_argument(
        "--days", type=int, default=7, help="Days of history (default: 7)"
    )
    p_fg.set_defaults(func=cmd_fear_greed)

    # indicators
    p_ind = subparsers.add_parser(
        "indicators", help="Get complete technical indicators"
    )
    p_ind.add_argument("inst_id", help="Trading pair, e.g., BTC-USDT")
    p_ind.add_argument("--bar", default="1D", help="K-line period (default: 1D)")
    p_ind.add_argument(
        "--limit", type=int, default=100, help="Number of K-lines (default: 100)"
    )
    p_ind.add_argument(
        "--last-n",
        type=int,
        default=10,
        help="Return only latest N rows (default: 10, 0=all)",
    )
    p_ind.set_defaults(func=cmd_indicators)

    # summary
    p_sum = subparsers.add_parser("summary", help="Get technical analysis summary")
    p_sum.add_argument("inst_id", help="Trading pair, e.g., BTC-USDT")
    p_sum.add_argument("--bar", default="1D", help="K-line period (default: 1D)")
    p_sum.add_argument(
        "--limit", type=int, default=100, help="Number of K-lines (default: 100)"
    )
    p_sum.set_defaults(func=cmd_summary)

    # support-resistance
    p_sr = subparsers.add_parser(
        "support-resistance", help="Get support/resistance levels"
    )
    p_sr.add_argument("inst_id", help="Trading pair, e.g., BTC-USDT")
    p_sr.add_argument("--bar", default="1D", help="K-line period (default: 1D)")
    p_sr.add_argument(
        "--limit", type=int, default=100, help="Number of K-lines (default: 100)"
    )
    p_sr.add_argument(
        "--window",
        type=int,
        default=5,
        help="Window size for finding extrema (default: 5)",
    )
    p_sr.set_defaults(func=cmd_support_resistance)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
