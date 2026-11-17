#!/usr/bin/env python3
"""Backtest dollar-cost averaging vs lump-sum investing using free CoinGecko historical price data."""

import argparse
import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone

COINGECKO_BASE = "https://api.coingecko.com/api/v3"

# CoinGecko free tier: daily granularity is auto-selected by the API for
# ranges > 90 days, and max lookback for the free public endpoint is 365 days.
MAX_DAYS = 365


def fetch_daily_prices(coin_id, days):
    days = min(days, MAX_DAYS)
    url = f"{COINGECKO_BASE}/coins/{urllib.parse.quote(coin_id)}/market_chart?vs_currency=usd&days={days}&interval=daily"
    req = urllib.request.Request(url, headers={"User-Agent": "curl/8.0"})
    with urllib.request.urlopen(req, timeout=25) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if "prices" not in data:
        raise RuntimeError(f"Unexpected response for coin_id={coin_id}: {data}")
    # [[ms_timestamp, price], ...]
    return [(ts / 1000.0, price) for ts, price in data["prices"]]


def sample_weekly(prices):
    """Downsample daily price series to ~weekly points (every 7th day) for a weekly-DCA simulation."""
    return prices[::7] if len(prices) > 7 else prices


def simulate_dca(prices, contribution_per_period):
    total_invested = 0.0
    total_units = 0.0
    for _, price in prices:
        if price <= 0:
            continue
        total_invested += contribution_per_period
        total_units += contribution_per_period / price
    return total_invested, total_units


def simulate_lump_sum(prices, total_capital):
    first_price = next((p for _, p in prices if p > 0), None)
    if first_price is None:
        raise RuntimeError("No valid price points to lump-sum invest at")
    units = total_capital / first_price
    return total_capital, units


def backtest(coin_id, days, weekly_contribution):
    daily_prices = fetch_daily_prices(coin_id, days)
    if len(daily_prices) < 2:
        raise RuntimeError("Not enough price history returned")

    weekly_prices = sample_weekly(daily_prices)
    final_price = daily_prices[-1][1]

    dca_invested, dca_units = simulate_dca(weekly_prices, weekly_contribution)
    dca_value = dca_units * final_price
    dca_return_pct = ((dca_value - dca_invested) / dca_invested) * 100 if dca_invested else 0.0

    total_capital = weekly_contribution * len(weekly_prices)
    ls_invested, ls_units = simulate_lump_sum(daily_prices, total_capital)
    ls_value = ls_units * final_price
    ls_return_pct = ((ls_value - ls_invested) / ls_invested) * 100 if ls_invested else 0.0

    start_dt = datetime.fromtimestamp(daily_prices[0][0], tz=timezone.utc).date().isoformat()
    end_dt = datetime.fromtimestamp(daily_prices[-1][0], tz=timezone.utc).date().isoformat()

    return {
        "coin_id": coin_id,
        "period": {"start": start_dt, "end": end_dt, "days": len(daily_prices)},
        "final_price_usd": round(final_price, 2),
        "dca": {
            "num_contributions": len(weekly_prices),
            "contribution_per_week_usd": weekly_contribution,
            "total_invested_usd": round(dca_invested, 2),
            "units_bought": round(dca_units, 8),
            "end_value_usd": round(dca_value, 2),
            "return_pct": round(dca_return_pct, 2),
        },
        "lump_sum": {
            "total_invested_usd": round(ls_invested, 2),
            "units_bought": round(ls_units, 8),
            "end_value_usd": round(ls_value, 2),
            "return_pct": round(ls_return_pct, 2),
        },
        "winner": "dca" if dca_return_pct > ls_return_pct else ("lump_sum" if ls_return_pct > dca_return_pct else "tie"),
    }


def main():
    ap = argparse.ArgumentParser(description="Backtest DCA vs lump-sum investing on historical crypto prices (CoinGecko, free)")
    ap.add_argument("--coin", type=str, default="bitcoin", help="CoinGecko coin id, e.g. bitcoin, ethereum, solana")
    ap.add_argument("--days", type=int, default=365, help=f"Lookback window in days (max {MAX_DAYS} on the free API)")
    ap.add_argument("--weekly-contribution", type=float, default=100.0, help="USD contributed per week in the DCA leg")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    try:
        result = backtest(args.coin, args.days, args.weekly_contribution)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        raise SystemExit(1)

    if args.json:
        print(json.dumps(result, indent=2))
        return

    p = result["period"]
    print(f"{result['coin_id'].upper()} backtest: {p['start']} -> {p['end']} ({p['days']} days)")
    print(f"Final price: ${result['final_price_usd']:,.2f}\n")

    d = result["dca"]
    print(f"DCA (${d['contribution_per_week_usd']:.0f}/week x {d['num_contributions']} weeks):")
    print(f"  Invested: ${d['total_invested_usd']:,.2f}  ->  End value: ${d['end_value_usd']:,.2f}  ({d['return_pct']:+.2f}%)\n")

    ls = result["lump_sum"]
    print(f"Lump sum (same total capital, invested on day 1):")
    print(f"  Invested: ${ls['total_invested_usd']:,.2f}  ->  End value: ${ls['end_value_usd']:,.2f}  ({ls['return_pct']:+.2f}%)\n")

    print(f"Winner over this period: {result['winner'].replace('_', ' ').upper()}")
    print("\nNote: this compares two strategies over one specific historical window using the same total capital. "
          "Past performance says nothing about future returns — DCA's real benefit is reducing timing risk and "
          "volatility exposure, which this return-only comparison doesn't fully capture. Not financial advice.")


if __name__ == "__main__":
    main()
