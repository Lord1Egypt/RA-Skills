import csv
import json
import os
import re
from dataclasses import dataclass
from statistics import mean
from typing import List


@dataclass
class Bar:
    trade_date: str
    close: float


DEFAULT_CONFIG = {
    "symbol": "518880.SH",
    "base_amount": 1000,
    "min_multiplier": 0.6,
    "max_multiplier": 1.8,
    "rules": {
        "oversold_rsi": 35,
        "weak_rsi_max": 45,
        "neutral_rsi_max": 60,
        "hot_rsi": 68,
        "discount_to_ma20": -0.03,
        "premium_to_ma20": 0.05,
        "ma20_near_band": 0.01,
        "drawdown_weak": 0.04,
        "deep_drawdown": 0.08
    }
}


def project_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def ensure_within_project(path: str) -> str:
    resolved = os.path.abspath(path)
    root = project_root()
    if os.path.commonpath([resolved, root]) != root:
        raise RuntimeError(f"Path escapes project root: {resolved}")
    return resolved


def sanitize_symbol(symbol: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", symbol):
        raise RuntimeError("OPENCLAW_SYMBOL contains invalid characters.")
    return symbol


def merge_dict(base: dict, extra: dict) -> None:
    for key, value in extra.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            merge_dict(base[key], value)
        else:
            base[key] = value


def load_history(path: str) -> List[Bar]:
    bars = []
    with open(path, "r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            bars.append(Bar(trade_date=row["trade_date"], close=float(row["close"])))
    if len(bars) < 60:
        raise RuntimeError("Not enough historical data for backtest.")
    return bars


def sma(values: List[float], window: int) -> float:
    return mean(values[-window:])


def stddev(values: List[float], window: int) -> float:
    window_values = values[-window:]
    avg = mean(window_values)
    variance = sum((value - avg) ** 2 for value in window_values) / len(window_values)
    return variance ** 0.5


def compute_rsi(values: List[float], period: int = 14) -> float:
    deltas = [values[i] - values[i - 1] for i in range(1, len(values))]
    gains = [max(delta, 0.0) for delta in deltas[-period:]]
    losses = [abs(min(delta, 0.0)) for delta in deltas[-period:]]
    avg_gain = mean(gains) if gains else 0.0
    avg_loss = mean(losses) if losses else 0.0
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))


def ema(values: List[float], period: int) -> List[float]:
    multiplier = 2 / (period + 1)
    series = [values[0]]
    for value in values[1:]:
        series.append((value - series[-1]) * multiplier + series[-1])
    return series


def compute_macd(values: List[float]) -> List[float]:
    ema12 = ema(values, 12)
    ema26 = ema(values, 26)
    dif = [a - b for a, b in zip(ema12, ema26)]
    dea = ema(dif, 9)
    return [d - e for d, e in zip(dif, dea)]


def classify_multiplier(closes: List[float], config: dict) -> float:
    rules = config["rules"]
    last_close = closes[-1]
    ma20 = sma(closes, 20)
    ma60 = sma(closes, 60)
    rsi14 = compute_rsi(closes, 14)
    recent_high = max(closes[-60:])
    drawdown = (recent_high - last_close) / recent_high if recent_high else 0.0
    vs_ma20 = (last_close - ma20) / ma20 if ma20 else 0.0
    vs_ma60 = (last_close - ma60) / ma60 if ma60 else 0.0

    if sum(
        [
            vs_ma20 <= rules["discount_to_ma20"],
            rsi14 <= rules["oversold_rsi"],
            drawdown >= rules["deep_drawdown"],
            vs_ma60 < 0,
        ]
    ) >= 2:
        base = 1.6
    elif sum(
        [
            vs_ma20 >= rules["premium_to_ma20"],
            rsi14 >= rules["hot_rsi"],
            vs_ma60 > 0,
            drawdown < rules["drawdown_weak"],
        ]
    ) >= 2:
        base = 0.7
    elif sum(
        [
            vs_ma20 < 0,
            rules["oversold_rsi"] <= rsi14 <= rules["weak_rsi_max"],
            rules["drawdown_weak"] <= drawdown < rules["deep_drawdown"],
        ]
    ) >= 2:
        base = 1.2
    else:
        base = 1.0

    boll_std = stddev(closes, 20)
    upper = ma20 + 2 * boll_std
    lower = ma20 - 2 * boll_std
    width = upper - lower
    pos = (last_close - lower) / width if width > 0 else 0.5
    if pos <= 0:
        base += 0.2
    elif pos <= 0.25:
        base += 0.1
    elif pos < 0.75:
        base += 0.0
    elif pos < 1:
        base -= 0.1
    else:
        base -= 0.2

    hist = compute_macd(closes)
    if len(hist) >= 3:
        h2, h1, h0 = hist[-3], hist[-2], hist[-1]
        bearish_easing = h0 < 0 and abs(h0) < abs(h1) < abs(h2)
        bullish_easing = h0 > 0 and abs(h0) < abs(h1) < abs(h2)
        if base >= 1.6 and bearish_easing:
            base += 0.1
        if base <= 0.7 and bullish_easing:
            base -= 0.1

    return round(max(config["min_multiplier"], min(config["max_multiplier"], base)), 2)


def run_backtest(bars: List[Bar], config: dict) -> dict:
    base_amount = float(config["base_amount"])
    total_invested = 0.0
    dynamic_units = 0.0
    fixed_units = 0.0
    records = 0

    for index in range(60, len(bars)):
        if index % 5 != 0:
            continue
        closes = [bar.close for bar in bars[: index + 1]]
        price = closes[-1]
        multiplier = classify_multiplier(closes, config)
        dynamic_amount = base_amount * multiplier
        fixed_amount = base_amount
        dynamic_units += dynamic_amount / price
        fixed_units += fixed_amount / price
        total_invested += dynamic_amount
        records += 1

    final_price = bars[-1].close
    dynamic_value = dynamic_units * final_price
    fixed_invested = records * base_amount
    fixed_value = fixed_units * final_price

    return {
        "symbol": config["symbol"],
        "period_start": bars[0].trade_date,
        "period_end": bars[-1].trade_date,
        "records": records,
        "dynamic_total_invested": round(total_invested, 2),
        "dynamic_final_value": round(dynamic_value, 2),
        "dynamic_return": round((dynamic_value - total_invested) / total_invested, 4) if total_invested else 0,
        "fixed_total_invested": round(fixed_invested, 2),
        "fixed_final_value": round(fixed_value, 2),
        "fixed_return": round((fixed_value - fixed_invested) / fixed_invested, 4) if fixed_invested else 0,
    }


def main() -> None:
    symbol = sanitize_symbol(os.getenv("OPENCLAW_SYMBOL", DEFAULT_CONFIG["symbol"]))
    history_path = os.getenv(
        "OPENCLAW_HISTORY_PATH",
        os.path.join(os.path.dirname(__file__), "..", "references", "history", f"{symbol.replace('.', '_')}.csv"),
    )
    history_path = ensure_within_project(history_path)
    config_path = os.getenv("OPENCLAW_CONFIG")
    config = json.loads(json.dumps(DEFAULT_CONFIG))
    if config_path and os.path.exists(config_path):
        safe_config_path = ensure_within_project(config_path)
        with open(safe_config_path, "r", encoding="utf-8") as fh:
            user_config = json.load(fh)
        merge_dict(config, user_config)
    bars = load_history(history_path)
    result = run_backtest(bars, config)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
