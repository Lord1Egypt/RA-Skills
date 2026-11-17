## Description:

Three-layer protection for the OpenClaw gateway: real-time config monitoring with auto-rollback, systemd crash recovery, and tiered notifications via Feishu, Telegram, and Discord.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dios-man](https://clawhub.ai/user/dios-man)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and administrators use Gateway Guardian to protect gateway availability by validating openclaw.json changes, rolling back invalid configs, restarting failed gateway services, and notifying owners or configured teams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent user services and service drop-ins can change gateway restart and recovery behavior.

Mitigation: Review the systemd user services and gateway drop-in before enabling them, and confirm the uninstall path removes the watcher, recovery service, and drop-in.

Risk: Unsafe install or configuration paths could run unintended commands.

Mitigation: Use bundled release files only, pin or verify any remote downloads, and avoid sourcing user-editable configuration as executable shell where possible.

Risk: Notification channel IDs and bot names can affect where operational alerts are sent.

Mitigation: Validate notification IDs and bot names strictly before writing guardian.conf, and keep fallback notification configuration private.

## Reference(s):

- [Gateway Guardian ClawHub Skill](https://clawhub.ai/dios-man/skills/gateway-config-guardian)
- [Dios-Man Publisher Profile](https://clawhub.ai/user/dios-man)
- [README.en.md](artifact/README.en.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include systemd service commands, guardian.conf configuration values, validation checks, uninstall commands, and notification setup guidance.]

## Skill Version(s):

1.6.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
