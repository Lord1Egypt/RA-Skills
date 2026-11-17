## Description:

Query real-time cryptocurrency prices, market data, and trends across major exchanges including Binance, Coinbase, and Kraken.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, traders, and portfolio operators use this skill to fetch public cryptocurrency quote data, compare major coins, and summarize market movement for pre-trade checks, tracking, sentiment review, or alerting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill calls public cryptocurrency market-data APIs and may expose requested symbols or query timing to those providers.

Mitigation: Use it only for symbols and market checks that are acceptable to send to public data providers.

Risk: Returned prices can be stale, rate-limited, unavailable, or inconsistent across exchanges.

Mitigation: Treat responses as informational market data and verify material decisions against authoritative exchange or portfolio systems.

Risk: The artifact includes Chinese-language output examples that may not match every user's preferred response language.

Mitigation: Ask the agent for the desired response language or formatting before presenting final market summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaocaixia888/skills/crypto-market-quotes)
- [Binance 24-hour ticker endpoint](https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT)
- [CoinGecko markets endpoint](https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&page=1&sparkline=false)
- [Kraken ticker endpoint](https://api.kraken.com/0/public/Ticker?pair=XBTUSD)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and market summary tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include live public market data, USD-denominated quote summaries, exchange-specific ticker fields, and rate-limit handling guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
