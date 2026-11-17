## Description:

简单易用的个人支出追踪和预算管理工具。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangjingzhi07](https://clawhub.ai/user/huangjingzhi07)

### License/Terms of Use:


## Use Case:

个人用户可用此技能记录支出、查看按日期或类别汇总的消费统计、设置月度预算，并生成月度支出报表。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Expense and budget details may be stored in local JSON files on the machine where the skill runs.

Mitigation: Use the skill on trusted machines and review or delete expenses.json and budget.json when handling shared environments.

Risk: Broad Chinese finance phrases may activate the skill when the user is discussing finances generally.

Mitigation: Confirm the intended tracking or budget action before recording expenses or changing budget data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangjingzhi07/skills/expense-tracker-oc)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Natural-language responses with local JSON-backed expense and budget records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use expenses.json for expense records and budget.json for budget settings.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
