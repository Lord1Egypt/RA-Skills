#!/usr/bin/env python3
import json
import os
import statistics
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests


ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config.json"
DEFAULT_TIMEOUT = 10
DISCORD_API_BASE = "https://discord.com/api/v10"


DEFAULT_CONFIG: dict[str, Any] = {
    "coins": [
        {"symbol": "BTCUSDT", "name": "Bitcoin", "coingecko_id": "bitcoin"},
        {"symbol": "ETHUSDT", "name": "Ethereum", "coingecko_id": "ethereum"},
    ],
    "binance": {
        "interval": "1w",
        "limit": 100,
        "quote_currency": "USDT",
    },
    "thresholds": {
        "rsi_max": 30.0,
        "volume_ratio_max": 0.7,
        "fear_greed_max": 25,
        "mvrv_proxy_max": 1.0,
        "lower_band_buffer": 1.05,
    },
    "discord": {
        "enabled": False,
        "token_env": "DISCORD_TOKEN",
        "channel_id": "",
        "mention_user_id": "",
    },
    "schedule": "0 8 * * *",
    "runtime": {
        "request_timeout_seconds": DEFAULT_TIMEOUT,
    },
}


class MonitorError(RuntimeError):
    pass


@dataclass
class CoinReport:
    symbol: str
    name: str
    price: float
    price_change_pct: float | None
    rsi: float | None
    macd: float | None
    macd_signal: float | None
    macd_histogram: float | None
    bollinger_upper: float | None
    bollinger_middle: float | None
    bollinger_lower: float | None
    volume_ratio: float | None
    support: float | None
    resistance: float | None
    fear_greed: int | None
    market_cap: float | None
    volume_24h: float | None
    ath: float | None
    atl: float | None
    mvrv_proxy: float | None
    signals: list[str]


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    if not path.exists():
        return DEFAULT_CONFIG
    with path.open("r", encoding="utf-8") as handle:
        user_config = json.load(handle)
    return deep_merge(DEFAULT_CONFIG, user_config)


def request_json(url: str, *, params: dict[str, Any] | None = None, timeout: int = DEFAULT_TIMEOUT) -> Any:
    response = requests.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()


def post_json(url: str, *, headers: dict[str, str], payload: dict[str, Any], timeout: int = DEFAULT_TIMEOUT) -> Any:
    response = requests.post(url, headers=headers, json=payload, timeout=timeout)
    response.raise_for_status()
    return response.json()


def get_binance_klines(symbol: str, interval: str, limit: int, timeout: int) -> list[list[Any]]:
    return request_json(
        "https://api.binance.com/api/v3/klines",
        params={"symbol": symbol, "interval": interval, "limit": limit},
        timeout=timeout,
    )


def get_bybit_klines(symbol: str, limit: int, timeout: int) -> list[list[Any]]:
    data = request_json(
        "https://api.bybit.com/v5/market/kline",
        params={"category": "linear", "symbol": symbol, "interval": "W", "limit": limit},
        timeout=timeout,
    )
    rows = data.get("result", {}).get("list", [])
    klines: list[list[Any]] = []
    for row in reversed(rows):
        klines.append(
            [
                int(row[0]),
                float(row[1]),
                float(row[2]),
                float(row[3]),
                float(row[4]),
                float(row[5]),
                0,
                float(row[6]),
            ]
        )
    return klines


def get_coingecko_weekly_klines(coin_id: str, limit: int, timeout: int) -> list[list[Any]]:
    days = 365
    data = request_json(
        f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart",
        params={"vs_currency": "usd", "days": days, "interval": "daily"},
        timeout=timeout,
    )

    prices = data.get("prices", [])
    volumes = data.get("total_volumes", [])
    if not prices:
        return []

    klines: list[list[Any]] = []
    for start in range(0, len(prices), 7):
        price_chunk = prices[start : start + 7]
        volume_chunk = volumes[start : start + 7]
        if len(price_chunk) < 2:
            continue
        open_price = float(price_chunk[0][1])
        closes = [float(point[1]) for point in price_chunk]
        high_price = max(closes)
        low_price = min(closes)
        close_price = closes[-1]
        quote_volume = sum(float(point[1]) for point in volume_chunk) if volume_chunk else 0.0
        klines.append(
            [
                int(price_chunk[0][0]),
                open_price,
                high_price,
                low_price,
                close_price,
                0,
                0,
                quote_volume,
            ]
        )

    return klines[-min(limit, len(klines)) :]


