## Description:

Backtest trading strategies against historical market data with performance analytics and risk metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[collierking](https://clawhub.ai/user/collierking)

### License/Terms of Use:


## Use Case:

External developers, quantitative traders, and finance analysts use BacktestBot to define, simulate, compare, and analyze trading strategies against historical market data. It supports strategy evaluation and risk review, not live trading authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a BacktestBot API key and may use a local cache for historical market data.

Mitigation: Confirm the BacktestBot service is trusted with the API key and configure BACKTESTBOT_DATA_DIR only where cached market data is acceptable.

Risk: Backtest results and risk metrics can be mistaken for live trading authority or financial advice.

Mitigation: Use the skill for analysis and backtesting only, and review strategy outputs before making trading decisions.

## Reference(s):

- [BacktestBot on ClawHub](https://clawhub.ai/collierking/skills/backtestbot)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis with performance metrics, risk metrics, strategy comparisons, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BACKTESTBOT_API_KEY for BacktestBot authentication; BACKTESTBOT_DATA_DIR may be used for an optional local historical data cache.]

## Skill Version(s):

0.0.2 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
