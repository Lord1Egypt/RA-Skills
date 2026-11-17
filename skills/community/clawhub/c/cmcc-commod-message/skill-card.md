## Description:

中国移动新消息（5G 消息 / RCS）收发工具，支持通用 AI Agent、普通 CLI，并兼容 Hermes Skill。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzzhe2333](https://clawhub.ai/user/zzzhe2333)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure a local CMCC 5G/RCS messaging client, send text or media, validate API-key connectivity, and listen for received messages through CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A CMCC API key could be exposed through chat, logs, or committed files.

Mitigation: Keep the key in the local state .env or environment variable, do not paste real keys into chat, and verify that logs and responses only show masked credentials.

Risk: An agent could be induced to send unintended local files.

Mitigation: Place only files intended for transmission in the configured outbox and preserve the outbox-only file sending restriction.

Risk: Received messages or media could be treated as trusted instructions or unsafe downloads.

Mitigation: Do not execute remote message content as shell commands or privileged agent instructions, and keep automatic media download disabled unless the media host allowlist is trusted.

Risk: Changed messaging or upload endpoints could redirect credentials or media.

Mitigation: Review server and upload URLs before use and keep the HTTPS/WSS and TLS validation requirements enabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zzzhe2333/skills/cmcc-commod-message)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send and receive text or media through the configured CMCC 5G/RCS service; local file sending is limited to the configured outbox directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact declares 1.0.0-universal)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
