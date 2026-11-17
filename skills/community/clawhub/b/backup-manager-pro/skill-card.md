## Description:

Manages local OpenClaw backups by scheduling configuration backups, cleaning expired archives, and creating pre-change snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reaperchen](https://clawhub.ai/user/reaperchen)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and operators use this skill to set up local daily, weekly, and monthly backups, create snapshots before changes, clean expired backups, and restore from trusted backup archives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can schedule persistent cron jobs that run backups and cleanup without further prompts.

Mitigation: Review cron setup scripts before running them, and avoid setup-cron-auto.sh unless unattended recurring backups and cleanup are intended.

Risk: Backup scripts can collect sensitive OpenClaw configuration and identity data into local archives.

Mitigation: Store generated archives with restricted permissions, keep them local or in trusted storage, and review backup targets before execution.

Risk: Cleanup and restore workflows can delete backups or overwrite live OpenClaw files.

Mitigation: Follow the documented confirmation and retention practices, restore only from trusted archives, and keep a current-state backup before restoring.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/reaperchen/skills/backup-manager-pro)
- [Backup strategies](artifact/backup-strategies.md)
- [Backup scripts reference](artifact/backup-scripts.md)
- [Recovery guide](artifact/recovery-guide.md)
- [Memory template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline bash commands and shell script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operates locally on OpenClaw backup paths and cron configuration.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
