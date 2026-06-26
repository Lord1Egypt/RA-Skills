# Codex Supergraph Query Templates

## 1) Simple query

```bash
curl -sS https://graph.codex.io/graphql \
  -H 'Content-Type: application/json' \
  -H "Authorization: $CODEX_API_KEY" \
  --data-binary @- <<'JSON'
{
  "query": "query GetNetworks { getNetworks { id name } }"
}
JSON
```

## 2) Query with variables

```bash
curl -sS https://graph.codex.io/graphql \
  -H 'Content-Type: application/json' \
  -H "Authorization: $CODEX_API_KEY" \
  --data-binary @- <<'JSON'
{
  "query": "query GetTokenPrices($inputs: [GetPriceInput!]!) { getTokenPrices(inputs: $inputs) { address networkId priceUsd timestamp } }",
  "variables": {
    "inputs": [
      { "address": "So11111111111111111111111111111111111111112", "networkId": 1399811149 }
    ]
  }
}
JSON
```

## 3) Token discovery (`filterTokens`)

```graphql
query FilterTokens(
  $filters: TokenFilters
  $statsType: TokenPairStatisticsType
  $rankings: [TokenRanking]
  $limit: Int
  $offset: Int
) {
  filterTokens(
    filters: $filters
    statsType: $statsType
    rankings: $rankings
    limit: $limit
    offset: $offset
  ) {
    count
    page
    results {
      priceUSD
      marketCap
      buyVolume24
      sellVolume24
      volume24
      circulatingMarketCap
      liquidity
      txnCount24
      holders
      token {
        info {
          address
          name
          symbol
          networkId
        }
      }
    }
  }
}
```

Example variables — top tokens on Solana by volume:

```json
{
  "filters": {
    "network": [1399811149],
    "liquidity": { "gte": 10000 }
  },
  "rankings": [{ "attribute": "volume24", "direction": "DESC" }],
  "limit": 25,
  "offset": 0
}
```

Example variables — trending tokens:

```json
{
  "filters": {
    "volume24": { "lte": 100000000000 },
    "liquidity": { "lte": 1000000000 },
    "marketCap": { "gte": 500000, "lte": 1000000000000 },
    "trendingIgnored": false,
    "creatorAddress": null,
    "potentialScam": false
  },
  "statsType": "FILTERED",
  "rankings": [{ "attribute": "trendingScore24", "direction": "DESC" }],
  "limit": 50,
  "offset": 0
}
```

Note: `trendingScore24` is a valid ranking attribute but is not a selectable field on the result type. Sort by it, but don't request it in the selection set.

## 4) Pair metadata (`pairMetadata`)

```graphql
query PairMetadata($pairId: String!) {
  pairMetadata(pairId: $pairId) {
    id
    pairAddress
    networkId
    liquidity
    price
    priceChange24
    volume24
    token0 {
      address
      symbol
      name
    }
    token1 {
      address
      symbol
      name
    }
  }
}
```

## 5) Pair bars (`getBars`)

```graphql
query GetBars(
  $symbol: String!
  $from: Int!
  $to: Int!
  $resolution: String!
  $countback: Int
  $removeEmptyBars: Boolean
) {
  getBars(
    symbol: $symbol
    from: $from
    to: $to
    resolution: $resolution
    countback: $countback
    removeEmptyBars: $removeEmptyBars
  ) {
    t
    o
    h
    l
    c
    volume
  }
}
```

## 6) Single-token realtime (`onPriceUpdated`)

```graphql
subscription OnPriceUpdated($address: String!, $networkId: Int!) {
  onPriceUpdated(address: $address, networkId: $networkId) {
    address
    networkId
    priceUsd
    timestamp
    blockNumber
  }
}
```

## 7) Multi-token realtime (`onPricesUpdated`)

```graphql
subscription OnPricesUpdated($input: [OnPricesUpdatedInput!]!) {
  onPricesUpdated(input: $input) {
    address
    networkId
    priceUsd
    timestamp
    blockNumber
  }
}
```

Example variables:

```json
{
  "input": [
    { "address": "So11111111111111111111111111111111111111112", "networkId": 1399811149 },
    { "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", "networkId": 1 }
  ]
}
```

## 8) Token bars (`getTokenBars`)

Aggregates OHLCV across top liquidity pairs for a token. Uses same `resolution` values as `getBars`.

