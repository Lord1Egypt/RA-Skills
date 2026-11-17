## Description:

Provides expert guidance for systematic backtesting and validation of quantitative trading strategies, including robustness testing, slippage modeling, bias prevention, and interpretation of results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, quantitative researchers, and strategy reviewers use this skill to evaluate whether trading strategies are robust enough to consider for live deployment. It helps structure hypothesis definition, parameter robustness testing, out-of-sample validation, Monte Carlo stress testing, execution-cost modeling, and walk-forward analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading methodology content may be mistaken for financial advice or profitable trade signals.

Mitigation: Treat the skill as a validation framework only; require independent financial, risk, and compliance review before using any strategy in live trading.

Risk: Backtest results can be misleading if they ignore slippage, commissions, survivorship bias, look-ahead bias, or overfitting.

Mitigation: Use the skill's staged validation process, including out-of-sample tests, Monte Carlo stress testing, realistic execution friction, and walk-forward analysis.

Risk: The optional evaluator writes report files to disk.

Mitigation: Choose the output directory intentionally and review generated JSON and Markdown reports before sharing or retaining them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/clawdiri-ai/skills/einstein-research-backtest-dv)
- [ClawHub Publisher Profile](https://clawhub.ai/user/clawdiri-ai)
- [Backtesting Methodology Reference](references/methodology.md)
- [Learning from Failed Backtests](references/failed_tests.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Natural-language guidance with optional JSON and Markdown evaluator reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optional evaluator script writes timestamped JSON and Markdown reports to the selected output directory; no API keys, broker access, network access, or credential use is indicated.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
