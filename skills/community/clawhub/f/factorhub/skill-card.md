## Description:

提供 5500+ 只 A 股的量化因子数据和财经指标，支持因子分析、行情查询、资金流向、财务分析及策略回测

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelfeng](https://clawhub.ai/user/michaelfeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and quantitative analysts use this skill to connect an AI agent to FactorHub for China A-share factor data, market quotes, fundamentals, trading calendars, and strategy backtesting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the third-party FactorHub MCP provider and the factorhub-mcp binary.

Mitigation: Install only when the provider is trusted and verify the required binary source before use.

Risk: China A-share market data, factor analysis, and backtesting outputs could be mistaken for financial advice.

Mitigation: Treat outputs as informational and independently validate data, assumptions, and strategy results before trading or business decisions.

## Reference(s):

- [FactorHub homepage](https://factorhub.cn)
- [ClawHub skill page](https://clawhub.ai/michaelfeng/skills/factorhub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the factorhub-mcp binary and access to the FactorHub service.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
