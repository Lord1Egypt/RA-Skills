## Description:

Trade Polymarket 5-minute crypto fast markets using 1-minute candle body analysis and volume surge detection from Binance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mibayy](https://clawhub.ai/user/mibayy)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to run or adapt a Polymarket fast-market trading bot that evaluates short-interval crypto candle structure and volume before deciding whether to place a trade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Polymarket trades, including when scheduled under cron.

Mitigation: Run in dry-run mode first, enable --live only deliberately, and avoid unattended scheduling until trade behavior and sizing are reviewed.

Risk: The configured max position should not be treated as a hard per-trade maximum.

Mitigation: Review and cap trade sizing independently before live use.

Risk: A Simmer API key is required for trading access.

Mitigation: Use a dedicated API key with the least practical account authority and rotate it if exposed.

Risk: Runtime dependencies and external market data affect trade decisions.

Mitigation: Pin dependencies and monitor Binance and Simmer responses before relying on automated execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mibayy/skills/candle-momentum)
- [Binance klines API endpoint](https://api.binance.com/api/v3/klines)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce dry-run trade summaries by default and live trading status when explicitly run with --live.]

## Skill Version(s):

2.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
