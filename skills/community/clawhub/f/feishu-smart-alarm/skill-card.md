## Description:

Feishu Smart Alarm reads Feishu/Lark message text, identifies task reminders with deadlines, computes a context-aware lead time, stores a one-time reminder, and sends confirmation and due reminder messages back to the original conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hei-maom](https://clawhub.ai/user/hei-maom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams integrating Feishu/Lark bots use this skill to turn Chinese task and deadline messages into one-time reminders in the original chat. It is suited for private chats or group conversations where reminder creation, confirmation, and due notification should happen through command-line automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured Feishu/Lark API host can receive app credentials and chat content.

Mitigation: Use only trusted HTTPS Feishu/Lark API hosts and keep the default host unless a reviewed deployment requires otherwise.

Risk: Current-directory .env files can supply credentials in untrusted workspaces.

Mitigation: Run the skill from trusted directories and manage secrets outside shared or untrusted workspaces.

Risk: Unrestricted chats or messages could create reminders through the integration.

Mitigation: Restrict allowed chats, senders, and message types before invoking reminder creation, and tightly gate any use of --no-confirm.

Risk: Reminder data is stored locally without declared retention controls.

Mitigation: Place the SQLite database in an access-controlled location and define retention and deletion rules.

## Reference(s):

- [Feishu integration guide](references/integration_cn.md)
- [Chinese time parsing rules](references/time_rules_cn.md)
- [Feishu Open Platform](https://open.feishu.cn)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [JSON command output and Feishu/Lark text messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores one-time reminder records in local SQLite and sends messages through configured Feishu/Lark API credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
