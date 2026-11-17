## Description:

Feishu DM Sender lets an OpenClaw agent send text messages to Feishu or Lark users and group chats using configured contacts, open_id, or chat_id values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingzuer](https://clawhub.ai/user/lingzuer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to let an OpenClaw agent notify colleagues, send task results, or coordinate through Feishu or Lark direct messages and group chats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive message content could be sent to the wrong recipient when fuzzy name matching resolves an unintended contact.

Mitigation: Use explicit open_id or chat_id values for sensitive messages and require human confirmation of both recipient and message text before sending confidential business information.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lingzuer/skills/feishu-dm-sender)
- [Feishu Open API](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script emits JSON success or failure results for agent parsing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
