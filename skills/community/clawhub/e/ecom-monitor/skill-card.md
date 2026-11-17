## Description:

电商数据分析助手 - 导入和管理商品价格数据，生成竞品分析报表，设置价格/库存预警。适用于竞品价格追踪、库存管理、销售报表生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[noworldzz](https://clawhub.ai/user/noworldzz)

### License/Terms of Use:

MIT-0

## Use Case:

External users, e-commerce operators, and developers use this skill to import and manage locally provided product price and inventory data, generate competitive analysis reports, and configure price or stock alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes running dependencies, scripts, cron setup, and alerting configuration that are not bundled in the inspected package.

Mitigation: Review any referenced scripts, dependencies, scheduled tasks, and alert channels before execution.

Risk: The workflow handles e-commerce price and inventory data and may be subject to platform data-use rules.

Mitigation: Use only authorized, user-provided data and confirm compliance with the relevant marketplace policies.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The inspected package contains documentation only; referenced scripts and dependencies are not bundled.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
