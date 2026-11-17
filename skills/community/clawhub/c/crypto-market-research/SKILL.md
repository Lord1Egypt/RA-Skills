---
name: crypto-market-research
description: Researches public cryptocurrency markets, coins, exchanges, categories, global metrics, news, NFTs, token unlocks, and treasuries through CoinGecko via the Crawlora API. Use for market snapshots and comparative research, not trading or financial advice.
---

# Crypto market research

Pull public CoinGecko market data as normalized JSON for coin discovery,
market comparisons, category and chain research, global metrics, news, NFT
surfaces, token unlocks, and treasury snapshots.

## When to use this skill

- Resolve a coin or token before comparing price, market cap, volume, or supply.
- Screen markets, categories, chains, exchanges, gainers/losers, or trending coins.
- Inspect global crypto metrics, public news, token unlocks, or treasuries.
- Compare an asset's public profile and market data across a defined timestamp.

## Research workflow

1. Search with `/coingecko/search` and use the returned CoinGecko ID. Tickers
   are ambiguous and must not be used as stable identity keys.
2. Fetch `/coingecko/coin/{id}` and `/coingecko/markets` with explicit currency,
   page, and ordering parameters. Preserve the quote currency and timestamp.
3. Use category, chain, exchange, and global routes for comparable cohorts.
   Keep spot markets, derivatives, NFTs, and treasury holdings as separate
   surfaces.
4. Treat gainers/losers, trending, news, and unlocks as time-sensitive signals,
   not forecasts. Report missing data and stale snapshots explicitly.

## Examples

```sh
scripts/crawlora.sh /coingecko/search query="bitcoin" | jq '.'
scripts/crawlora.sh /coingecko/coin/bitcoin vs_currency=usd | jq '.'
scripts/crawlora.sh /coingecko/markets vs_currency=usd order=market_cap_desc | jq '.'
scripts/crawlora.sh /coingecko/trending | jq '.'
scripts/crawlora.sh /coingecko/global | jq '.'
```

## Notes and limits

- Public market information only. This skill does not place orders, connect
  wallets, move funds, or access private exchange accounts.
- Prices, volumes, rankings, and news change quickly; include retrieval time,
  quote currency, source, and requested filters in reports.
- Market data is not investment advice. Do not convert a snapshot into a price
  target, guaranteed return, or claim of manipulation without evidence.
- CoinGecko IDs, symbols, chain IDs, and exchange IDs are distinct namespaces.

See [`reference/endpoints.md`](reference/endpoints.md) for the complete generated endpoint list.
