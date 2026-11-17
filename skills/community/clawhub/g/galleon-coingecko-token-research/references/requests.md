# Requests and identity

Reuse an existing official MCP connection when available; discover its current input schema and request only the required identity and price fields. REST fallback uses GET only. Demo uses `https://api.coingecko.com/api/v3` and header `x-cg-demo-api-key`; Pro uses `https://pro-api.coingecko.com/api/v3` and `x-cg-pro-api-key`. Inject existing credentials through the client's protected header configuration. Do not place keys in URLs, shell history or artifacts.

Request sequence for an EVM token:

```text
GET /asset_platforms
GET /coins/{platform}/contract/{address}
GET /simple/token_price/{platform}?contract_addresses={address}&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true
```

Use a cached platform map if available. The contract route resolves provider identity; the price route returns an address-keyed object. Request at most ten addresses for an ordinary comparison, with a 15-second timeout, no redirects, and no automatic retries. The endpoint's provider limit is not a reason to fetch unrelated assets.

A keyless public connectivity example, if the provider currently permits public access:

```sh
curl --fail --silent --show-error --max-time 15 --max-redirs 0 \
 'https://api.coingecko.com/api/v3/simple/token_price/ethereum?contract_addresses=0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48&vs_currencies=usd&include_last_updated_at=true'
```

This is Ethereum USDC, chain 1, and does not identify an arbitrary user token. Public access can be rejected or throttled; do not claim Demo authentication was tested by this request. For key-bearing requests use a maintained SDK or existing protected HTTP tool.

For unlisted assets use the official onchain token/pool endpoints only after resolving the separate network ID via `/onchain/networks`. Inspect contract identity, reserve USD, per-pool volume and observation timestamps. Record whether price comes from an aggregate or a particular pool; a token with one thin pool cannot support a large exit estimate.

Freshness: compute retrieval UNIX seconds minus `last_updated_at`. A missing, non-finite, future or overly old timestamp fails a strict freshness request; don't silently substitute retrieval time. CoinGecko historical chart sampling also differs by range and plan, so a sampled point is not an exact transaction-time valuation.

## Schema and entitlement changes, checked 2026-10-08

[Official changelog](https://docs.coingecko.com/changelog) documents removed optional `community_data` and `developer_data` fields. Do not dereference missing fields, substitute zero scores or claim absent development/community activity from the removal. Keep the public/default request scope and report unsupported observations explicitly.

Wallet balances/PnL are plan-scoped Analyst+ features; selected multi-network token and minute-interval history features have Enterprise access boundaries. An aggregate token/market read does not establish wallet holdings or those entitlements. Discover current API method/plan support and use existing approved access; do not upgrade plans, invoke paid wallet methods or replace unsupported precision with fabricated data.
