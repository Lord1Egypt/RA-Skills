# Live evidence

Use official documentation and the public API before secondary dashboards.

## Documentation

Start at `https://hyperliquid.gitbook.io/hyperliquid-docs/llms.txt`. Fetch only the pages needed for the question. Markdown is available by adding `.md` to a documentation URL.

For implementation details, inspect the current official Python SDK release and commit. Do not assume a historical SDK example still matches the exchange.

## Public API

Mainnet reads use `https://api.hyperliquid.xyz/info`; testnet reads use `https://api.hyperliquid-testnet.xyz/info`. All are `POST` requests with JSON.

```bash
HL_BASE=https://api.hyperliquid.xyz
curl -fsSL -X POST "$HL_BASE/info" -H 'Content-Type: application/json' -d '{"type":"allMids"}'
```

Use the smallest request set that settles the question:

| Need | Request |
|---|---|
| Perp identity, precision, leverage, margin table | `meta`, with `dex` for HIP-3 |
| Mark, oracle, mid, funding, OI, volume | `metaAndAssetCtxs` |
| HIP-3 DEX list | `perpDexs` |
| Spot token and pair identity | `spotMeta`, `spotMetaAndAssetCtxs` |
| Current book | `l2Book` |
| Recent prints | `recentTrades` |
| Candles | `candleSnapshot` |
| Historical funding | `fundingHistory` |
| Cross-venue forecast | `predictedFundings` |
| Effective user fees | `userFees`, only with a public account address |

## Identity

Record network, product class, DEX name, API coin name, display name, market index, asset ID, base and quote assets, and observation time. User interfaces may remap names. Resolve the wire identity from metadata, not the display ticker.

For HIP-3, prefix coin names with the DEX name and query that DEX's own metadata. Mainnet and testnet IDs differ.

## Depth

`l2Book` returns at most twenty levels per side. For each requested band:

1. Compute mid from best bid and ask.
2. Sum visible size and notional inside the band.
3. Measure the furthest returned price on each side in basis points from mid.
4. If a side returned twenty levels but did not reach the band, report its sum as `>= visible amount`, not total depth.
5. Request a coarser `nSigFigs` page when needed. Use the finest page that reaches each band and disclose the page.
6. Walk the consuming side for the user's size to estimate volume-weighted price and impact. If visible levels do not fill the size, report `beyond visible depth`.

## Funding

Hyperliquid funding fields are hourly. Cross-venue `predictedFundings` entries can use different intervals by venue and coin. Divide each non-null rate by its own `fundingIntervalHours`; missing intervals stay unknown. State whether positive funding is paid by longs or shorts and use oracle-priced notional for Hyperliquid payment estimates.

## Time series

The public candle endpoint exposes a bounded recent window per interval. Record interval, requested start and end, returned start and end, row count, gaps, duplicates, network, and fetch time. A request completing does not prove the intended history was returned.
