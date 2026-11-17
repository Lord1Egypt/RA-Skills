## Description:

Send automatic notifications when the OpenClaw gateway starts up. Supports Telegram, WhatsApp, Discord, Slack, Signal, iMessage, IRC, Google Chat, Line, WeChat, Feishu (Lark), and QQ Bot. Triggers on phrases like 'gateway restart notification', 'notify me when gateway starts', 'startup alert'. Run setup script to configure channel and recipient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keaneyan](https://clawhub.ai/user/keaneyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to configure a gateway startup hook that sends notifications to a selected messaging channel when the OpenClaw gateway starts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a persistent OpenClaw hook that automatically sends gateway startup metadata to a configured messaging service.

Mitigation: Install only when that notification behavior is intended, and review the generated config.json and handler.ts before restarting the gateway.

Risk: The uninstall instructions remove the gateway-notify hook directory.

Mitigation: Verify ~/.openclaw/hooks/gateway-notify before using the deletion command.

## Reference(s):

- [Channel Reference](references/CHANNELS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and generated hook configuration/code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Configures a persistent OpenClaw hook for one selected messaging channel and recipient.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
