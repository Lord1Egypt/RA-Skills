## Description:

Monitors email in real time via IMAP IDLE and triggers the OpenClaw agent to notify users through active channels such as Telegram or Discord.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canihojr](https://clawhub.ai/user/canihojr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure a persistent IMAP watcher that delivers new-email events to an agent for notification, triage, and optional reply workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a persistent email-monitoring service with mailbox and agent access.

Mitigation: Review the systemd service before enabling it and install only when continuous mailbox monitoring is acceptable.

Risk: Mailbox credentials and an OpenClaw gateway token are stored locally for the watcher.

Mitigation: Limit local file access, review the generated configuration, and rotate credentials if the host or configuration file is exposed.

Risk: Automatic Himalaya installation introduces supply-chain exposure.

Mitigation: Prefer a preinstalled, verified Himalaya binary or verify the downloaded binary version and checksum before use.

Risk: Email content can influence downstream agent behavior, including reply workflows.

Mitigation: Keep auto-reply disabled or set to approval-only unless the operator accepts the risk of agent-generated replies.

Risk: Auto-detected delivery sessions can send notifications to an unintended active channel.

Mitigation: Set an explicit channel and target in configuration for predictable notification routing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/canihojr/skills/bee-push-email-skill)
- [Publisher profile](https://clawhub.ai/user/canihojr)
- [Himalaya releases](https://github.com/pimalaya/himalaya/releases/latest/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides installation, status checks, Telegram command handling, auto-reply settings, and cleanup for a systemd-based email watcher.]

## Skill Version(s):

1.5.3 (source: server release metadata, _meta.json, CHANGELOG released 2026-03-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
