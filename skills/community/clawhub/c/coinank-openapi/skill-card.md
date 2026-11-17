## Description:

Access CoinAnk crypto derivatives market data via API key or Agent Payments Protocol/x402 pay-per-call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[annata](https://clawhub.ai/user/annata)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analysts, and agents use this skill to retrieve CoinAnk cryptocurrency derivatives market data, including K-lines, ETF data, open interest, long/short ratios, funding rates, liquidations, order flow, whale activity, and related analytics. It supports direct API-key access and pay-per-call access when CoinAnk returns an Agent Payments Protocol or x402 payment challenge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates wallet and payment setup to an external OKX payment skill that may change over time.

Mitigation: Use a pinned, verified OKX payment skill version and review the payment flow before installing or updating.

Risk: CoinAnk API keys, wallet credentials, payment proofs, and authorization headers could be exposed if mishandled by an agent or environment.

Mitigation: Keep credentials in a secret store or configured environment, never print or persist them, and send the CoinAnk API key only in the `apikey` request header.

Risk: Pay-per-call requests can authorize real payments.

Mitigation: Independently confirm every non-zero payment amount, token, network, and recipient before authorization, and do not charge speculatively.

## Reference(s):

- [CoinAnk OpenAPI service](https://open-api.coinank.com)
- [OKX Agent Payments buyer integration](https://web3.okx.com/zh-hans/onchainos/dev-docs/payments/payment-use-buyer-ai)
- [ETF OpenAPI reference](references/ETF.openapi.json)
- [Coins and pairs OpenAPI reference](references/coins-and-pairs.openapi.json)
- [Fund flow OpenAPI reference](references/fund-flow.openapi.json)
- [Funding rate OpenAPI reference](references/funding-rate.openapi.json)
- [HyperLiquid whales OpenAPI reference](references/hyperliquid-whales.openapi.json)
- [Indicators OpenAPI reference](references/indicators.openapi.json)
- [K-line OpenAPI reference](references/kline.openapi.json)
- [Large orders OpenAPI reference](references/large-orders.openapi.json)
- [Liquidation OpenAPI reference](references/liquidation.openapi.json)
- [Long-short net OpenAPI reference](references/long-short-net.openapi.json)
- [Long-short ratio OpenAPI reference](references/long-short-ratio.openapi.json)
- [Market order stats OpenAPI reference](references/market-order-stats.openapi.json)
- [News OpenAPI reference](references/news.openapi.json)
- [Open interest OpenAPI reference](references/open-interest.openapi.json)
- [Order flow OpenAPI reference](references/order-flow.openapi.json)
- [Orderbook OpenAPI reference](references/orderbook.openapi.json)
- [RSI screener OpenAPI reference](references/rsi-screener.openapi.json)
- [Trending OpenAPI reference](references/trending.openapi.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Concise text or Markdown with endpoint parameters, access-mode guidance, API response summaries, and payment confirmation prompts when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CoinAnk endpoint details and payment requirements; should not print, persist, or expose API keys, private keys, seed phrases, payment proofs, authorization headers, or wallet-session credentials.]

## Skill Version(s):

1.0.3 (source: server release metadata and user-supplied release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
