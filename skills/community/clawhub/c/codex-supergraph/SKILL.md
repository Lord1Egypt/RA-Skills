---
name: codex-supergraph
description: >-
  Use when the user asks about token prices, charts, holders, trending tokens,
  pair data, prediction markets, or any on-chain analytics from Codex.
  Also use when building GraphQL queries against https://graph.codex.io/graphql.

  TRIGGERS: token price, token chart, trending tokens, pair data, holders,
  prediction markets, Polymarket, Kalshi, event odds, prediction event,
  prediction traders, trader leaderboard, trader PnL, prediction charts,
  outcome probability, open interest, prediction categories, betting markets,
  market resolution, prediction positions, prediction trades
metadata:
  author: codex-data
  version: "1.0"
---

# Codex Supergraph Data

[Codex](https://www.codex.io) provides real-time on-chain data — token prices, charts, holders, and prediction markets — via a single GraphQL API. Full documentation: [docs.codex.io](https://docs.codex.io).

## Authentication

Pass `$CODEX_API_KEY` in the `Authorization` header if available. Get a free API key at [dashboard.codex.io/signup](https://dashboard.codex.io/signup). If the server returns `402 Payment Required`, use the codex-gateway skill to handle the payment flow.

If both a local and global copy of this skill exist, the local copy takes precedence.

## Summary

Use this skill to produce valid Codex GraphQL requests using API key authentication.

|                       |                                                                 |
| --------------------- | --------------------------------------------------------------- |
| HTTP endpoint         | `https://graph.codex.io/graphql`                                |
| WebSocket endpoint    | `wss://graph.codex.io/graphql`                                  |
| Schema (SDL)          | `https://graph.codex.io/schema/latest.graphql`                  |
| Introspection JSON    | `https://graph.codex.io/schema/latest.json`                     |
| API-key auth          | `Authorization: <key>` or `Authorization: Bearer <token>`       |

## Session preflight (required)

Run once and cache:

```bash
curl -sS https://graph.codex.io/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $CODEX_API_KEY" \
  --data-binary '{"query":"query GetNetworks { getNetworks { id name } }"}'
```

Use network IDs from this result before expensive requests.

## Operation selection

| Need | Operation |
| ---- | --------- |
| Networks | `getNetworks` |
| Token discovery/search | `filterTokens` |
| Trending tokens | `filterTokens` with `trendingScore24` ranking |
| Token prices | `getTokenPrices` |
| Pairs for a token | `listPairsWithMetadataForToken` |
| Pair metadata | `pairMetadata` |
| Pair OHLCV | `getBars` |
| Token OHLCV | `getTokenBars` |
| Token events | `getTokenEvents` |
| Maker events | `getTokenEventsForMaker` |
| Wallet leaders | `filterTokenWallets` |
| Wallet chart/stats | `walletChart`, `detailedWalletStats` |
| Holders | `holders` |
| Top-10 concentration | `top10HoldersPercent` |
| Live single price | `onPriceUpdated` |
| Live multi-price | `onPricesUpdated` |
| Live token events | `onTokenEventsCreated`, `onEventsCreatedByMaker` |
| Live bars/pairs | `onBarsUpdated`, `onPairMetadataUpdated`, `onTokenBarsUpdated` |
| Launchpad streams | `onLaunchpadTokenEventBatch`, `onLaunchpadTokenEvent` |
| Unconfirmed Solana events | `onUnconfirmedEventsCreated` |
| Short-lived keys | `createApiTokens`, `apiTokens`, `apiToken`, `deleteApiToken` |
| Webhooks (server-side alerts) | `createWebhooks`, `deleteWebhooks`, `getWebhooks` |
| Windowed token change stats | `getDetailedTokenStats` |
| Prediction event discovery | `filterPredictionEvents` |
| Prediction market discovery | `filterPredictionMarkets` |
| Prediction event detail | `detailedPredictionEventStats` |
| Prediction market chart | `predictionMarketBars` |
| Prediction multi-market chart | `predictionEventTopMarketsBars` |
| Prediction event chart | `predictionEventBars` |
| Prediction trades | `predictionTrades` |
| Prediction token holders | `predictionTokenHolders` |
| Prediction categories | `predictionCategories` |
| Prediction trader leaderboard | `filterPredictionTraders` |
| Prediction trader profile | `detailedPredictionTraderStats` |
| Prediction trader positions | `filterPredictionTraderMarkets` |
| Prediction trader chart | `predictionTraderBars` |

Default discovery path: start with `filterTokens`.

## Rules

- Never print raw API keys.
- Validate `networkId` first.
- Keep selection sets minimal until shape is confirmed.
- Use `onPricesUpdated` instead of many single-token subscriptions.

## References

| File | Purpose |
| ---- | ------- |
| [references/gotchas.md](references/gotchas.md) | Common failure points — check here first |
| [references/query-templates.md](references/query-templates.md) | Query + websocket templates with examples |
| [references/endpoint-playbook.md](references/endpoint-playbook.md) | Operation selection heuristics by intent |
| [references/apis.md](references/apis.md) | Endpoint/auth matrix, pagination, rate limits |
| [references/prediction-markets.md](references/prediction-markets.md) | Prediction market queries — events, markets, traders, charts |
| [references/tooling-and-mcp.md](references/tooling-and-mcp.md) | Codex Docs MCP setup for coding tools |

## Links

- Website: [www.codex.io](https://www.codex.io)
- Documentation: [docs.codex.io](https://docs.codex.io)
- Get an API key: [dashboard.codex.io/signup](https://dashboard.codex.io/signup)
