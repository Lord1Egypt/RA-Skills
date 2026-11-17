# Official public research routes

Reviewed 2026-10-08 against [Polymarket documentation](https://docs.polymarket.com/llms.txt) and [official CLI source](https://github.com/Polymarket/polymarket-cli).

[Market discovery](https://docs.polymarket.com/market-data/discover-markets) and [prices/order books](https://docs.polymarket.com/market-data/prices-order-books) define Gamma discovery and the official public client/API route. Current Gamma `version` determines whether `positionIds` or JSON-encoded `clobTokenIds` identify the outcomes. Parse arrays, confirm lengths/order and keep identifiers as strings. The current unified client uses `assetId`; older raw CLOB book responses use `asset_id`. A newer API may use different fields, so normalize explicitly before comparing.

The Rust CLI is experimental. Its README documents public `markets`, `events`, `clob book`, `clob price`, `clob midpoint`, `clob tick-size`, `clob fee-rate`, `clob neg-risk` and `clob geoblock` reads. Its CTF examples alone are insufficient evidence of Protocol V2 ledger support. Prefer the maintained public client for a ledger the installed CLI cannot resolve. Do not run `setup`, `wallet create/import/show`, `approve set`, authenticated trading commands or lifecycle writes for a research task. Never put a private key in command arguments.

## Saved-book helper

Save a public JSON book, then run:

```bash
node scripts/book-summary.mjs --file book.json --asset 123456789012345678901 --shares 5 --now-ms 1791446400000 --max-age-ms 60000
```

`--now-ms` is your explicit observation comparison time, not a replacement for the provider timestamp. The helper accepts raw `asset_id` or normalized `assetId`, decimal price/size levels, and an epoch-millisecond `timestamp`. Missing time remains unknown. It uses approximate JavaScript arithmetic for research, excludes fees, and never reports signable amounts or execution. It rejects malformed or duplicate aggregated levels, mismatched identities and invalid inputs, finds best prices independently of ordering, and labels stale, future or crossed observations. Input is bounded to a regular file of 2 MiB and 10,000 levels per side; larger sources need a deliberately bounded research sample, identified as partial coverage.

No paid route, authentication or provider adapter is installed by this skill. Public read access does not establish account eligibility, resolution truth or execution.