def calculate_rsi(prices: list[float], period: int = 14) -> float | None:
    if len(prices) <= period:
        return None

    gains: list[float] = []
    losses: list[float] = []
    for index in range(1, period + 1):
        delta = prices[index] - prices[index - 1]
        gains.append(max(delta, 0.0))
        losses.append(abs(min(delta, 0.0)))

    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period

    for index in range(period + 1, len(prices)):
        delta = prices[index] - prices[index - 1]
        gain = max(delta, 0.0)
        loss = abs(min(delta, 0.0))
        avg_gain = ((avg_gain * (period - 1)) + gain) / period
        avg_loss = ((avg_loss * (period - 1)) + loss) / period

    if avg_loss == 0:
        return 100.0 if avg_gain > 0 else 0.0

    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))


def calculate_ema(values: list[float], period: int) -> list[float]:
    if len(values) < period:
        return []
    multiplier = 2 / (period + 1)
    ema_values = [statistics.mean(values[:period])]
    for value in values[period:]:
        ema_values.append((value - ema_values[-1]) * multiplier + ema_values[-1])
    return ema_values


def calculate_macd(prices: list[float], fast: int = 12, slow: int = 26, signal: int = 9) -> tuple[float | None, float | None, float | None]:
    if len(prices) < slow + signal:
        return None, None, None

    fast_ema = calculate_ema(prices, fast)
    slow_ema = calculate_ema(prices, slow)
    offset = slow - fast
    aligned_fast = fast_ema[offset:]
    macd_series = [fast_value - slow_value for fast_value, slow_value in zip(aligned_fast, slow_ema)]
    signal_series = calculate_ema(macd_series, signal)
    if not signal_series:
        return None, None, None
    macd_line = macd_series[-1]
    signal_line = signal_series[-1]
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def calculate_bollinger_bands(prices: list[float], period: int = 20, std_dev: int = 2) -> tuple[float | None, float | None, float | None]:
    if len(prices) < period:
        return None, None, None
    recent = prices[-period:]
    middle = statistics.mean(recent)
    deviation = statistics.stdev(recent)
    upper = middle + (deviation * std_dev)
    lower = middle - (deviation * std_dev)
    return upper, middle, lower


def get_volume_ratio(klines: list[list[Any]], lookback: int = 30) -> float | None:
    if len(klines) < lookback:
        return None
    volumes = [float(candle[7]) for candle in klines]
    average_volume = statistics.mean(volumes[-lookback:])
    if average_volume == 0:
        return None
    return volumes[-1] / average_volume


def get_price_change_pct(klines: list[list[Any]]) -> float | None:
    if len(klines) < 2:
        return None
    current = float(klines[-1][4])
    previous = float(klines[-2][4])
    if previous == 0:
        return None
    return ((current - previous) / previous) * 100


def get_support_resistance(prices: list[float], window: int = 20) -> tuple[float | None, float | None]:
    if len(prices) < window:
        return None, None
    recent = prices[-window:]
    return min(recent), max(recent)


def get_fear_greed_index(timeout: int) -> int | None:
    try:
        data = request_json("https://api.alternative.me/fng/", timeout=timeout)
    except requests.RequestException:
        return None
    entries = data.get("data") or []
    if not entries:
        return None
    try:
        return int(entries[0]["value"])
    except (KeyError, TypeError, ValueError):
        return None


def get_coingecko_market_data(coin_id: str, timeout: int) -> dict[str, float | None]:
    try:
        data = request_json(f"https://api.coingecko.com/api/v3/coins/{coin_id}", timeout=timeout)
    except requests.RequestException:
        return {}

    market_data = data.get("market_data", {})
    return {
        "market_cap_usd": market_data.get("market_cap", {}).get("usd"),
        "volume_24h": market_data.get("total_volume", {}).get("usd"),
        "circulating_supply": market_data.get("circulating_supply"),
        "ath": market_data.get("ath", {}).get("usd"),
        "atl": market_data.get("atl", {}).get("usd"),
    }