```graphql
query GetTokenBars(
  $symbol: String!
  $from: Int!
  $to: Int!
  $resolution: String!
  $countback: Int
  $removeEmptyBars: Boolean
) {
  getTokenBars(
    symbol: $symbol
    from: $from
    to: $to
    resolution: $resolution
    countback: $countback
    removeEmptyBars: $removeEmptyBars
  ) {
    t
    o
    h
    l
    c
    volume
  }
}
```

## 9) List pairs for a token (`listPairsWithMetadataForToken`)

```graphql
query ListPairs($tokenAddress: String!, $networkId: Int!) {
  listPairsWithMetadataForToken(tokenAddress: $tokenAddress, networkId: $networkId) {
    results {
      pair {
        address
        networkId
        token0
        token1
      }
      volume
      liquidity
    }
  }
}
```

## 10) Token events (`getTokenEvents`)

```graphql
query GetTokenEvents(
  $query: EventsQueryInput!
  $cursor: String
  $limit: Int
) {
  getTokenEvents(
    query: $query
    cursor: $cursor
    limit: $limit
  ) {
    cursor
    items {
      timestamp
      eventType
      token0SwapValueUsd
      token1SwapValueUsd
      token0ValueBase
      token1ValueBase
      maker
      transactionHash
    }
  }
}
```

Example variables:

```json
{
  "query": {
    "address": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
    "networkId": 1
  },
  "limit": 25
}
```

## 11) Maker events (`getTokenEventsForMaker`)

```graphql
query GetTokenEventsForMaker(
  $query: MakerEventsQueryInput!
  $cursor: String
  $limit: Int
) {
  getTokenEventsForMaker(
    query: $query
    cursor: $cursor
    limit: $limit
  ) {
    cursor
    items {
      timestamp
      eventType
      token0SwapValueUsd
      token1SwapValueUsd
      token0ValueBase
      token1ValueBase
      transactionHash
    }
  }
}
```

Example variables:

```json
{
  "query": {
    "maker": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    "networkId": 1,
    "tokenAddress": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
  },
  "limit": 25
}
```

## 12) Holders (`holders`)

```graphql
query Holders($input: HoldersInput!) {
  holders(input: $input) {
    cursor
    count
    top10HoldersPercent
    items {
      address
      balance
      shiftedBalance
      balanceUsd
    }
  }
}
```

## 13) Top-10 holder concentration (`top10HoldersPercent`)

The `tokenId` is a composite ID in `address:networkId` format.

```graphql
query Top10HoldersPercent($tokenId: String!) {
  top10HoldersPercent(tokenId: $tokenId)
}
```

Example variables:

```json
{
  "tokenId": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2:1"
}
```

## 14) Wallet leaders (`filterTokenWallets`)

```graphql
query FilterTokenWallets($input: FilterTokenWalletsInput!) {
  filterTokenWallets(input: $input) {
    results {
      address
      tokenAddress
      networkId
      amountBoughtUsd1d
      amountSoldUsd1d
      realizedProfitUsd1d
      realizedProfitPercentage1d
      buys1d
      sells1d
      labels
    }
  }
}
```

Example variables:

```json
{
  "input": {
    "tokenIds": ["0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2:1"],
    "limit": 25
  }
}
```

## 15) Wallet chart (`walletChart`)

```graphql
query WalletChart($input: WalletChartInput!) {
  walletChart(input: $input) {
    walletAddress
    networkId
    resolution
    data {
      timestamp
      volumeUsd
      realizedProfitUsd
      swaps
    }
  }
}
```

Example variables:

```json
{
  "input": {
    "walletAddress": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    "networkId": 1,
    "range": { "start": 1710000000, "end": 1710600000 },
    "resolution": "1D"
  }
}
```

## 16) WebSocket client (`graphql-ws`)

```typescript
import { createClient } from "graphql-ws";

const client = createClient({
  url: "wss://graph.codex.io/graphql",
  connectionParams: {
    Authorization: process.env.CODEX_API_KEY!,
  },
});

const unsubscribe = client.subscribe(
  {
    query: `
      subscription OnPriceUpdated($address: String!, $networkId: Int!) {
        onPriceUpdated(address: $address, networkId: $networkId) {
          address
          networkId
          priceUsd
          timestamp
          blockNumber
        }
      }
    `,
    variables: {
      address: "So11111111111111111111111111111111111111112",
      networkId: 1399811149,
    },
  },
  {
    next: (msg) => console.log(msg),
    error: (err) => console.error(err),
    complete: () => console.log("done"),
  }
);
```

## 17) Windowed token change stats (`getDetailedTokenStats`)

