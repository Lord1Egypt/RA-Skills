## Description:

Extract and store structured information from Feishu group messages, then query it and get AI-generated insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vinzeny](https://clawhub.ai/user/vinzeny)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and team operators use this skill to record Feishu group discussions, query customer or project history, and generate summaries or advice from stored chat-derived records. It supports sales, customer service, legal, project management, and custom knowledge-pack workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive Feishu group chat content may be stored locally as raw or structured records.

Mitigation: Use only for groups where processing is authorized, restrict workspace file permissions, and define retention and deletion procedures before deployment.

Risk: Billing credentials are embedded in the artifact.

Mitigation: Remove the embedded SkillPay key, rotate the exposed credential, and require runtime secret injection before broad use.

Risk: Billing checks may fail open when the billing service is unavailable.

Mitigation: Fail closed on billing errors and require explicit user confirmation before chargeable analysis, advice, or summary operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vinzeny/skills/feishu-group-memory)
- [Feishu Open API](https://open.feishu.cn/open-apis)
- [SkillPay](https://skillpay.me)
- [Sales knowledge pack](artifact/industries/sales.md)
- [Customer service knowledge pack](artifact/industries/customer-service.md)
- [Legal knowledge pack](artifact/industries/legal.md)
- [Project management knowledge pack](artifact/industries/project.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local chat-derived records and Feishu API responses as inputs; analysis, advice, and summaries may require billing checks.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
