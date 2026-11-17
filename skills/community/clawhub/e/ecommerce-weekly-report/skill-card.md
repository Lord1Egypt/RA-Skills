## Description:

把一周电商数据整理成能直接拿去复盘和开会的管理周报——核心指标环比、异动解释、利润质量判断、下周动作清单。适用于电商周报、经营复盘、例会材料。

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce operators, analysts, and managers use this skill to turn weekly store data into a review-ready operating report with KPI movement, anomaly attribution, profit-quality judgment, and prioritized next-week actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The report can mislead decision makers if weekly data uses inconsistent date ranges, tax treatment, attribution windows, currency, or estimate handling.

Mitigation: Confirm the reporting period, metric definitions, and data gaps in the report header, and mark estimates and low-confidence conclusions explicitly.

Risk: The skill uses an opinionated Chinese weekly-report structure that may not match every team's language or meeting format.

Mitigation: Ask the agent to adapt the language, section names, or output format before generating the report when a different audience or template is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leooooooow/skills/ecommerce-weekly-report)
- [电商周报输出模板](references/output-template.md)
- [核心指标口径定义与计算公式](references/kpi-glossary.md)
- [异动归因方法与置信度分级](references/anomaly-analysis-guide.md)
- [周报交付前自检清单](assets/weekly-report-checklist.md)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance]

**Output Format:** [Structured Markdown weekly report with KPI tables, attribution notes, risk summaries, and prioritized action items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The template is opinionated about report structure and may default to Chinese output unless the user asks the agent to adapt the language or format.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
