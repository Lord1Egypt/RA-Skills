## Description:

Set up automatic notifications when OpenClaw gateway restarts via a user-selected messaging channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deemoartisan](https://clawhub.ai/user/deemoartisan)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to install and manage a persistent gateway startup hook that sends a timestamp-only notification to iMessage, WhatsApp, Telegram, Discord, or Slack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installed hook persists and sends a notification on every OpenClaw gateway startup.

Mitigation: Install only after confirming this behavior, and remove it with scripts/uninstall_gateway_notify.sh followed by a gateway restart when notifications are no longer wanted.

Risk: Notifications pass through the selected third-party messaging provider, which may log message metadata.

Mitigation: Confirm the channel and recipient carefully, keep the default timestamp-only message unless additional data sharing is explicitly accepted, and avoid adding sensitive local details to customized handlers.

Risk: The --yes flag skips the privacy confirmation prompt.

Mitigation: Use --yes only in automation you control where the channel, recipient, and data flow have already been reviewed.

Risk: Activating or deactivating the hook may require restarting the gateway, which can briefly disconnect the current session.

Mitigation: Warn users before restart and plan for manual reconnect if auto-reconnect is unavailable.

## Reference(s):

- [Gateway Notify on ClawHub](https://clawhub.ai/deemoartisan/skills/gateway-notify)
- [Security & Privacy](SECURITY.md)
- [Manual Setup Guide](references/MANUAL.md)
- [Supported Channels](references/CHANNELS.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose running setup or uninstall scripts that create or remove a persistent OpenClaw gateway startup hook.]

## Skill Version(s):

2.1.5 (source: frontmatter and changelog, released 2026-07-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
