# Public read contract

Verified against the official Info documentation on 2026-10-09. Mainnet endpoint: `https://api.hyperliquid.xyz/info`. Testnet: `https://api.hyperliquid-testnet.xyz/info`. Every request is POST with `Content-Type: application/json`. No signing or authentication is used. Query the account being examined, not its API-agent address.

The five snapshot request bodies are:

```json
{"type":"userRole","user":"0x1111111111111111111111111111111111111111"}
{"type":"userAbstraction","user":"0x1111111111111111111111111111111111111111"}
{"type":"clearinghouseState","user":"0x1111111111111111111111111111111111111111","dex":""}
{"type":"spotClearinghouseState","user":"0x1111111111111111111111111111111111111111"}
{"type":"frontendOpenOrders","user":"0x1111111111111111111111111111111111111111","dex":""}
```

The history request bodies add epoch-millisecond `startTime` and `endTime`, both inclusive:

```json
{"type":"userFillsByTime","user":"0x1111111111111111111111111111111111111111","startTime":1790812800000,"endTime":1790899200000,"aggregateByTime":false}
{"type":"userFunding","user":"0x1111111111111111111111111111111111111111","startTime":1790812800000,"endTime":1790899200000}
```

Use the actual input values. The example address and dates are synthetic inputs.

## Pagination and completeness

The general time-range documentation limits responses to 500 elements or distinct blocks. Fills by time have an additional 2000-fill response limit and retain only the 10000 most recent fills. Requests after a page use the last returned timestamp as the next inclusive `startTime`. The helper conservatively continues for any page of at least 500 rows, retaining boundary overlap for deduplication. A shorter page ends pagination.

The helper never increments the boundary by one millisecond to escape a saturated timestamp, because that could skip unseen records at that timestamp. A saturated page with no timestamp progress ends as `timestamp-stall`. A finite page budget, read failure or stall keeps coverage partial. Malformed pages are saved in a live capture, then deterministic analysis fails closed.

`api-exhausted` describes the fetched available history only. It does not prove that the requested window predates no retained records or that earlier opening costs are known. `completeWindow` is always false. A gap-free bounded report remains subject to retention and scope limits. Empty data alone does not identify the intended account; the role observation is retained.

## Market and state scope

`dex: ""` selects validator-operated perpetuals. Snapshot positions and outcome accounting cover that DEX only. Fills/funding can include other markets: spot names begin with `@` or contain `/`, while HIP-3 names contain `:`. These are captured and counted as excluded activity, not mixed into default-perp accounting. Other DEX exposure, subaccounts, vaults, staking and lending are not enumerated.

Account abstraction mode is read independently. Under unified/portfolio-margin modes, spot token balances are the authoritative trading-balance endpoint; perpetual margin summary must not be added to them. The helper reports observed balances by token, without a USD conversion or portfolio-equity estimate.

Position state and open orders are current at their sequential read times. They are not historical state at the window end. Open-order flags describe those records only. They do not prove protection between reads or for a matching position size and trigger price.

## Failure bounds

The defaults are 10 pages per history type and 15 seconds per read. Allowed bounds: 1..50 pages and 1..60000 milliseconds. Each response is limited to 8 MiB, with 64 MiB across all raw responses. Offline capture files are limited to 160 MiB, and replay enforces the same per-response and total byte bounds. Redirects and custom endpoints are rejected. HTTP 429, timeouts and other failures are captured without automatic retries; the user or harness can start a fresh bounded capture later.
