## Description: <br>
Cryptocurrency market analysis for Bitcoin and Ethereum that fetches 4h (24h) and 1d (30-day) data from Binance API, calculates technical indicators (RSI, SMAs, support/resistance), and provides bullish/bearish sentiment analysis with reasoning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hmzo](https://clawhub.ai/user/hmzo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to generate BTC and ETH market summaries with technical indicators, sentiment, confidence, and reasoning. It is suitable for informational market reporting, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Binance for public market data, so reports depend on external API availability and returned market data. <br>
Mitigation: Run it only in environments where Binance access is expected, and treat missing or stale data as a reason to retry or review the report before use. <br>
Risk: The output is cryptocurrency market analysis and could be mistaken for financial advice. <br>
Mitigation: Use the report as informational analysis only and review conclusions before making financial decisions. <br>
Risk: Optional daily scheduling can repeatedly send market reports to a configured destination. <br>
Mitigation: Enable the schedule deliberately and keep any messaging destination under the user's control. <br>


## Reference(s): <br>
- [Binance Public API](https://api.binance.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [JSON analysis output and human-readable Markdown report guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analyzes BTCUSDT and ETHUSDT using public Binance market data with no API key required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
