## Description:

Analyzes China macro conditions by scoring growth, inflation, exchange rate, interest rate, and credit indicators, identifying the Merrill Lynch clock phase, and producing asset allocation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenge791](https://clawhub.ai/user/stevenge791)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and agents use this skill to produce China-focused macro climate reports, cycle-stage assessments, and educational asset allocation guidance from market and macroeconomic indicator data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Macro scores, cycle labels, and allocation suggestions may be misleading if market data is stale, incomplete, or incorrect.

Mitigation: Verify the underlying indicator data independently and review confidence labels before relying on the report.

Risk: Asset allocation percentages and sector suggestions could be mistaken for personalized investment advice.

Mitigation: Treat outputs as educational analysis and consult a qualified financial professional before making investment decisions.

Risk: Unavailable indicators or proxy substitutions can reduce reliability of dimension-level scores.

Mitigation: Label missing or approximate data clearly and prefer complete five-year history windows where available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stevenge791/skills/china-macro-climate)
- [中国宏观景气分析 — 指标体系](references/indicators.md)
- [美林投资时钟 — 经济周期与大类资产配置](references/merrill-lynch-clock.md)
- [宏观景气打分方法论](references/scoring-methodology.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with optional JSON or plain-text scoring output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses supplied or retrieved macro and market indicators; allocation percentages and sector suggestions should be treated as educational analysis and independently verified.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
