## Description:

Collects multi-interval cryptocurrency K-line market data from the Binance API for BTC, ETH, and other Binance-supported USDT trading pairs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[u91win](https://clawhub.ai/user/u91win)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts use this skill to fetch Binance candlestick data for selected symbols and intervals, print recent market data, and save historical K-line records into local SQLite databases for analysis or downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proxy configuration can expose Binance API traffic to an untrusted intermediary.

Mitigation: Run with no proxy or a trusted proxy, and review proxy values before automated execution.

Risk: Untrusted symbol, interval, or database-path values can cause unreliable collection behavior or writes to unintended local paths.

Mitigation: Validate symbol, interval, date range, and database-path inputs before passing them through automation.

Risk: Large historical collection jobs can encounter Binance API availability or rate-limit issues.

Mitigation: Use bounded date ranges, monitor failures, and retry collection only within Binance API usage limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/u91win/skills/crypto-kline-bn)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Configuration]

**Output Format:** [Markdown guidance with shell commands; scripts produce console tables and SQLite database files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public Binance API requests, optional proxy configuration, symbol and interval arguments, date ranges, and local database paths.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
