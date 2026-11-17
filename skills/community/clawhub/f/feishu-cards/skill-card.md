## Description:

Send customizable interactive Feishu cards with titles, content, buttons, dropdown options, notes, and color templates through Feishu Open API workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seetherianbow](https://clawhub.ai/user/seetherianbow)

### License/Terms of Use:


## Use Case:

Developers and automation authors use this skill to build or send rich Feishu direct-message and group-chat cards when a workflow needs structured notifications, action buttons, dropdown options, or status notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release can send Feishu messages through bundled default app credentials when FEISHU_APP_ID and FEISHU_APP_SECRET are not supplied.

Mitigation: Use a dedicated least-privileged Feishu app, set credentials through environment variables, rotate the exposed defaults, and avoid sensitive content until credential handling is fixed.

Risk: The security guidance flags a recipient-type bug that may affect message sending behavior.

Mitigation: Verify recipient identifiers in a test tenant and prefer known-working open_id or chat_id flows until the recipient-type issue is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seetherianbow/skills/feishu-cards)
- [Feishu message API endpoint](https://open.feishu.cn/open-apis/im/v1/messages)
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown guidance with CLI commands, Python snippets, and Feishu card JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send Feishu messages through configured app credentials; artifact documentation states a 45KB maximum card size.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
