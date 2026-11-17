## Description:

Comprehensive cryptocurrency market monitoring and economic data analysis for tracking crypto prices, market sentiment, economic data releases, and how economic indicators may affect crypto markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kjjjj0](https://clawhub.ai/user/kjjjj0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to monitor cryptocurrency prices, generate market and economic-data reports, update released economic values, and receive analysis-oriented guidance for market context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial and economic-data analysis may be incomplete, generated, or unsuitable as a sole basis for trading decisions.

Mitigation: Verify market and economic data independently before acting on the reports or analysis.

Risk: Hard-coded root paths and import behavior may fail in normal environments or encourage unnecessary privileged execution.

Mitigation: Install in an isolated workspace, avoid sudo, and fix paths and imports before running or scheduling the scripts.

Risk: Cron-based monitoring repeatedly fetches public market data and writes local JSON data and logs.

Mitigation: Review cron entries, filesystem paths, permissions, and logging locations before enabling scheduled execution.

## Reference(s):

- [Installation Guide](INSTALL.md)
- [Quick Reference](references/quick-reference.md)
- [Economic Data Types](references/data-types.md)
- [Usage Examples](references/usage-examples.md)
- [ClawHub Skill Page](https://clawhub.ai/kjjjj0/skills/crypto-market-publish)
- [ClawHub Publisher Profile](https://clawhub.ai/user/kjjjj0)
- [CoinGecko Markets API](https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={ids}&order=market_cap_desc&sparkline=true&price_change_percentage=1h,24h,7d,30d)
- [CoinGecko Global API](https://api.coingecko.com/api/v3/global)
- [Binance 24hr Ticker API](https://api.binance.com/api/v3/ticker/24hr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, json data, guidance]

**Output Format:** [Markdown guidance with shell command examples, text reports, and local JSON data updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches public market data, writes local JSON data and logs, and can be scheduled with cron after local paths are reviewed.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
