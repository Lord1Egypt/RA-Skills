## Description:

Provides expert guidance for developing, testing, stress-testing, and validating systematic quantitative trading strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, quantitative researchers, and systematic traders use this skill to structure backtests, stress-test trading assumptions, identify fragile results, and decide whether a strategy is robust enough for further validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake educational backtesting guidance for financial advice or for an automated trading system.

Mitigation: Treat the output as educational guidance only and independently validate data quality, assumptions, execution costs, and regulatory or tax implications before risking capital.

Risk: Backtest conclusions can be misleading when sample size, data alignment, slippage, market regime coverage, or overfitting controls are weak.

Mitigation: Use conservative friction assumptions, out-of-sample validation, sufficient trade counts, regime analysis, and explicit bias checks before considering live implementation.

## Reference(s):

- [Backtesting Methodology Reference](references/methodology.md)
- [Learning from Failed Backtests](references/failed_tests.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Educational backtesting guidance only; it does not execute code, access external systems, persist data, or place trades.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
