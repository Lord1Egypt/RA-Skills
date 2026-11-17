## Description:

A-Share Paper Trading System - Data Fetch, Storage, Backtest, Simulation.

This skill is for research and development only.

## Publisher:

[bombfuock](https://clawhub.ai/user/bombfuock)

### License/Terms of Use:


## Use Case:

External users, developers, and analysts can use this skill to fetch China A-share market data, store it locally, run simple moving-average or momentum backtests, and simulate paper trades. Outputs are educational and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches market data from East Money over HTTP, so unavailable or tampered market data can mislead simulated results.

Mitigation: Verify source data quality before relying on backtest or paper-trading output, and avoid using results as investment advice.

Risk: The skill writes a local SQLite database under ~/.openclaw/workspace/a-stock/, and malformed CLI inputs can corrupt or misstate simulated positions and trades.

Mitigation: Use validated stock codes, share counts, and prices; keep backups or delete the local database before rerunning simulations when results look inconsistent.

Risk: Backtests and paper trades are educational simulations and do not represent real execution, transaction costs, slippage, or future performance.

Mitigation: Review assumptions and strategy outputs manually before making any financial decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bombfuock/skills/a-stock-trader)
- [Publisher profile: bombfuock](https://clawhub.ai/user/bombfuock)
- [East Money daily K-line API endpoint](http://push2his.eastmoney.com/api/qt/stock/kline/get)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and concise trading-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct execution of local Python scripts that read and write a SQLite database under ~/.openclaw/workspace/a-stock/.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
