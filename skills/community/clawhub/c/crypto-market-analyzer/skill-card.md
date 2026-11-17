## Description:

Cryptocurrency market analysis for Bitcoin and Ethereum. Fetches 4h (24h) and 1d (30-day) data from Binance API, calculates technical indicators (RSI, SMAs, support/resistance), and provides bullish/bearish sentiment analysis with reasoning. Use when user asks for crypto market reports, BTC/ETH analysis, or daily market summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmzo](https://clawhub.ai/user/hmzo)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate Bitcoin and Ethereum market summaries from public Binance data, including technical indicators and bullish, bearish, or neutral sentiment reasoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Binance's public API and depends on current third-party market data availability.

Mitigation: Run it only in environments where outbound access to the Binance public API is acceptable, and treat API errors or missing data as report limitations.

Risk: Scheduled execution and messaging delivery can create recurring automated reports.

Mitigation: Enable cron execution and delivery only after confirming the destination, schedule, and user intent.

Risk: Market sentiment summaries may be mistaken for financial advice.

Mitigation: Present outputs as informational technical analysis and require human review before making trading or investment decisions.

## Reference(s):

- [Binance Public API endpoint](https://api.binance.com)
- [Crypto Market Analyzer on ClawHub](https://clawhub.ai/hmzo/skills/crypto-market-analyzer)

## Skill Output:

**Output Type(s):** [analysis, json, markdown, shell commands, guidance]

**Output Format:** [JSON market-analysis output and optional human-readable Markdown-style report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language explanatory report text is expected unless the skill is modified.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
