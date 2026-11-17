## Description:

缠论买点扫描闭环用于扫描科创板/创业板缠论一、二、三类买点，滚动复用自选股分组，并生成次日条件单与 HTML 报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[menglaw2308](https://clawhub.ai/user/menglaw2308)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill after market close to run A-share technical screening, maintain rolling watchlist groups, calculate next-trading-day conditional order levels, and produce an HTML report. The output is decision-support technical analysis, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can modify external stock watchlist groups.

Mitigation: Review the planned group changes before execution, verify group contents after connector calls, and use group-scoped moves when clearing reused slots.

Risk: Generated reports and trigger prices depend on current dates and complete K-line data.

Mitigation: Confirm TODAY, NEXT_TRADE, and every 10-trading-day K-line sequence before relying on the report; treat all trigger prices as non-advisory technical analysis.

Risk: HTML report fields may be unsafe if untrusted values are inserted without escaping.

Mitigation: Review generated HTML locally and avoid untrusted report fields until the publisher adds explicit HTML escaping.

## Reference(s):

- [A+B 合并主策略参数表](references/策略参数表.md)
- [ClawHub release page](https://clawhub.ai/menglaw2308/skills/chanlun-scan-closed-loop)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python configuration edits and generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current TODAY, NEXT_TRADE, POOL, and external K-line/watchlist connector data; trigger prices should be reviewed as non-advisory technical analysis.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
