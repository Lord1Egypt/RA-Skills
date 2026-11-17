## Description:

Crypto Radar monitors cryptocurrency prices and market context for major tokens using public Yahoo Finance, CoinGecko, and Binance data sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gold3bear](https://clawhub.ai/user/gold3bear)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve read-only crypto market snapshots and Chinese-language market commentary for tracked assets such as BTC, ETH, SOL, BNB, XRP, DOGE, ADA, AVAX, DOT, and MATIC.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live requests to public Yahoo Finance, CoinGecko, and Binance endpoints for market data.

Mitigation: Use it only where outbound requests to those public services are acceptable, and treat returned prices as time-sensitive third-party data.

Risk: The skill produces Chinese-language crypto-market commentary, including DXY and VIX macro context, that is not fully disclosed in the short description.

Mitigation: Disclose the language and commentary scope before deployment, and review outputs so users understand they are market context rather than financial advice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gold3bear/skills/crypto-radar)
- [ClawHub Publisher Profile](https://clawhub.ai/user/gold3bear)
- [Yahoo Finance Chart Endpoint](https://query2.finance.yahoo.com/v8/finance/chart/{symbol})
- [CoinGecko Markets Endpoint](https://api.coingecko.com/api/v3/coins/markets)
- [Binance 24hr Ticker Endpoint](https://api.binance.com/api/v3/ticker/24hr)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Chinese-language console text and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public market-data lookup; no credential environment variables detected.]

## Skill Version(s):

1.0.1 (source: server release evidence, created 2026-04-30)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
