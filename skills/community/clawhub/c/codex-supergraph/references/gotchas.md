# Codex Supergraph Gotchas

Common failure points. Check here first when a query returns unexpected results.

## Validate against the schema on 400 errors

If a query returns a 400 or GraphQL validation error, fetch the latest schema and check your query against it:

```
https://graph.codex.io/schema/latest.graphql
```

Field names, input shapes, and argument structures change over time. Don't guess — validate.

## Input objects vs flat args

Many queries wrap their arguments in an `input` or `query` object rather than accepting flat args. Common examples:

- `getTokenEvents` takes `query: EventsQueryInput!` (not flat `address`/`networkId`)
- `getTokenEventsForMaker` takes `query: MakerEventsQueryInput!` (not flat `maker`/`address`)
- `filterTokenWallets` takes `input: FilterTokenWalletsInput!`
- `walletChart` takes `input: WalletChartInput!` (with `range: { start, end }`, not `from`/`to`)
- `holders` takes `input: HoldersInput!`

If you get a validation error about missing required args, check whether the schema expects an input wrapper.

## Composite ID formats

Several operations use `address:networkId` composite IDs:

- `getBars` / `getTokenBars`: `symbol` is `pairAddress:networkId`
- `pairMetadata`: `pairId` is `pairAddress:networkId`
- `top10HoldersPercent`: `tokenId` is `tokenAddress:networkId`
- `filterTokenWallets`: `tokenIds` array uses `tokenAddress:networkId`

## `trendingScore24` is a sort attribute, not a field

You can rank by `trendingScore24` in `filterTokens` rankings, but it is not a selectable field on the result type. Don't include it in the selection set.

Cross-domain trap: tokens rank by `trendingScore24` (no "h"); prediction markets rank by `trendingScore24h` (with "h", and it *is* selectable there). Swapping them returns empty results rather than erroring, so verify which domain you're in.

## `filterTokens` pagination

Max 200 results per call. Use `offset` as an input arg to paginate. The response returns `page` (not `offset`) and `count`.

## `filterTokens` trending queries need `statsType`

When ranking by `trendingScore24`, set `statsType: "FILTERED"` or you'll get zero/null scores. Also use `trendingIgnored: false` and `potentialScam: false` in filters to exclude noise.

## `Event` type has no `priceUsd` field

The `Event` type does not have a `priceUsd` field. Use `token0SwapValueUsd` and `token1SwapValueUsd` for USD values, or `token0ValueBase` and `token1ValueBase` for base token values.

## `holders` response uses `items`, not `holders`

The `HoldersResponse` type returns the holder list in `items`, not a `holders` field. Each `Balance` object has `address`, `balance`, `shiftedBalance`, `balanceUsd` — there is no `sharedPct` field.

## `listPairsWithMetadataForToken` field names

The result type uses `volume` (not `volume24`) and does not have a `price` field.

## `getBars` missing timestamps

Always include `t` in the selection set. Without it the bars are unplottable. The fields are `t o h l c volume`.

## `getBars` max datapoints

Max 1500 datapoints per request. Narrow the time window or increase the resolution if you hit the limit.

## `networkId` validation

Always validate `networkId` against `getNetworks` before using it. A wrong ID returns empty results, not an error. Common IDs: Ethereum=`1`, Solana=`1399811149`, Base=`8453`.

## Subscription fan-out

Use `onPricesUpdated` (batch) instead of opening many `onPriceUpdated` (single) subscriptions. Batch input supports ~25 tokens per subscription.

## Rate limits return 429, not GraphQL errors

Rate limit responses are HTTP 429, not wrapped in GraphQL `errors`. Check the HTTP status, not just the response body.

## Short-lived tokens can't manage themselves

`apiTokens`, `apiToken`, and `deleteApiToken` are not available when authenticated with a short-lived token. Use the long-lived API key for token management.

## Prediction market `bestAskCT` is the implied probability

For stablecoin-collateral markets, `bestAskCT` of 0.65 means 65% implied probability. Prefer CT (Collateral Token) values over USD values.

## Prediction trader ID format

Trader IDs use the format `address:Protocol` (e.g., `0x1234...:Polymarket`). Missing the protocol suffix will return no results.

## Prediction OHLC values are strings

All OHLC fields (`o`, `h`, `l`, `c`) in prediction market bars are strings, not numbers. Parse them to floats before rendering. Timestamps are unix seconds — multiply by 1000 for JavaScript milliseconds.

## `predictionEventBars` has no per-outcome prices

`predictionEventBars` only returns aggregated volume, liquidity, and open interest. For per-outcome price data, use `predictionMarketBars` or `predictionEventTopMarketsBars`.

## `filterPredictionEvents` vs `filterPredictionMarkets`

Events are containers grouping related markets. Use `filterPredictionEvents` for discovery, then `filterPredictionMarkets(eventIds)` for market-level pricing within an event.

## `competitiveScore24h` is markets-only

`competitiveScore24h` is available on `filterPredictionMarkets` but not on `filterPredictionEvents`. It measures how close the outcome prices are.
