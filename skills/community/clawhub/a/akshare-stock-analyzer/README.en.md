# Akshare-Stock-Analyzer

> For the Chinese documentation, see [README.md](README.md).

Akshare-Stock-Analyzer is a lightweight A-share analysis helper built on top of Akshare. It focuses on:
- **Today's intraday snapshot** for a single stock (price, % change, volume, intraday high/low);
- **Recent daily trend** (from about 1 week to a few months), with signals and a simple score.

Think of it as a short-term technical health check rather than a full trading system.

---

## How to talk to it

You don’t need to remember any CLI commands. Just ask in natural language, for example:

- "What’s today’s intraday move of Ping An Bank?"
- "Check the last week and today’s action for China Pacific Insurance."
- "Over the past three months, is this stock in a bullish or bearish trend?"
- "Is it better to hold or reduce position on this name now?"

Behind the scenes, the tool will call its own `today` / `fetch` / `analyze` scripts to:
- Fetch today’s snapshot: price, % change, volume, intraday high/low;
- Analyze recent daily trend, weekly change and today change;
- Produce a trading signal (buy / sell / hold) and a 0–10 score;
- Expose extra context like moving averages, MACD and RSI.

---

## How the trend analysis works (brief)

Internally, the analysis logic combines:

- Daily candles: recent closes, highs/lows and volume;
- Moving averages: MA7 / MA14 / MA20 / MA60 structure and where price sits relative to them;
- MACD: golden/death crosses, position vs. zero line, and whether momentum is increasing or decreasing;
- RSI: strength zone, proximity to overbought/oversold and whether it’s trending up or down;
- Trend strength and risk-related signals:
  - `trend_strength` to quantify bullish/bearish strength;
  - `reversal_hint` to flag early top/bottom warnings;
  - `risk_level` to highlight overbought/oversold or overextended trends.

From this, the model derives:
- `trend`: bullish, bearish or sideways;
- `weekly_change_pct` / `today_change_pct`: one-week and today’s % change;
- `signal`: a coarse buy / sell / hold view;
- `score`: a 0–10 short-term technical score.

You can read the output as a compact synthesis of **trend + momentum + sentiment**, to be used as technical input only.

---

## Notes

- All conclusions are based purely on technical indicators and price action and **do not constitute investment advice**.
- Real trading decisions should also consider fundamentals, news, position sizing and your own risk tolerance.
- Intraday data depends on upstream real-time APIs and your network; short outages or delays can occasionally occur.

### 3. Which script to use when

- **Just intraday view** → use `scripts/today.py` only.
- **Trend / strategy view** → use `scripts/analyze.py` (it calls fetch internally; you don't need to run today.py manually).

## Notes

- All conclusions are based purely on technicals and price action and **do not constitute investment advice**.
- Intraday data depends on upstream real-time APIs and your network; if real-time fails, analysis will fall back to the most recent completed trading day.
