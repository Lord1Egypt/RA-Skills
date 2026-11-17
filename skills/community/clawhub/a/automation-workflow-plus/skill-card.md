## Description:

帮你把每周重复做的事变成自动运行的机器人。识别高价值自动化场景、选对工具（Dify / Coze / n8n 工作流，或零Token的RPA脚本）、设计流程模板、计算ROI回报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[laziobird](https://clawhub.ai/user/laziobird)

### License/Terms of Use:

MIT-0

## Use Case:

External users, operators, and developers use this skill to identify repeatable business workflows, choose between workflow platforms and RPA, design automation flows, test and monitor them, and estimate ROI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes examples that place account credentials in task descriptions.

Mitigation: Do not paste real passwords into chats or automation prompts; use secure secret storage and replace examples with placeholders.

Risk: The skill recommends reusable browser cookies and saved login state for RPA workflows.

Mitigation: Use encrypted session storage, isolated least-privilege accounts, and organization-approved handling for cookies or session files.

Risk: The skill discusses automating internal finance and reconciliation workflows.

Mitigation: Review workflows before use, constrain access to the minimum required systems, and require human review for financial outputs before relying on them.

Risk: The skill points users toward external automation platforms and packages.

Mitigation: Pin or review package versions and evaluate third-party platform permissions before connecting production accounts.

## Reference(s):

- [Dify](https://dify.ai)
- [Dify GitHub Repository](https://github.com/langgenius/dify)
- [Coze China](https://www.coze.cn)
- [Coze Global](https://www.coze.com)
- [n8n](https://n8n.io)
- [n8n GitHub Repository](https://github.com/n8n-io/n8n)
- [OpenClaw RPA Skill](https://clawhub.ai/laziobird/openclaw-rpa)
- [OpenClaw RPA Chinese README](https://github.com/laziobird/openclaw-rpa/blob/main/README.zh-CN.md)
- [OpenClaw RPA Amazon Bestsellers Scenario](https://github.com/laziobird/openclaw-rpa/blob/main/articles/scenario-amazon-bestsellers.en-US.md)
- [OpenClaw RPA Airbnb Compare Scenario](https://github.com/laziobird/openclaw-rpa/blob/main/articles/scenario-airbnb-compare.en-US.md)
- [OpenClaw RPA Accounts Payable Reconciliation Scenario](https://github.com/laziobird/openclaw-rpa/blob/main/articles/scenario-ap-reconciliation.en-US.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with tables, workflow templates, ROI calculations, and inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform recommendations, RPA prompts, workflow setup steps, monitoring checklists, and automation ROI calculations.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence, created 2026-04-21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
