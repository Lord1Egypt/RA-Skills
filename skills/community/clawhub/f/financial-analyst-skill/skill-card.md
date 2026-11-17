## Description:

金融分析师 — 综合趋势判断、周期定位与风险控制的投资分析技能，适用于市场方向判断、行业/公司分析、资产配置、交易策略评估、持仓复盘、杠杆与仓位管理问题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[phoenixlucky](https://clawhub.ai/user/phoenixlucky)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to structure investment questions across market direction, sector analysis, equity or fund review, portfolio diagnosis, trading strategy, and risk or leverage decisions. It helps produce conditional financial analysis with explicit assumptions, information gaps, recommended actions, and key risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial analysis may be mistaken for personalized financial advice or used for consequential buy, sell, leverage, or concentrated-position decisions.

Mitigation: Treat outputs as decision support only, verify market and portfolio data independently, and consult a licensed advisor for consequential decisions.

Risk: Incomplete or stale financial data can lead to misleading cycle, valuation, or risk conclusions.

Mitigation: Require current source data for the target asset, timeframe, benchmark, holdings, fees, and risk constraints before acting on the analysis.

Risk: Leverage or margin-related guidance can amplify losses if users skip drawdown and liquidation checks.

Mitigation: Review leverage recommendations manually and enforce predefined maximum drawdown, position sizing, and forced-reduction rules before execution.

## Reference(s):

- [Financial Analyst Skill on ClawHub](https://clawhub.ai/phoenixlucky/skills/financial-analyst-skill)
- [Financial analysis examples](references/examples.md)
- [Common financial metrics and valuation framework](references/metric-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured bilingual Markdown analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a six-lens framework with conditional conclusions, recommended actions, key risks, assumptions, and verification signals.]

## Skill Version(s):

1.0.0 (source: frontmatter and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
