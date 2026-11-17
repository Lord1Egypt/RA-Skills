"""No-key Hyperliquid perpetual context and its explicit oracle price reference.

Hyperliquid's public API provides BTC/ETH perpetuals and an oracle/index price.
It does not currently provide a liquid native BTC or ETH spot market suitable for
using as an exchange-spot quote.  Keep that distinction in the output: the
oracle is a reference price for perp basis, never a fabricated spot BBO.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from urllib.request import Request, urlopen

from market_analytics import price_level_dossier, realized_volatility_dossier

INFO = "https://api.hyperliquid.xyz/info"


def info(payload):
    request = Request(INFO, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json", "User-Agent": "crypto-market-strategist/0.1"})
    with urlopen(request, timeout=30) as response:  # noqa: S310
        return json.load(response)


def candles(asset, interval, days):
    end = int(datetime.now(timezone.utc).timestamp() * 1000)
    rows = info({"type": "candleSnapshot", "req": {"coin": asset, "interval": interval, "startTime": end - days * 86_400_000, "endTime": end}})
    return [{"open_time": datetime.fromtimestamp(int(row["t"]) / 1000, timezone.utc).isoformat(), "open": float(row["o"]), "high": float(row["h"]), "low": float(row["l"]), "close": float(row["c"]), "volume": float(row["v"]), "trade_count": int(row["n"])} for row in rows]


def sma(values, length):
    return sum(values[-length:]) / length if len(values) >= length else None


def rsi(values, length=14):
    changes = [values[index] - values[index - 1] for index in range(1, len(values))][-length:]
    if len(changes) < length:
        return None
    gains, losses = sum(max(x, 0) for x in changes) / length, sum(max(-x, 0) for x in changes) / length
    return 100.0 if not losses else 100 - 100 / (1 + gains / losses)


def run(asset):
    asset = asset.upper()
    if asset not in {"BTC", "ETH"}:
        raise ValueError("Perpetual context supports BTC and ETH only.")
    daily, four_hour = candles(asset, "1d", 200), candles(asset, "4h", 30)
    universe, contexts = info({"type": "metaAndAssetCtxs"})
    index = next(index for index, item in enumerate(universe["universe"]) if item["name"] == asset)
    current = contexts[index]
    end = int(datetime.now(timezone.utc).timestamp() * 1000)
    funding_history = info({"type": "fundingHistory", "coin": asset, "startTime": end - 30 * 86_400_000, "endTime": end})
    funding = [float(row["fundingRate"]) for row in funding_history if row.get("fundingRate") is not None]
    average = sum(funding) / len(funding) if funding else None
    closes = [row["close"] for row in daily]
    last = closes[-1]
    def change(days): return (last / closes[-days - 1] - 1) * 100 if len(closes) > days else None
    mark, oracle = float(current["markPx"]), float(current["oraclePx"])
    # Hyperliquid funding is an hourly rate. Annualization is intentionally a
    # simple convention, not a tradable yield forecast.
    volatility = realized_volatility_dossier(daily)
    levels = price_level_dossier(daily, four_hour)
    realized_30d = next((row["close_to_close_pct"] for row in volatility.get("estimators", []) if row["window_days"] == 30), None)
    return {
        "asset": asset,
        "as_of": datetime.now(timezone.utc).isoformat(),
        "source": "Hyperliquid public Info API: perpetual candles, meta/asset context, funding history",
        "spot_reference": {
            "status": "reference_only",
            "venue": "Hyperliquid",
            "reference_type": "perpetual_oracle_index",
            "price_usd": oracle,
            "is_tradable_spot_quote": False,
            "use": "Use only as the same-venue reference price for the Hyperliquid perpetual basis.",
        },
        "native_spot_market": {
            "status": "unavailable",
            "reason": "No liquid native BTC/USDC or ETH/USDC spot market was found in Hyperliquid spot metadata; do not synthesize a spot BBO.",
        },
        "daily_ohlcv": daily,
        "four_hour_ohlcv": four_hour,
        "technical_snapshot": {"price_series": "Hyperliquid perpetual close", "perpetual_close": last, "return_1d_pct": change(1), "return_7d_pct": change(7), "return_30d_pct": change(30), "sma_20": sma(closes, 20), "sma_50": sma(closes, 50), "sma_200": sma(closes, 200), "rsi_14": rsi(closes), "realized_vol_30d_pct": realized_30d},
        "realized_volatility_dossier": volatility,
        "price_level_dossier": levels,
        "perp_snapshot": {"venue": "Hyperliquid", "instrument": f"{asset}-PERP", "mark_price": mark, "basis_reference": "Hyperliquid perpetual oracle index", "oracle_price": oracle, "mark_oracle_basis_pct": (mark / oracle - 1) * 100, "open_interest_contracts": float(current["openInterest"]), "volume_24h_usd": float(current["dayNtlVlm"]), "current_funding_1h_pct": float(current["funding"]) * 100, "current_funding_annualized_simple_pct": float(current["funding"]) * 24 * 365 * 100, "average_funding_1h_30d_pct": average * 100 if average is not None else None, "average_funding_annualized_simple_30d_pct": average * 24 * 365 * 100 if average is not None else None, "funding_history_observations": len(funding)},
        "limitations": ["This is Hyperliquid venue-level perpetual data, not aggregate market data.", "Funding annualization is simple (hourly rate × 24 × 365), not a guaranteed return.", "The oracle is a reference/index price, not a tradable Hyperliquid BTC/ETH spot quote.", "Hyperliquid reference prices and Polymarket's stated rule source can differ."],
    }
