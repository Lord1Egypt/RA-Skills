# AgentKey Tool Reference

Use this reference after the skill triggers. AgentKey's crypto catalog changes over time; call `find_tools` or `list_tools(prefix="crypto")` when an endpoint is missing, then call `describe_tool` before `execute_tool`.

## Core Endpoints

- `CoinMarketCap/getFearAndGreedLatest`
  - Purpose: latest crypto Fear and Greed value.
  - Known cost: 0.6 credits.
  - Params: none.

- `CoinMarketCap/getFearAndGreedHistorical`
  - Purpose: historical sentiment context.
  - Known cost from discovery: 0.6 credits.
  - Run `describe_tool` before use.

- `CoinMarketCap/getCryptocurrencyQuotesHistoricalV2`
  - Purpose: BTC historical quotes: price, volume, market cap.
  - Known cost: 0.6 credits.
  - Useful params: `symbol=BTC`, `convert=USD`, `interval=daily`, `count`, `time_start`, `time_end`.
  - Plan note: sub-daily granularity is limited to recent data; use daily for longer cycle analysis.

## Optional Deep-Dive Endpoints

- `Surf/market-onchain-indicator`
  - Purpose: on-chain indicator context.
  - Discovered cost: 3.6 credits.

- `Surf/market-price-indicator`
  - Purpose: technical indicator context.
  - Discovered cost: 3.6 credits.

- `Surf/market-etf`
  - Purpose: ETF flow history.
  - Discovered cost: 3.6 credits.

Run `describe_tool` for all Surf endpoints before executing because parameter names and indicator coverage can change.

## Suggested Call Plans

Quick score: Fear and Greed latest plus BTC historical quotes.

Standard score: quick score plus historical Fear and Greed and one technical/on-chain endpoint. Ask for confirmation first.

Deep score: standard score plus ETF flow and additional on-chain indicators. Use when the user wants a full dashboard or report.