Period-over-period deltas per window. Complements `filterTokens` on a detailed token page: use `filterTokens` for the header bulk, this for the windowed change breakdown.

```graphql
query DetailedTokenStats($networkId: Int!, $tokenAddress: String!) {
  getDetailedTokenStats(
    networkId: $networkId
    tokenAddress: $tokenAddress
    statsType: FILTERED
  ) {
    stats_min5   { statsUsd { liquidity { previousValue currentValue change } volume { previousValue currentValue change } } }
    stats_hour1  { statsUsd { liquidity { previousValue currentValue change } volume { previousValue currentValue change } } }
    stats_hour4  { statsUsd { liquidity { previousValue currentValue change } volume { previousValue currentValue change } } }
    stats_hour12 { statsUsd { liquidity { previousValue currentValue change } volume { previousValue currentValue change } } }
    stats_day1   { statsUsd { liquidity { previousValue currentValue change } volume { previousValue currentValue change } } }
  }
}
```

Example variables:

```json
{ "networkId": 56, "tokenAddress": "0x299ad4299da5b2b93fba4c96967b040c7f611099" }
```

Notes: flat args (`networkId`, `tokenAddress`, `statsType`), not an input object. `statsType: FILTERED` is the filtered stat set (default is `UNFILTERED`). Window keys are snake_case (`stats_min5`, `stats_hour1`, `stats_hour4`, `stats_hour12`, `stats_day1`) — different from `detailedWalletStats`, whose keys are camelCase (`statsDay1`, `statsWeek1`); easy to transpose. Each metric under `statsUsd` (`liquidity`, `volume`, and others) is a change triple `{ previousValue, currentValue, change }` of strings, not a flat scalar.

## 18) Single-wallet stats (`detailedWalletStats`)

```graphql
query DetailedWalletStats($input: DetailedWalletStatsInput!) {
  detailedWalletStats(input: $input) {
    walletAddress
    lastTransactionAt
    labels
    scammerScore
    botScore
    statsDay1 {
      start
      end
      statsUsd {
        volumeUsd
        realizedProfitUsd
        realizedProfitPercentage
        averageProfitUsdPerTrade
        averageSwapAmountUsd
      }
      statsNonCurrency { swaps uniqueTokens wins losses avgHoldPeriodSec }
    }
    statsWeek1 { statsUsd { volumeUsd realizedProfitUsd } statsNonCurrency { swaps wins losses } }
    statsDay30 { statsUsd { volumeUsd realizedProfitUsd } }
    statsYear1 { statsUsd { volumeUsd realizedProfitUsd } }
    networkBreakdown {
      networkId
      nativeTokenBalance
      statsDay1 { statsUsd { volumeUsd realizedProfitUsd } }
    }
  }
}
```

Example variables:

```json
{
  "input": {
    "walletAddress": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    "networkId": 1,
    "includeNetworkBreakdown": true
  }
}
```

