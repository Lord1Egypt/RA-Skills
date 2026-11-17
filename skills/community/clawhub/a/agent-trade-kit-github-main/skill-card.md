## Description:

Automatically monitors OKX Flash Earn, Fixed Earn, and Flexible Earn opportunities, sends push notifications, and guides subscription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satawat10](https://clawhub.ai/user/satawat10)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor OKX earn opportunities, configure scan thresholds and notification channels, and receive guidance before subscribing to Fixed Earn products.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses an authenticated OKX CLI and may guide live financial actions.

Mitigation: Use it only with accounts and permissions you intend to expose, and require explicit user confirmation before any subscription, redemption, transfer, or purchase flow.

Risk: The skill can create persistent scheduled execution through cron, LaunchAgent, or OpenClaw cron.

Mitigation: Review and explicitly approve scheduler creation, inspect the installed job, and disable or remove the job when monitoring is no longer needed.

Risk: Credential or notification-token handling can expose sensitive values if users paste secrets into chat or logs.

Mitigation: Keep OKX credentials in the OKX CLI configuration and Telegram credentials in environment variables; do not provide secrets through natural-language chat.

Risk: Cron environment and env.snapshot path issues can cause failed or unintended background behavior.

Mitigation: Run the activation smoke tests, including the minimal cron environment test, and verify env.snapshot, cron logs, and notification delivery before relying on scheduled monitoring.

Risk: Dependency installation relies on the OKX CLI package.

Mitigation: Use an explicitly pinned and integrity-verified OKX CLI package before deployment.

## Reference(s):

- [Configuration Reference](artifact/references/config-reference.md)
- [Notification Channels](artifact/references/notify-channels.md)
- [Purchase Guide](artifact/references/purchase-guide.md)
- [Scan Logic](artifact/references/scan-logic.md)
- [Scheduler Setup](artifact/references/scheduler-setup.md)
- [OKX Homepage](https://www.okx.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown messages with JSON configuration changes and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local OKX earn-hunter config, state, scheduler, and notification log files during activation or operation.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
