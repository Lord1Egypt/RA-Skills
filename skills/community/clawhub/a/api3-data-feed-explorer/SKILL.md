---
name: api3-data-feed-explorer
description: Explore and analyze Api3 data feeds using public data. Lists which providers support which feeds, shows aggregation composition, fetches latest prices, compares providers (spread/outliers), checks on-chain vs off-chain staleness, and cross-checks feed values against exchange spot prices. Use when asked about Api3 dAPI health, provider coverage, price verification, feed deviation, or staleness.
metadata:
  version: 0.1.0
  clawdis:
    requires:
      bins:
        - ts-node
        - pnpm
---
# Api3 Data Feed Explorer

Analyze Api3 data feeds using only public data sources: Signed API endpoints, on-chain dAPI reads, and public exchange APIs.

## Scripts

All scripts live in `{baseDir}/scripts/`.

### explore-data-feeds.ts

Fetches per-provider off-chain data for a feed from Signed API:

```bash
ts-node {baseDir}/scripts/explore-data-feeds.ts <FEED_NAME>
```

Example: `ts-node {baseDir}/scripts/explore-data-feeds.ts BTC/USD`

Output starts with a config freshness note, then two summary lists, then one block per provider:

```
Note that this dAPI configuration is updated at 2026-06-11T12:00:00.000Z and may not reflect the latest changes.

Providers that support this feed:
[ '- blocksize', '- coingecko' ]
Providers that are used in the aggregation of this feed:
[ '- blocksize', '- coingecko' ]
**************************************************
- API Alias: blocksize
- Data Feed ID: 0x3502633779071a82a8a6a17e9ade05e97aa45dfc390b934cd360bef2e983edd7
- Signed API URL: https://signed-api.api3.org/public/0xBA910Eb2867977A0a651FE3D2607237ff4116B1C
- Homepage: https://www.blocksize.info
- Value: 62883.522017606105
- Timestamp: 2026-06-11T14:10:03.000Z
**************************************************
...
```

The config freshness timestamp is the last-modified date of the feed configuration, not the data itself.

### get-chains.ts

Lists all chains supported by Api3, with their name, alias, and numeric id:

```bash
ts-node {baseDir}/scripts/get-chains.ts
```

Use this to discover valid chain aliases before calling `read-data-feed.ts`.

### get-dapis.ts

Lists all currently active dAPI names:

```bash
ts-node {baseDir}/scripts/get-dapis.ts
```

Use this to enumerate available feeds or verify a feed name before passing it to other scripts.

### read-data-feed.ts

Reads the on-chain value and timestamp for a feed on a specific chain:

```bash
ts-node {baseDir}/scripts/read-data-feed.ts <FEED_NAME> <CHAIN_ALIAS>
```

Example: `ts-node {baseDir}/scripts/read-data-feed.ts BTC/USD ethereum`

Output:

```
Proxy address: 0x...
value     : 62901.234567890123
timestamp : 2026-06-11T14:08:00.000Z
```

The script derives the `Api3ReaderProxyV1` proxy address from the feed name and chain, then reads it via the chain's default public RPC. Use `get-chains.ts` to find valid chain aliases.

## Capabilities

### 1. List which providers support which feeds

Run `explore-data-feeds.ts` for the requested feed(s). The "Providers that support this feed" list in the output are the ones supporting that feed. To answer "which feeds does provider X support", run the script across the relevant feeds and collect where the provider's alias appears.

### 2. Show which providers are used in a feed's aggregation

Run `explore-data-feeds.ts` for the feed. The "Providers that are used in the aggregation" list shows the aggregation participants. Report the provider aliases and count. Note feeds with few providers (≤3) as concentration risk.

### 3. Fetch latest prices for any feed

Run `explore-data-feeds.ts` and report:
- The median of all provider values (this approximates the served price)
- Each provider's value and timestamp
- Flag any provider whose timestamp is older than 5 minutes as stale

### 4. Per-provider price comparison (spread, outliers, live)

From the `explore-data-feeds.ts` output, compute:
- **Median** of all provider values
- **Spread**: (max - min) / median, as a percentage
- **Per-provider deviation**: (value - median) / median, as a percentage
- **Outliers**: any provider deviating more than 0.5% from the median (adjust threshold for volatile or low-liquidity assets)
- **Freshness**: age of each provider's timestamp relative to now

Present results as a table: provider | value | deviation % | timestamp age. Call out outliers and stale providers explicitly.

### 5. On-chain vs. off-chain gap (staleness check)

1. Compute the live off-chain median from the script output (capability 4).
2. If the user has not specified a chain, ask which chain to check (run `get-chains.ts` to list valid aliases).
3. Read the on-chain value with `read-data-feed.ts <FEED_NAME> <CHAIN_ALIAS>`.
4. Report:
   - On-chain value and its timestamp
   - Live off-chain median
   - Gap percentage: (off-chain median - on-chain value) / on-chain value
   - Time since last on-chain update

Interpretation: on-chain data is updated on a 24h heartbeat **or** whenever the off-chain median deviates from the current on-chain value beyond the feed's deviation threshold. A gap within that threshold with an on-chain timestamp under 24h is healthy. A gap exceeding the threshold, or an on-chain timestamp older than 24h, indicates the update mechanism may be stalled.

### 6. List supported chains

Run `get-chains.ts` and report the chain names, aliases, and ids. Use this to answer "what chains does Api3 support?" or to look up a chain alias before calling `read-data-feed.ts`.

### 7. List active dAPIs

Run `get-dapis.ts` and report the names. Use this to answer "what feeds are available?" or to confirm a feed name exists before running other scripts.

### 8. Feed vs. exchange spot composite (divergence check)

1. Compute the off-chain median from the script output.
2. Fetch spot prices for the same pair from public exchange APIs (no keys required), e.g.:
   - Binance: `https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT`
   - Coinbase: `https://api.coinbase.com/v2/prices/BTC-USD/spot`
   - Kraken: `https://api.kraken.com/0/public/Ticker?pair=XBTUSD`
3. Compute the exchange composite as the median of fetched spot prices.
4. Report: feed median, exchange composite, divergence percentage.
5. Flag divergence above 0.5% as notable, above 1% as significant.

Note: stablecoin-quoted pairs (USDT) vs USD pairs can legitimately differ slightly; mention this when comparing.

## Workflow guidance

- Always run the script fresh for each question; do not reuse stale output across questions.
- When asked a general health question ("is BTC/USD healthy?"), run capabilities 4, 5, and 8 together and give a one-paragraph verdict followed by the numbers.
- Report timestamps in UTC and include data age in human-readable form ("23s ago").
- Never invent provider names, values, or feed IDs. Only report what the script and public APIs return. If a feed name is not found, say so.
- All data used by this skill is public. Do not attempt to access internal alerting, dashboards, or private infrastructure.

## Limitations

- Provider list reflects the current feed configuration; historical composition is not available.
- The off-chain median computed here approximates but may not exactly match the on-chain aggregation logic.
- Exchange composite is an external sanity reference, not the feed's source of truth.