## Description:

Operate DingTalk messaging APIs through UXC with a curated OpenAPI schema, app-token bearer auth, and robot/service-group guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and run DingTalk v1.0 request/response messaging operations through UXC, including user lookup, one-to-one bot messages, group bot messages, and service group sends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill links a credentialed DingTalk messaging client to an unpinned remote OpenAPI schema.

Mitigation: Use the locally bundled schema or a commit-pinned schema URL before deployment.

Risk: Manual token examples can expose DingTalk app secrets or access tokens if pasted into chats, logs, or shell history.

Mitigation: Prefer managed UXC bootstrap with environment-backed credentials, and avoid sharing real secrets in prompts or command examples.

Risk: Messaging operations can send one-to-one, group, or service group messages to real recipients.

Mitigation: Require explicit user confirmation before executing send operations.

## Reference(s):

- [Usage patterns](references/usage-patterns.md)
- [Curated OpenAPI schema](references/dingtalk-messaging.openapi.json)
- [DingTalk developer docs](https://open.dingtalk.com/document/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON]

**Output Format:** [Markdown with inline bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command guidance for credentialed DingTalk API operations; write operations should be confirmed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
