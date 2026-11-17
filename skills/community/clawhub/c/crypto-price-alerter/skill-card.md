## Description:

Monitors live cryptocurrency prices, technical indicators, support and resistance levels, and customizable price alerts for portfolio summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch CoinGecko cryptocurrency market data, calculate simple technical indicators, and generate threshold-based price alerts in text or JSON form.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crypto symbols and selected fiat currencies are sent to CoinGecko for market-data lookups.

Mitigation: Use the skill only with symbols and currencies that are acceptable to disclose to the external market-data provider.

Risk: Technical signals and price alerts may be mistaken for investment advice.

Mitigation: Treat generated indicators, alerts, and summaries as informational only and review them before making financial decisions.

Risk: Broad crypto and trading triggers may activate the skill in generic market discussions.

Mitigation: Confirm the requested symbol, currency, thresholds, and output format before running the price-check command.

## Reference(s):

- [Technical Signals Reference](references/signals.md)
- [ClawHub Skill Page](https://clawhub.ai/fuzzyb33s/skills/crypto-price-alerter)
- [CoinGecko Search API Endpoint](https://api.coingecko.com/api/v3/search)
- [CoinGecko Simple Price API Endpoint](https://api.coingecko.com/api/v3/simple/price)
- [CoinGecko Coins API Base](https://api.coingecko.com/api/v3/coins)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text report or JSON object from a command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes live price, 24h change, volume, market cap, SMA, RSI, support/resistance, timestamp, and alert messages when thresholds are crossed.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
