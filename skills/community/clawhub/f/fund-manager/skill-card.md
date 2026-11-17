## Description:

猎金者私人基金经理AI — 集成巴菲特投资哲学、专业财务分析、技术分析、宏观经济研判、基金投资框架于一体的完整投研系统。管理约5,000元人民币基金组合，覆盖8只场外基金持仓，支持每日监控、深度分析、调仓建议、风险预警。

This skill is ready for commercial/non-commercial use.

## Publisher:

[amateur6](https://clawhub.ai/user/amateur6)

### License/Terms of Use:

MIT-0

## Use Case:

External retail investors and agent users use this skill to monitor fund portfolios, analyze financial, technical, and macro signals, and generate research reports, risk alerts, and rebalancing suggestions. Trading suggestions should be treated as informational rather than licensed financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes real portfolio details.

Mitigation: Remove or replace personal portfolio data before installing or sharing the skill.

Risk: The skill directs agents to read a hard-coded persistent memory path and write reports automatically.

Mitigation: Replace the hard-coded path with a user-selected portfolio file and require confirmation before reading or writing local files.

Risk: The skill can produce trading or rebalancing suggestions.

Mitigation: Treat financial guidance as informational and review recommendations with appropriate financial expertise before taking action.

Risk: The skill requests broad read, write, command, and web capabilities.

Mitigation: Install only in environments where those permissions are acceptable and review commands before execution.

## Reference(s):

- [Fund Manager ClawHub Skill Page](https://clawhub.ai/amateur6/skills/fund-manager)
- [巴菲特投资哲学精华浓缩版](references/buffett-core.md)
- [完整财务指标公式库](references/financial-metrics.md)
- [基金投资专用框架](references/fund-framework.md)
- [宏观经济指标手册](references/macro-indicators.md)
- [技术分析完整指南](references/technical-analysis.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with tables, risk alerts, action proposals, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include portfolio monitoring summaries, market analysis, fund research, and rebalancing suggestions; outputs should be reviewed before acting on financial recommendations.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
