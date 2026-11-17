## Description:

Manage Feishu (Lark) group chats using natural language, including listing groups or members, adding or removing members, sending group messages, renaming groups, and creating new groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vinzeny](https://clawhub.ai/user/vinzeny)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and administrators use this skill to manage Feishu group chats from natural-language requests while the agent resolves groups, users, permissions, confirmations, and billing prompts. It is intended for operational Feishu workspace tasks such as member management, announcements, group creation, and group renaming.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires trust in the publisher with Feishu app credentials and live group-management authority.

Mitigation: Install only after reviewing the publisher and limiting Feishu app permissions to the minimum needed workspace scope.

Risk: Bearer tokens and billing identifiers may be exposed through command output, arguments, or operational logs.

Mitigation: Avoid sharing logs that include command lines or JSON results, and prefer a release that removes raw token printing and token passing through argv.

Risk: Billing behavior should fail closed before normal use.

Mitigation: Confirm the billing flow and identity sharing model before enabling billable write operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vinzeny/skills/feishu-group-ops)
- [Feishu Open Platform](https://open.feishu.cn/open-apis)
- [SkillPay](https://skillpay.me)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Natural-language guidance with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Feishu credentials and may perform billable write operations after user confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