Notes: input is `DetailedWalletStatsInput`; `walletAddress` required, `networkId` / `timestamp` / `includeNetworkBreakdown` optional. Stats are fixed windows (`statsDay1` / `statsWeek1` / `statsDay30` / `statsYear1`), not an arbitrary date range — for a date range use `walletChart` (template #15). The currency sub-object is `statsUsd`, not `statsCurrency`. `networkSpecificStats` is deprecated — use `networkBreakdown`. USD/volume/profit values are strings; `realizedProfitPercentage` and `avgHoldPeriodSec` are floats.

## 19) Live token events (`onTokenEventsCreated`)

```graphql
subscription OnTokenEventsCreated($input: OnTokenEventsCreatedInput!) {
  onTokenEventsCreated(input: $input) {
    id
    events {
      timestamp
      eventType
      eventDisplayType
      maker
      token0SwapValueUsd
      token1SwapValueUsd
      transactionHash
      networkId
      walletLabels
    }
  }
}
```

Example variables:

```json
{
  "input": {
    "tokenAddress": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
    "networkId": 1
  }
}
```

Notes: `networkId` required, `tokenAddress` optional (required unless on an enterprise EventFeed plan). Optional field-level arg `commitmentLevel: [EventCommitmentLevel!]`. Payload is `AddTokenEventsOutput!` (`{ id, events: [Event!]! }`). `Event` has no `priceUsd` — use `token0SwapValueUsd` / `token1SwapValueUsd` (USD) or the base-token values. `eventDisplayType` splits Swap into Buy/Sell.

## 20) Live maker events (`onEventsCreatedByMaker`)

```graphql
subscription OnEventsCreatedByMaker($input: OnEventsCreatedByMakerInput!) {
  onEventsCreatedByMaker(input: $input) {
    makerAddress
    events {
      timestamp
      eventType
      eventDisplayType
      address
      networkId
      token0SwapValueUsd
      token1SwapValueUsd
      transactionHash
    }
  }
}
```

Example variables:

```json
{ "input": { "makerAddress": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045" } }
```

Notes: input has a single required field `makerAddress` — no network or token filter; it streams the maker's activity across networks and tokens. Optional field-level arg `commitmentLevel`. Payload `AddEventsByMakerOutput` (`{ makerAddress, events: [Event!]! }`). Not to be confused with the deprecated Solana-only `onUnconfirmedEventsCreatedByMaker`.

## 21) Live token bars (`onTokenBarsUpdated`)

Differs sharply from `getBars` / `getTokenBars`: there is no flat `bars { t o h l c volume }` array. You get `aggregates: ResolutionBarData`, a per-resolution object — select only the resolutions you need.

```graphql
subscription OnTokenBarsUpdated($tokenId: String!) {
  onTokenBarsUpdated(tokenId: $tokenId) {
    tokenId
    tokenAddress
    networkId
    timestamp
    statsType
    aggregates {
      r1  { t usd { o h l c v } token { o h l c v } }
      r60 { t usd { o h l c v } token { o h l c v } }
      r1D { t usd { o h l c } }
    }
  }
}
```

Example variables:

```json
{ "tokenId": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2:1" }
```

Notes: `tokenId` is the `address:networkId` composite (optional in schema but effectively required unless on an enterprise BarFeed plan). Available resolutions: `r1S`, `r5S`, `r15S`, `r30S`, `r1`, `r5`, `r15`, `r30`, `r60`, `r240`, `r720`, `r1D`, `r7D`. Each is `{ t, usd, token }` where `usd` / `token` are `IndividualBarData` (`{ o, h, l, c, v }` — note `v`, not `volume`; OHLC are Floats, `v` is Int). Pair-level fields (`pairAddress`, `pairId`, `quoteToken`) on this type are deprecated — use `tokenAddress` / `tokenId`.

## 22) Launchpad token events (`onLaunchpadTokenEvent` / `onLaunchpadTokenEventBatch`)

Despite "Event" in the name, the payload is a token snapshot, not a transaction — it carries market cap, per-hour buy/sell/volume, holder-quality percentages (sniper / bundler / insider / dev), and fees, closer to a `filterTokens` row than to `getTokenEvents`. The transaction-type discriminator is the `eventType` enum.

```graphql
subscription OnLaunchpadTokenEvent($input: OnLaunchpadTokenEventInput) {
  onLaunchpadTokenEvent(input: $input) {
    address
    networkId
    protocol
    launchpadName
    eventType
    token { address name symbol networkId decimals info { imageThumbUrl } }
    marketCap
    price
    liquidity
    holders
    buyCount1
    sellCount1
    volume1
    top10HoldersPercent
    devHeldPercentage
    sniperCount
    sniperHeldPercentage
    bundlerHeldPercentage
    insiderHeldPercentage
    devWallet { address }
  }
}
```

Example variables:

```json
{ "input": { "protocols": ["Pump", "RaydiumLaunchpad"], "networkId": 1399811149, "eventType": "Deployed" } }
```

Batched variant (returns an array per emission, more efficient):

```graphql
subscription OnLaunchpadTokenEventBatch($input: OnLaunchpadTokenEventBatchInput) {
  onLaunchpadTokenEventBatch(input: $input) {
    address networkId launchpadName eventType marketCap price
    token { address symbol name }
  }
}
```

Notes: both take an optional input (no input gives the firehose). Filters: `protocol` / `protocols` (enum `LaunchpadTokenProtocol`: `Pump`, `PumpMayhem`, `FourMeme`, `RaydiumLaunchpad`, `BoopFun`, and many more), `launchpadName` / `launchpadNames`, `eventType`, `address` + `networkId`. Single returns `LaunchpadTokenEventOutput!`; batch returns `[LaunchpadTokenEventOutput!]!`. `eventType` (`LaunchpadTokenEventType`): `Deployed`, `Created`, `Updated`, `Completed`, `Migrated` (plus `Unconfirmed*` variants). `protocol` / `launchpadName` come back as plain strings on the output even though the enum is on the input. `volume1` is an Int; most money values are strings; `price` is a Float.

## 23) Manage API tokens (`createApiTokens` / `deleteApiToken`)

Mutations — require the long-lived API key (short-lived tokens can't manage tokens).

```graphql
mutation CreateApiTokens($input: CreateApiTokensInput!) {
  createApiTokens(input: $input) { id token expiresTimeString requestLimit remaining }
}
```

```json
{ "input": { "count": 3, "requestLimit": "5000", "expiresIn": 3600000 } }
```

```graphql
mutation DeleteApiToken($id: String!) {
  deleteApiToken(id: $id)
}
```

```json
{ "id": "your-token-id" }
```

Notes: `createApiTokens` returns `[ApiToken!]!`. `deleteApiToken(id: String!)` takes a flat `id`, not an input object, and returns a plain `String!`. `requestLimit` is a String, not an Int — pass `"5000"`. It counts root-field resolutions before rate-limiting, not requests-per-second. `expiresIn` is milliseconds, not seconds (default `3600000`, one hour). `count` defaults to 1; all three input fields are optional. There is no scopes/permissions field — don't invent one. The returned `token` is the JWT to send as `Authorization: Bearer <token>`.

## 24) Webhooks (`createWebhooks` / `deleteWebhooks`)

Server-side push alerts that POST to a `callbackUrl` when conditions are met — use these for backend/serverless alerting where holding a persistent WebSocket isn't practical. (For live in-app UI, prefer subscriptions, templates #6/#7/#19–#21.) These are mutations, so they require the long-lived API key — they are **not** available under the MPP 402 (codex-gateway) flow, which is query-only. `createWebhooks` takes one wrapper input whose fields each carry a list of typed webhooks; below creates a token-price-event webhook.

```graphql
mutation CreateWebhooks($input: CreateWebhooksInput!) {
  createWebhooks(input: $input) {
    tokenPriceEventWebhooks { id name webhookType status callbackUrl alertRecurrence }
    marketCapWebhooks { id name webhookType status }
  }
}
```

Example variables — alert when WETH crosses above $4000:

```json
{
  "input": {
    "tokenPriceEventWebhooksInput": {
      "webhooks": [
        {
          "name": "weth-above-4000",
          "callbackUrl": "https://example.com/hooks/codex",
          "securityToken": "your-shared-secret",
          "alertRecurrence": "ONCE",
          "conditions": {
            "address": { "eq": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2" },
            "networkId": { "eq": 1 },
            "priceUsd": { "gt": "4000" }
          }
        }
      ]
    }
  }
}
```

Delete by ID:

```graphql
mutation DeleteWebhooks($input: DeleteWebhooksInput!) {
  deleteWebhooks(input: $input) { deletedIds }
}
```

```json
{ "input": { "webhookIds": ["your-webhook-id"] } }
```

Notes: `CreateWebhooksInput` is a wrapper — set the input field for the webhook family you want, each holding a `webhooks: [...]` array, so you can create many at once. Available families (input field → the `webhookType` it produces): `tokenPriceEventWebhooksInput` → `TOKEN_PRICE_EVENT` (token price), `marketCapWebhooksInput` → `MARKET_CAP_EVENT` (market cap / circulating cap), `tokenTransferEventWebhooksInput` → `TOKEN_TRANSFER_EVENT` (wallet transfers), `tokenPairEventWebhooksInput` → `TOKEN_PAIR_EVENT`, `predictionTradeWebhooksInput` → `PREDICTION_TRADE`, `predictionMarketMetricsEventWebhooksInput` → `PREDICTION_MARKET_METRICS_EVENT`. `priceWebhooksInput` is deprecated — use `tokenPriceEventWebhooksInput`. Condition scalars use comparison objects, not flats: equality fields take `{ eq: ... }` (`StringEqualsConditionInput` / `IntEqualsConditionInput`), thresholds take `ComparisonOperatorInput` (`{ gt, gte, lt, lte, eq }`) — and its values are **strings** (`"4000"`, not `4000`). `alertRecurrence` is `INDEFINITE` or `ONCE`. `securityToken` is hashed (SHA-256) into the message so your callback can verify authenticity. Optional `retrySettings`, `bucketKey` (for querying subgroups via `getWebhooks`), `publishingType` (`SINGLE` default, or `BATCH`), and `deduplicate`. `createWebhooks` returns `CreateWebhooksOutput` (one `[Webhook]` list per family); `deleteWebhooks` returns `{ deletedIds }`. List existing webhooks with the `getWebhooks` query.
