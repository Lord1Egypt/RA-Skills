## Description:

Professional BTC risk radar using public options, perp, and spot data. Use when the user wants a clear Bitcoin risk snapshot with volatility/skew context, panic or black-swan validation, timestamped evidence, confidence scoring, and explicit caveats for traders or advanced observers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spyfree](https://clawhub.ai/user/spyfree)

### License/Terms of Use:

MIT-0

## Use Case:

External users, traders, and advanced market observers use this skill to generate timestamped Bitcoin risk snapshots from public options, perpetual, and spot-market data, with confidence scoring, caveats, and action triggers. It supports quick market-risk assessment, not investment advice or automated trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes unauthenticated outbound requests to public crypto exchange APIs, so execution depends on network access and third-party endpoint availability.

Mitigation: Run it only where public exchange API access is acceptable; review data_gaps and degraded_mode before relying on the snapshot.

Risk: The skill produces heuristic market-risk analysis that could be mistaken for financial advice or deterministic prediction.

Mitigation: Present outputs with caveats, confidence score, and not-investment-advice language; avoid automated trading or order placement based on the output alone.

Risk: Some metrics are proxies or approximations, including put-volume share and front-expiry delta-nearest risk reversals.

Mitigation: Label proxy metrics explicitly and use them for situational awareness rather than exact institutional replication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spyfree/skills/btc-risk-radar)
- [Metrics Reference](references/metrics.md)
- [Deribit Public API](https://www.deribit.com/api/v2/public)
- [Coinbase BTC-USD spot price API](https://api.coinbase.com/v2/prices/BTC-USD/spot)
- [Binance Public API](https://api.binance.com/api/v3)
- [OKX Public API](https://www.okx.com/api/v5)
- [Bybit Public API](https://api.bybit.com/v5)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Plain-text or Markdown narrative with optional JSON payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Timestamped BTC market snapshot with risk label, confidence score, availability, data gaps, degraded mode, 72h validation matrix, action triggers, and caveats; language may be English or Chinese.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; script version 0.1.1 differs)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
