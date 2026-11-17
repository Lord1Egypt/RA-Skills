## Description:

基于《因子投资：方法与实践》的量化选股系统，融合Fama-French多因子模型与技术面选股，提供集合竞价选股、盘中监控、持仓复盘等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenkunming](https://clawhub.ai/user/shenkunming)

### License/Terms of Use:

MIT-0

## Use Case:

Investors and financial analysis agents use this skill to structure China A-share factor screening, intraday monitoring, holding review, and report generation with Fama-French-style and technical indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a preconfigured holding that may influence analysis or appear in generated reports.

Mitigation: Remove the holding, mark it clearly as sample data, or require the user to provide portfolio details before producing holding-specific analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenkunming/skills/factor-investment)
- [Skill prompt documentation](artifact/prompts/default.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports, tables, scoring summaries, and natural-language investment guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stock screening reports, intraday selection suggestions, holding review reports, portfolio updates, and risk notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
