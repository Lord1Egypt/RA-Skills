# Public price diagnostic

From this skill's directory:

```bash
node scripts/price-check.mjs --provider coingecko --id bitcoin
node scripts/price-check.mjs --provider defillama --id bitcoin --max-age 300
node scripts/price-check.mjs --help
```

Or run `defi-data-skills price-check` from the independently installed npm CLI. Both routes execute the same standalone script, which only needs Node.js 20+.

Each invocation sends one keyless GET to either CoinGecko's public simple-price endpoint or DefiLlama's public coins endpoint. It accepts a single normalized CoinGecko ID (not a ticker or arbitrary URL), requests USD and a timestamp, and validates both before emitting a provenance record. DefiLlama maps that ID through the `coingecko:` namespace. Resolve identity first for any asset other than the known connectivity example.

It reads no environment variables or credentials, follows no redirects, waits at most 10 seconds for headers plus body, and accepts at most 64 KiB. Maximum accepted age defaults to 300 seconds and can be set from 1 to 86400; over-60-second future timestamps fail as clock skew. A freshness check depends on the local clock being correct.

Success includes source, ID, USD price, retrieval and observation times and age. Failure exits nonzero with a stable error code, HTTP status where relevant, and a bounded numeric Retry-After where available. Raw response bodies, network exception messages, cookies and headers are not printed. Authentication failures, rate limits, payment requests, malformed content, oversize payloads and stale data stay failures; the script never escalates to a paid route or silently returns cached data. It performs no automatic retries.

This only proves the selected public price route at that moment. It does not test MCP authentication, plan coverage, RPC connectivity, protocol balances, yield pools, market executability or signer access. Use the official MCP/SDK for wider queries; this diagnostic is not a daemon, general proxy or adapter service.
