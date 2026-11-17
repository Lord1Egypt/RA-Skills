## Description:

OpenClaw data backup skill that helps agents configure and run full or selective backups with ZIP compression, scheduled execution, logging, notifications, and retention management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjj345](https://clawhub.ai/user/hjj345)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to configure, run, schedule, inspect, and clean backups of OpenClaw workspace data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups can include more OpenClaw workspace data than users expect, including sensitive files when broad targets are selected or sensitive-file exclusions remain disabled.

Mitigation: Review backup targets before first use, prefer selective backups, enable sensitive-file exclusions when appropriate, and keep backup storage private.

Risk: Unencrypted backup archives or copied notification prompts can expose secrets, credentials, or messaging tokens.

Mitigation: Enable encryption for sensitive backups, store passwords in a password manager, and avoid saving Telegram tokens or other secrets in copied prompts.

Risk: Custom backup targets that contain parent-directory traversal or absolute paths can expand the backup scope.

Mitigation: Use workspace-relative backup targets and reject targets containing '..' or absolute path syntax before running backup commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hjj345/skills/auto-backup-openclaw-user-data)
- [Configuration Schema](references/config-schema.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [HEARTBEAT Prompt Example](HEARTBEAT_prompt_example.md)
- [Cron Prompt Example](cron_prompt_example.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown or plain text responses with inline shell commands and JSON status or configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When backup commands run, the skill may create local ZIP backup files, backup logs, and configuration files in the user's OpenClaw workspace.]

## Skill Version(s):

1.1.0 (source: server release and package.json; artifact docs note v1.1.0.20260414 released 2026-04-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
