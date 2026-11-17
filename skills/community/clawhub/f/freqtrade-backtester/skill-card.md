## Description:

Run Freqtrade backtests for cryptocurrency trading strategies, interpret results, and iterate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cryptocurrency strategy authors use this skill to download historical market data, run and compare Freqtrade backtests, and interpret performance while iterating on strategies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Existing Compose configuration, container image, or strategy code is outside the supplied skill and may affect what runs.

Mitigation: Review those files before execution.

Risk: Exchange credentials can expose account access if given unnecessary permissions or stored insecurely.

Mitigation: Use historical data without authentication when possible; otherwise use read-only keys with trading and withdrawals disabled, and keep secrets in the environment or a gitignored file.

Risk: Historical backtest results may not predict live market performance.

Mitigation: Compare performance across market conditions and treat backtests as historical evidence rather than a guarantee.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/djc00p/skills/freqtrade-backtester)
- [Reading Backtest Results](references/reading-results.md)
- [Iteration Guide: Improving Your Strategy](references/iteration-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Analysis, Guidance]

**Output Format:** [Markdown with shell command examples and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Explains backtest metrics and comparisons; does not include a trading strategy or guarantee future performance.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