def calculate_mvrv_proxy(coin_id: str, timeout: int) -> float | None:
    try:
        current_data = request_json(f"https://api.coingecko.com/api/v3/coins/{coin_id}", timeout=timeout)
        history_data = request_json(
            f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart",
            params={"vs_currency": "usd", "days": "365", "interval": "daily"},
            timeout=timeout,
        )
    except requests.RequestException:
        return None

    market_data = current_data.get("market_data", {})
    market_cap = market_data.get("market_cap", {}).get("usd")
    circulating_supply = market_data.get("circulating_supply")
    historical_prices = [point[1] for point in history_data.get("prices", [])]

    if not market_cap or not circulating_supply or not historical_prices:
        return None

    realized_cap_proxy = statistics.mean(historical_prices) * circulating_supply
    if realized_cap_proxy <= 0:
        return None

    return market_cap / realized_cap_proxy


def analyze_coin(coin: dict[str, str], config: dict[str, Any], fear_greed: int | None) -> CoinReport:
    timeout = int(config["runtime"]["request_timeout_seconds"])
    interval = config["binance"]["interval"]
    limit = int(config["binance"]["limit"])
    thresholds = config["thresholds"]

    try:
        klines = get_binance_klines(coin["symbol"], interval, limit, timeout)
    except requests.RequestException:
        try:
            klines = get_bybit_klines(coin["symbol"], limit, timeout)
        except requests.RequestException:
            klines = get_coingecko_weekly_klines(coin["coingecko_id"], limit, timeout)
    if not klines:
        raise MonitorError(f"no market data returned for {coin['symbol']}")

    prices = [float(candle[4]) for candle in klines]
    current_price = prices[-1]

    rsi = calculate_rsi(prices)
    macd_line, macd_signal, macd_histogram = calculate_macd(prices)
    upper_bb, middle_bb, lower_bb = calculate_bollinger_bands(prices)
    volume_ratio = get_volume_ratio(klines)
    price_change_pct = get_price_change_pct(klines)
    support, resistance = get_support_resistance(prices)

    market_data = get_coingecko_market_data(coin["coingecko_id"], timeout)
    mvrv_proxy = calculate_mvrv_proxy(coin["coingecko_id"], timeout)

    signals: list[str] = []
    if rsi is not None and rsi <= thresholds["rsi_max"]:
        signals.append(f"RSI oversold ({rsi:.1f})")
    if volume_ratio is not None and volume_ratio <= thresholds["volume_ratio_max"]:
        signals.append(f"Volume washout ({volume_ratio:.2f}x)")
    if macd_histogram is not None and macd_histogram < 0:
        signals.append(f"MACD histogram negative ({macd_histogram:.2f})")
    if lower_bb is not None and current_price <= lower_bb * thresholds["lower_band_buffer"]:
        signals.append("Price near lower Bollinger band")
    if fear_greed is not None and fear_greed <= thresholds["fear_greed_max"]:
        signals.append(f"Extreme fear ({fear_greed})")
    if mvrv_proxy is not None and mvrv_proxy <= thresholds["mvrv_proxy_max"]:
        signals.append(f"MVRV proxy low ({mvrv_proxy:.2f})")

    return CoinReport(
        symbol=coin["symbol"],
        name=coin["name"],
        price=current_price,
        price_change_pct=price_change_pct,
        rsi=rsi,
        macd=macd_line,
        macd_signal=macd_signal,
        macd_histogram=macd_histogram,
        bollinger_upper=upper_bb,
        bollinger_middle=middle_bb,
        bollinger_lower=lower_bb,
        volume_ratio=volume_ratio,
        support=support,
        resistance=resistance,
        fear_greed=fear_greed,
        market_cap=market_data.get("market_cap_usd"),
        volume_24h=market_data.get("volume_24h"),
        ath=market_data.get("ath"),
        atl=market_data.get("atl"),
        mvrv_proxy=mvrv_proxy,
        signals=signals,
    )


def fmt_price(value: float | None) -> str:
    return "n/a" if value is None else f"${value:,.2f}"


def fmt_billions(value: float | None) -> str:
    return "n/a" if value is None else f"${value / 1_000_000_000:.2f}B"


def fmt_number(value: float | None, digits: int = 2) -> str:
    return "n/a" if value is None else f"{value:.{digits}f}"


