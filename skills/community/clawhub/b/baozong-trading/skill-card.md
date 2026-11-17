## Description:

宝总霸盘Skill helps an agent provide Chinese-language stock analysis, portfolio review, market scanning, strategy backtesting structure, watchlist monitoring, and risk-control guidance across A-share, Hong Kong, and U.S. equity workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-focused agent operators use this skill to structure stock research, daily reviews, watchlist monitoring, backtesting prompts, and risk checks. It is intended as decision-support guidance, not professional investment advice or automated trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad finance-related prompts and produce buy/sell-style analysis templates.

Mitigation: Treat outputs as decision-support only, verify market data independently, and do not rely on them as professional investment advice.

Risk: The artifact states that the skill does not provide real-time market data without external data sources.

Mitigation: Connect and verify current market data through appropriate sources before using any analysis for trading decisions.

Risk: Backtesting and technical-analysis outputs can be misleading when data is incomplete or assumptions are weak.

Mitigation: Review assumptions, data coverage, fees, slippage, and risk metrics before applying any strategy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zmy1006-sudo/skills/baozong-trading)
- [Publisher profile](https://clawhub.ai/user/zmy1006-sudo)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style analytical responses with structured checklists and finance templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stock analysis frameworks, risk warnings, monitoring thresholds, backtesting assumptions, and action-oriented decision-support templates.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
