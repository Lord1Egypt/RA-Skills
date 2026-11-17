## Description:

Automates daily compressed backups of OpenClaw configurations, agent workspaces, environment files, scripts, and related data with seven-day rotation and restore guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harvnk](https://clawhub.ai/user/harvnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up daily OpenClaw backups, retention, and restore procedures for disaster recovery. It is especially relevant for installations with agent configs, workspaces, scripts, API keys, and environment files that need recoverable backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups may contain sensitive files such as API keys, environment files, workspaces, and operational configuration.

Mitigation: Add encryption at rest, restrict backup and log permissions, and exclude or separately encrypt `.env` files before operational use.

Risk: Restore commands can overwrite system state or expose restored secrets if run directly on a live host.

Mitigation: Extract restores into a staging directory first, validate contents and ownership, and rotate secrets after a restore or suspected exposure.

Risk: The restore flow references a remote installer command that should be trusted before execution.

Mitigation: Verify or replace the remote installer flow before using it in recovery procedures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harvnk/skills/daily-backup-system)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and cron configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes restore guidance and backup rotation instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
