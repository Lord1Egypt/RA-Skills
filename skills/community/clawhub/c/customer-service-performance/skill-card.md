## Description:

客服绩效核算读取用户提供的坐席工作量数据表与绩效规则表，按可配置权重和阶梯规则逐人核算得分，并输出透明的绩效明细、团队分布和待人工复核清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenobiazizi](https://clawhub.ai/user/zenobiazizi)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-language customer service operations, HR, and team managers use this skill to calculate agent performance from workload data and configurable rules. Results are intended as review material before compensation or performance decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Performance calculations may influence compensation or HR decisions if accepted without review.

Mitigation: Review the detailed calculations and independently validate results before any payroll or performance action.

Risk: Input files may contain employee data.

Mitigation: Use copies of the intended input files and do not send employee data to external support contacts.

Risk: Missing or ambiguous data can produce incomplete scores.

Mitigation: Keep missing values and rule ambiguities in the manual review list rather than treating them as zero.

## Reference(s):

- [Default customer service performance rules](references/rules-default.md)
- [Custom performance rules guide](references/rules-guide.md)
- [Sample performance report](examples/sample-report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Excel workbook when supported; otherwise Markdown tables with a summary and review notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes per-agent calculation details, team distribution, and a manual review list; outputs are for human review before HR or payroll use.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
