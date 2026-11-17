# forecast-os-lite

Read-only edition of [ForecastOS](https://github.com/precog-markets/forecast-os), an agent skill for checking live prediction markets before answering questions about future events.

## What it does

- Looks up open markets on **Polymarket**, **Kalshi**, and **Precog**
- Reports market-implied probabilities of an event with the source and a freshness timestamp
- Discovers upcoming markets

## What it does not do

This edition is strictly read-only (HTTP GET against public endpoints). It does not provide executable quotes or handle trades, claims, positions, market creation, funding, wallets, keys, configuration, or updates. Those requests are redirected to the full `forecast-os` skill.

## Install

```bash
npx skills add precog-markets/forecast-os-lite
```

## Example prompts

- "What are the odds the Fed cuts rates in December?"
- "Compare Polymarket and Kalshi on the next US election."
- "Any upcoming Precog markets about ETH?"

## Disclaimer

Market data only. This is not financial advice.
