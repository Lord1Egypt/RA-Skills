from __future__ import annotations

import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable, Optional
from urllib.request import urlopen


BINANCE_URL = "https://api.binance.us/api/v3/klines"


@dataclass
class SignalDecision:
    action: str
    edge: float
    confidence: float
    signal_source: str
    reasoning: str
    metrics: dict

    def to_signal_data(self) -> dict:
        data = {
            "edge": round(self.edge, 4),
            "confidence": round(self.confidence, 4),
            "signal_source": self.signal_source,
        }
        for key, value in self.metrics.items():
            if isinstance(value, float):
                data[key] = round(value, 6)
            else:
                data[key] = value
        return data


def fetch_binance_klines(symbol: str = "BTCUSDT", interval: str = "1m", limit: int = 30) -> list[dict]:
    url = f"{BINANCE_URL}?symbol={symbol}&interval={interval}&limit={limit}"
    with urlopen(url, timeout=10) as resp:
        raw = json.loads(resp.read().decode())
    klines = []
    for row in raw:
        klines.append(
            {
                "open_time": int(row[0]),
                "open": float(row[1]),
                "high": float(row[2]),
                "low": float(row[3]),
                "close": float(row[4]),
                "volume": float(row[5]),
            }
        )
    return klines


def _pct_change(a: float, b: float) -> float:
    if a == 0:
        return 0.0
    return (b - a) / a


def _realized_volatility(closes: Iterable[float]) -> float:
    closes = list(closes)
    if len(closes) < 2:
        return 0.0
    moves = [_pct_change(closes[i], closes[i + 1]) for i in range(len(closes) - 1)]
    mean = sum(moves) / len(moves)
    variance = sum((move - mean) ** 2 for move in moves) / len(moves)
    return math.sqrt(variance)


def fallback_signal_from_context(context: dict, min_edge: float) -> SignalDecision:
    market = context.get("market", {})
    external_price = market.get("external_price")
    current_probability = market.get("current_probability")
    divergence = market.get("divergence")
    if external_price is None or current_probability is None:
        return SignalDecision(
            action="hold",
            edge=0.0,
            confidence=0.5,
            signal_source="context_fallback",
            reasoning="No Binance signal and insufficient context for fallback signal.",
            metrics={"divergence": divergence or 0.0},
        )

    diff = external_price - current_probability
    edge = abs(diff)
    action = "yes" if diff > 0 else "no" if diff < 0 else "hold"
    confidence = min(0.9, 0.55 + edge * 4)
    if edge < min_edge:
        action = "hold"
    return SignalDecision(
        action=action,
        edge=edge,
        confidence=confidence,
        signal_source="context_fallback",
        reasoning=f"Fallback signal from external/current price divergence ({diff:+.4f}).",
        metrics={"divergence": diff},
    )


def build_signal(window: str, context: dict, symbol: str = "BTCUSDT", interval: str = "1m", min_edge: float = 0.07) -> SignalDecision:
    try:
        klines = fetch_binance_klines(symbol=symbol, interval=interval, limit=30)
    except Exception as exc:
        fallback = fallback_signal_from_context(context, min_edge=min_edge)
        fallback.reasoning += f" Binance fetch failed: {exc}."
        return fallback

    closes = [row["close"] for row in klines]
    short_window = 3 if window == "5m" else 5
    long_window = 8 if window == "5m" else 13
    short_move = _pct_change(closes[-short_window], closes[-1])
    long_move = _pct_change(closes[-long_window], closes[-1])
    volatility = _realized_volatility(closes[-long_window:])
    combined_move = (short_move * 0.6) + (long_move * 0.4)
    edge = max(0.0, min(0.2, abs(combined_move) * 22))
    confidence = max(0.5, min(0.95, 0.58 + abs(combined_move) * 18 - volatility * 8))

    if edge < min_edge:
        action = "hold"
    else:
        action = "yes" if combined_move > 0 else "no"

    direction = "up" if combined_move > 0 else "down" if combined_move < 0 else "flat"
    reasoning = (
        f"{window} momentum from Binance {symbol} is {direction}: short_move={short_move:+.4f}, "
        f"long_move={long_move:+.4f}, vol={volatility:.4f}."
    )
    return SignalDecision(
        action=action,
        edge=edge,
        confidence=confidence,
        signal_source="binance_1m_momentum",
        reasoning=reasoning,
        metrics={
            "window": window,
            "short_move": short_move,
            "long_move": long_move,
            "volatility": volatility,
            "computed_at": datetime.now(timezone.utc).isoformat(),
        },
    )
