## Description:

Backup Rotator helps agents create timestamped backups, apply grandfather-father-son retention policies, verify SHA256 checksums, and schedule backup rotation via cron.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericlooi504](https://clawhub.ai/user/ericlooi504)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to ask an agent for local backup creation, retention rotation, checksum verification, and cron-ready command or configuration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic rotation can permanently delete backup files, especially when cron runs unattended.

Mitigation: Run dry-run rotation first, use dedicated backup destinations, review retention counts, and schedule cron only after confirming the deletion plan.

Risk: Checksum output may create false confidence because verification is not proof that backups are complete or restorable.

Mitigation: Treat SHA256 checks as basic corruption checks and periodically test restore workflows from retained backups.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ericlooi504/skills/backup-rotator)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide file creation, backup rotation, checksum verification, dry runs, and cron scheduling for local filesystem backups.]

## Skill Version(s):

1.0.0 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
