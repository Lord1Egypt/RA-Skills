# BTC Monitor Skill Docs

## Runtime Flow

1. Load `config.json`
2. Fetch Binance candle data for each configured coin, or fall back to CoinGecko-derived weekly candles
3. Fetch CoinGecko market data and history
4. Fetch the Fear & Greed Index once per run
5. Calculate indicators and signal count
6. Print a plain-text report
7. Optionally send the report to Discord

## Config Reference

```json
{
  "coins": [
    {"symbol": "BTCUSDT", "name": "Bitcoin", "coingecko_id": "bitcoin"},
    {"symbol": "ETHUSDT", "name": "Ethereum", "coingecko_id": "ethereum"}
  ],
  "binance": {
    "interval": "1w",
    "limit": 100
  },
  "thresholds": {
    "rsi_max": 30.0,
    "volume_ratio_max": 0.7,
    "fear_greed_max": 25,
    "mvrv_proxy_max": 1.0,
    "lower_band_buffer": 1.05
  },
  "discord": {
    "enabled": false,
    "token_env": "DISCORD_TOKEN",
    "channel_id": "",
    "mention_user_id": ""
  },
  "schedule": "0 8 * * *"
}
```

## Output Semantics

- `Signal count` is the number of triggered rules out of 6.
- `MVRV proxy` is an approximation and should be treated as a heuristic only.
- `Recommendation` is a coarse label driven only by the signal count.

## Extending

To add a new asset:

1. Add a new entry to `coins` in `config.json`
2. Ensure the Binance symbol and CoinGecko ID both exist
3. Run `python3 scripts/monitor.py`
