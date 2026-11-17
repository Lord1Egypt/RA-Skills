## Description:

高考志愿填报智能规划技能，面向中国高考考生提供分数定位、院校专业匹配、冲稳保策略和信息差机会分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yibeixiaobai](https://clawhub.ai/user/yibeixiaobai)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to generate Gaokao college application planning reports for Chinese provinces, including score positioning, school and major matching, special program checks, and reach-match-safe recommendation tables. The output is advisory and should be checked against official provincial exam authority and university admissions sources before final decisions.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill may ask users for education-related personal details, including exam score, province, subject choices, special eligibility, and budget.

Mitigation: Collect only details needed for the planning task and avoid sharing unnecessary personal information in prompts or generated reports.

Risk: Admissions guidance can be incorrect or become outdated because official scores, policies, quotas, and timelines vary by province and year.

Mitigation: Treat the report as advisory planning support and verify final choices against official provincial exam authority and university admissions sources.

## Reference(s):

- [Source repository](https://github.com/yibeixiaobai/college-admission-planner)
- [ClawHub skill page](https://clawhub.ai/yibeixiaobai/skills/college-admission-plan)
- [院校专业匹配策略参考手册](references/matching-strategy.md)
- [特殊招生通道参考手册](references/special-programs.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with tables, analysis sections, reminders, and action checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include advisory recommendations, search-derived admissions data, and source-check reminders.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
