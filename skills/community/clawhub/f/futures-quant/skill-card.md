## Description:

期货量化系统 supports CTP-connected futures quantitative workflows for market data handling, strategy development, risk management, backtesting, and trade execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, traders, and financial-analysis teams use this skill to structure futures quant workflows, including data processing, strategy analysis, backtesting, risk checks, and execution planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes live futures order execution and automated strategy runs without clearly requiring confirmation.

Mitigation: Use paper-trading or read-only analysis mode by default, and require manual confirmation before order placement, leverage changes, or automated strategy execution.

Risk: Futures trading guidance can create material financial exposure if treated as autonomous execution advice.

Mitigation: Limit use to explicit futures quantitative tasks, review generated plans before acting, and apply independent risk controls outside the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/futures-quant)
- [Shanghai Stock Exchange Market Data](https://www.sse.com.cn/marketdata/)
- [Nasdaq Index Data](https://www.nasdaq.com/market-activity/indexes/nasdaq)
- [Euronext Market Data](https://www.euronext.com/en/market-data)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured trading workflow outputs, configuration suggestions, and execution status examples.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
