## Description:

Backtesting Framework helps agents produce Python backtesting guidance for futures and stock strategies, including moving average crossovers, RSI mean reversion, Bollinger Bands breakout, custom strategies, and performance reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative analysts use this skill to ask an agent for NumPy-based backtesting examples, strategy signal code, and performance report summaries for futures and stock strategies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backtest output may overstate strategy performance because the sample calculations omit commissions, slippage, and liquidity.

Mitigation: Treat results as hypothetical, add realistic trading frictions, and forward-test strategies before live trading.

Risk: Generated reports may default to the Chinese report format shown in the artifact.

Mitigation: Ask the agent to format reports in the preferred language and review terminology before sharing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhaocaixia888/skills/backtesting-framework)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with Python code blocks and performance-report examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Python examples expect python3 and NumPy; backtest reports are hypothetical and may need user-supplied market data.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
