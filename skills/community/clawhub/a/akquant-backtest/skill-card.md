## Description:

A-share quantitative trading backtesting using AKQuant and AKShare data for testing double moving average, RSI, and custom strategies on Chinese stocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lamtest556-blip](https://clawhub.ai/user/lamtest556-blip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to run A-share strategy backtests, compare moving-average parameters, inspect basic performance metrics, and draft custom quantitative trading strategy code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships apparent private portfolio data in a holdings configuration file.

Mitigation: Review the packaged files before installation and ask the publisher to remove or replace private holdings data with sample data.

Risk: The backtest runner uses a hardcoded import path that may load code from an unexpected workspace location.

Mitigation: Replace hardcoded import paths with package-relative imports before deployment.

Risk: Dependency installation instructions are unpinned and the skill may fetch market data from AKShare or related third-party services.

Mitigation: Pin dependencies, install in an isolated environment, and confirm network/data-provider access policies before running backtests.

## Reference(s):

- [AKQuant Cheat Sheet](references/akquant_cheatsheet.md)
- [AKShare Documentation](https://www.akshare.xyz/)
- [AKQuant GitHub](https://github.com/akfamily/akquant)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include backtest metrics such as total return, trade count, and equity curve summaries.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
