# Methodology

## Core Metrics

- Directional return: `(last_close / first_close - 1)`.
- Path return: sum of absolute close-to-close returns.
- Trend efficiency: `abs(last_close - first_close) / sum(abs(close_delta))`. Values near `1` mean price moved in one dominant direction.
- ATR-normalized move: absolute net move divided by latest ATR. A larger value means the trend travelled meaningfully beyond normal candle noise.
- ADX: standard directional movement strength estimate. Values above `25` support trend conditions; above `35` support stronger trend conditions.
- Max countertrend pullback: worst retracement from the running high in bullish moves or running low in bearish moves.
- MA slope agreement: EMA20 and EMA50 slope/direction should agree with the net direction.

## Default Thresholds

Classify `bullish_one_way` or `bearish_one_way` when most of these are true:

- Absolute directional return is at least `1.5%` for intraday timeframes or meaningful for the selected lookback.
- Trend efficiency is at least `0.45`; stronger evidence above `0.60`.
- ADX is at least `25`; stronger evidence above `35`.
- ATR-normalized move is at least `3.0`.
- Countertrend pullback is controlled: default max `35%` of the net move.
- EMA20 and EMA50 slope agree with the direction, or price stays mostly on one side of EMA20.

Classify `weak_trend` when direction is clear but one-way conditions are incomplete.

Classify `range_or_chop` when trend efficiency is low, ADX is weak, or price repeatedly mean-reverts.

## Reporting Guidance

Prefer "当前 K 线结构更像..." rather than "一定会...". Mention that the result describes the sampled interval only. A 15m one-way move can still be a pullback on 4h or daily charts.

For borderline results, state which metric failed and what would strengthen the conclusion, such as higher efficiency, break of range high/low, or controlled pullbacks.