def recommendation(signal_count: int) -> str:
    if signal_count >= 5:
        return "strong accumulation setup"
    if signal_count >= 3:
        return "watch closely / scale in carefully"
    return "weak setup"


def build_coin_section(report: CoinReport) -> list[str]:
    lines = [
        f"{report.name} ({report.symbol})",
        f"  Price: {fmt_price(report.price)}",
        f"  Weekly change: {fmt_number(report.price_change_pct)}%",
        f"  RSI(14): {fmt_number(report.rsi)}",
        f"  MACD / signal / hist: {fmt_number(report.macd, 4)} / {fmt_number(report.macd_signal, 4)} / {fmt_number(report.macd_histogram, 4)}",
        f"  Bollinger lower / mid / upper: {fmt_price(report.bollinger_lower)} / {fmt_price(report.bollinger_middle)} / {fmt_price(report.bollinger_upper)}",
        f"  Volume ratio: {fmt_number(report.volume_ratio)}x",
        f"  Support / resistance: {fmt_price(report.support)} / {fmt_price(report.resistance)}",
        f"  Fear & Greed: {report.fear_greed if report.fear_greed is not None else 'n/a'}",
        f"  Market cap / 24h volume: {fmt_billions(report.market_cap)} / {fmt_billions(report.volume_24h)}",
        f"  ATH / ATL: {fmt_price(report.ath)} / {fmt_price(report.atl)}",
        f"  MVRV proxy: {fmt_number(report.mvrv_proxy)}",
        f"  Signal count: {len(report.signals)}/6",
        f"  Recommendation: {recommendation(len(report.signals))}",
    ]

    if report.signals:
        lines.append("  Signals:")
        for signal in report.signals:
            lines.append(f"    - {signal}")
    else:
        lines.append("  Signals: none triggered")

    return lines


def build_report(reports: list[CoinReport]) -> str:
    timestamp = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    lines = [
        "BTC Monitor Report",
        f"Generated: {timestamp}",
        "",
    ]

    for report in reports:
        lines.extend(build_coin_section(report))
        lines.append("")

    lines.append("Notes:")
    lines.append("- This tool uses public market APIs only.")
    lines.append("- MVRV proxy is an approximation derived from CoinGecko history, not a true on-chain realized cap metric.")
    lines.append("- Outputs are informational and not trading advice.")
    return "\n".join(lines).strip() + "\n"


def split_message(content: str, limit: int = 1900) -> list[str]:
    chunks: list[str] = []
    current: list[str] = []
    current_length = 0

    for line in content.splitlines():
        projected = current_length + len(line) + 1
        if current and projected > limit:
            chunks.append("\n".join(current))
            current = [line]
            current_length = len(line) + 1
        else:
            current.append(line)
            current_length = projected

    if current:
        chunks.append("\n".join(current))
    return chunks


def send_to_discord(report_text: str, config: dict[str, Any]) -> None:
    discord = config["discord"]
    if not discord.get("enabled"):
        return

    token = os.getenv(discord["token_env"], "").strip()
    channel_id = str(discord.get("channel_id", "")).strip()
    mention_user_id = str(discord.get("mention_user_id", "")).strip()
    timeout = int(config["runtime"]["request_timeout_seconds"])

    if not token:
        raise MonitorError(f"discord enabled but env var {discord['token_env']} is not set")
    if not channel_id:
        raise MonitorError("discord enabled but channel_id is empty")

    prefix = f"<@{mention_user_id}>\n" if mention_user_id else ""
    chunks = split_message(prefix + report_text)
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json",
    }

    for chunk in chunks:
        post_json(
            f"{DISCORD_API_BASE}/channels/{channel_id}/messages",
            headers=headers,
            payload={"content": chunk},
            timeout=timeout,
        )


def main() -> int:
    try:
        config = load_config()
        timeout = int(config["runtime"]["request_timeout_seconds"])
        fear_greed = get_fear_greed_index(timeout)
        reports = [analyze_coin(coin, config, fear_greed) for coin in config["coins"]]
        report_text = build_report(reports)
        sys.stdout.write(report_text)
        send_to_discord(report_text, config)
        return 0
    except (MonitorError, requests.RequestException) as exc:
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 1
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
