## Description:

Guide to set up and configure IM channels(Telegram, Discord, Slack, Feishu, Dingtalk) for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[petopagi](https://clawhub.ai/user/petopagi)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to configure Telegram, Discord, Slack, Feishu, and Dingtalk channels and apply the channel setup by restarting the OpenClaw gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Channel setup requires bot tokens, app secrets, gateway tokens, and passwords that could expose messaging integrations if shared or logged.

Mitigation: Treat credentials as sensitive, avoid pasting them into shared terminals or recorded sessions, rotate exposed credentials, and grant each integration only the minimum required scopes.

Risk: Restarting the OpenClaw gateway can interrupt active service.

Mitigation: Tell the user before restarting the gateway and perform the restart during an acceptable maintenance window.

## Reference(s):

- [Channels Setup on ClawHub](https://clawhub.ai/petopagi/skills/channels-setup)
- [Feishu Channel Setup Guide](/root/.openclaw/extensions/feishu/README.md)
- [Dingtalk Channel Setup Guide](/root/.openclaw/extensions/dingtalk-connector/README.md)
- [OpenClaw Channel Setup Guide](/root/.local/share/pnpm/global/5/node_modules/openclaw/docs/channels)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes channel-specific setup commands and restart guidance for OpenClaw.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
