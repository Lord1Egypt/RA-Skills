## Description:

Fetches cryptocurrency historical kline data from CoinMarketCap, calculates EMA7, EMA30, and RSI14 indicators, and supports JSON or CSV output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrierdb](https://clawhub.ai/user/harrierdb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to collect recent cryptocurrency OHLC market data and produce technical-indicator datasets for agent workflows, reports, or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JSON or CSV export may not work reliably because the security summary reports broken or inaccurate functionality.

Mitigation: Review and fix wrapper behavior before relying on exported files in production workflows.

Risk: The documented cron command can create repeated CoinMarketCap requests and daily local output files.

Mitigation: Enable scheduled execution only when repeated API requests and local file creation are intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrierdb/skills/cmc-kline-data-collector)
- [Publisher profile](https://clawhub.ai/user/harrierdb)
- [CoinMarketCap data API endpoint](https://api.coinmarketcap.com/data-api/v3.1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with Python and shell examples; generated market data may be JSON or CSV files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces OHLC fields and EMA7, EMA30, and RSI14 indicator values for configured cryptocurrency symbols.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
