# Pendle decision worksheet

## Read recipe

After resolving the verified market on the selected chain, Foundry can perform these reads:

```sh
cast call "$MARKET" 'readTokens()(address,address,address)' --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$MARKET" 'expiry()(uint256)' --rpc-url "$RPC_URL" --block "$BLOCK"
```

The token tuple is SY, PT, YT. Discover current API paths and query parameters in the [live API schema](https://api-v2.pendle.finance/core/docs), then use the Hosted SDK operation appropriate to swap or redeem. This avoids freezing request bodies across API versions. Record provider version/schema and returned transaction; an HTTP 200 price response is not a simulated route. The schema currently recommends `POST /v3/sdk/{chainId}/convert` under `https://api-v2.pendle.finance/core`; inspect its typed inputs before constructing the body. For URL-only read-only quote preparation, the documented v2 Convert interface takes `tokensIn`, `tokensOut`, `amountsIn`, `receiver` and `slippage`. A pre-expiry paired redemption specifies both PT and YT with equal raw amounts; a post-expiry principal redemption supplies PT alone. Treat returned transaction data as unsigned preparation.

## Synthetic worked comparison

10,000 accounting-asset units buy 10,200 PT with 90 days remaining. Gross hold return is 2%; simple annualized equivalent is approximately 8.11%, effective annualized approximately 8.36%. Neither figure includes gas, fees, a depeg or redemption restrictions. If exit/redemption costs total 30 units, net maturity proceeds are 10,170 units and net holding return is 1.7%. An exact-size early sale quote of 9,950 units is a realized loss of 50 units relative to entry, despite a positive displayed fixed yield.

If the accounting asset is USDe and the output is sUSDe, convert through the actual SY exchange rate and supported redemption path; do not promise 10,200 sUSDe or USD. If expiry has passed but the underlying has a seven-day cooldown, distinguish `PT redeemed` from `desired liquid output received`.

## Primary sources checked 2026-09-27

- [Pendle FAQ](https://docs.pendle.finance/pendle-v2/FAQ)
- [PT, YT and LP distinctions](https://docs.pendle.finance/pendle-academy/cheatsheet-for-the-impatient/pt-yt-lp-cheatsheet)
- [API schema](https://api-v2.pendle.finance/core/docs)
- [Core interfaces](https://github.com/pendle-finance/pendle-core-v2-public)

