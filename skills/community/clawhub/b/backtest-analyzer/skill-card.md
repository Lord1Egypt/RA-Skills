## Description:

Backtest Analyzer helps agents analyze trading-record CSV files and produce core strategy metrics such as win rate, drawdown, Sharpe ratio, profit factor, best and worst trades, and JSON reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cqdev-ai](https://clawhub.ai/user/cqdev-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, quantitative analysts, and trading-strategy reviewers use this skill to run local analysis of trade CSV files, compute performance and risk metrics, compare dimensions or benchmarks, and export reports for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes local trade CSV files that may contain sensitive portfolio or transaction data.

Mitigation: Run it only on CSV files you intentionally provide, use explicit input and output paths, and keep generated reports within approved storage.

Risk: Generated performance metrics and ratings can be misleading if source data is incomplete, column mapping is wrong, or financial assumptions do not match the strategy.

Mitigation: Review the parsed inputs and generated reports before relying on them for financial decisions or strategy comparisons.

Risk: The main skill description is narrower than the script behavior, which also includes benchmark comparison, frequency, streak, period, stock, and sector analyses.

Mitigation: Review the script help and selected command options before deployment so users understand the full available behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cqdev-ai/skills/backtest-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Terminal text reports and optional JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally against user-provided CSV files; optional output paths can write JSON reports.]

## Skill Version(s):

1.0.0 (source: server release, package.json, CHANGELOG released 2026-07-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
