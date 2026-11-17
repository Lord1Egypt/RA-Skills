## Description:

Provides cross-channel message delivery and contact coordination through OpenClaw commands for sending text messages, media attachments, broadcasts, scheduled notifications, and alert-driven updates across common messaging platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to route alerts, reports, summaries, and broadcast messages to people or groups across messaging services such as Feishu, WhatsApp, Telegram, Discord, Slack, Signal, iMessage, Line, and Teams. It supports immediate sends, batch notifications, scheduled delivery, and condition-triggered alert workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can execute unintended shell commands from user-controlled message or target values.

Mitigation: Review before installing or running the script; avoid untrusted recipients, message text, media paths, and target files unless the command construction is fixed.

Risk: Messages, broadcasts, and attachments are transmitted to external communication services.

Mitigation: Confirm recipients, channels, message content, and attachments before sending, especially for broadcasts or scheduled notifications.

## Reference(s):

- [Cross Platform Messenger Claw](https://clawhub.ai/tujinsama/skills/cross-platform-messenger-claw)
- [Cross-platform channel reference](references/channels.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce OpenClaw message commands and notification script usage patterns that transmit content to external messaging services.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
