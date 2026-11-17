# Trading API recipes

Checked 2026-09-27. Base URL `https://trade-api.gateway.uniswap.org/v1`. Read requests need `x-api-key`; preserve the selected supported router-version header across calls. These shell examples query/build only and never send blockchain transactions.

## Exact-input quote

Create quote-request.json from verified chain/token inputs (addresses are deliberately placeholders):

```json
{
  "type": "EXACT_INPUT",
  "amount": "100000000",
  "tokenInChainId": 8453,
  "tokenOutChainId": 8453,
  "tokenIn": "<verified USDC address>",
  "tokenOut": "<verified WETH address>",
  "swapper": "<wallet address>",
  "slippageTolerance": 0.5,
  "protocols": ["V3"]
}
```

```sh
curl --fail-with-body --silent --show-error 'https://trade-api.gateway.uniswap.org/v1/quote'   -H "x-api-key: $UNISWAP_API_KEY" -H 'Content-Type: application/json'   -H "x-universal-router-version: $UNISWAP_ROUTER_VERSION"   --data-binary @quote-request.json
```

Do not enable shell tracing. Persist response with restricted permissions if needed; API keys and signatures stay out of evidence files.

## Approval check and construction

`POST /check_approval` body includes `walletAddress`, `token`, `amount`, `chainId`; use the same router version and approval mode. Inspect returned approval/revocation transactions independently. `isTokenApprovalApplicable` on the quote describes route mechanics, not the wallet's current allowance.

For CLASSIC, `POST /swap` accepts the `quote` object from the response and, when required, `permitData` and `signature` matching that quote. Read the current request schema for permitted options; never invent a recipient override inside encoded data. For a non-CLASSIC response stop this construction recipe and use that route's documented endpoint. Calling a construction endpoint supplies no wallet execution authority.

## Primary sources

- [Approval schema](https://developers.uniswap.org/docs/api-reference/check_approval)
- [Quote API schema](https://developers.uniswap.org/docs/api-reference/aggregator_quote)
- [Integration guide and routing discriminators](https://developers.uniswap.org/docs/trading/swapping-api/start-building/integration-guide)
- [Permit2 lifecycle](https://developers.uniswap.org/docs/trading/swapping-api/concepts/permit2)
- [Swapping workflow](https://developers.uniswap.org/docs/trading/swapping-api/getting-started)
- [Trading API overview](https://developers.uniswap.org/docs/trading/overview)
