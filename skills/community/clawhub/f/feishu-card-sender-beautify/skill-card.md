## Description:

Sends Feishu Interactive Card messages for richer card-style push notifications and formatted updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kolikoliko](https://clawhub.ai/user/kolikoliko)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to format and send Feishu Interactive Card notifications to users or group chats. It is suited for user-requested cards, scheduled updates, and structured notification workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send Feishu messages to user or group recipients, and broad triggers could result in unintended notifications.

Mitigation: Require explicit recipient IDs and user confirmation before sending sensitive or broad-audience messages.

Risk: The referenced Feishu permissions include inbound message access even though the main behavior is message sending.

Mitigation: Grant only the minimum Feishu app permissions needed for the intended workflow and avoid inbound access unless separately required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kolikoliko/skills/feishu-card-sender-beautify)
- [API guide](references/api-guide.md)
- [Card templates](references/card-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, code, configuration]

**Output Format:** [Markdown with Python examples and JSON card structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to guide Feishu message construction and recipient targeting.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
