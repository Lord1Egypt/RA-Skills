## Description:

Set up scheduled automated backups with version tracking, cleanup, and backup strategies for directories, configuration files, code repositories, or user data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zfanmy](https://clawhub.ai/user/zfanmy)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to create one-time, scheduled, version-aware, and retention-managed backups using shell scripts and cron.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell and cron construction can turn user-supplied paths or version commands into persistent command execution.

Mitigation: Use only trusted, simple paths and version sources; review generated cron entries before installation; avoid scheduling jobs until unsafe version checks and unquoted cron construction are fixed.

Risk: Running backup or cleanup jobs with elevated privileges can increase the impact of path or command-handling mistakes.

Mitigation: Run scripts as a least-privileged user and do not run them as root.

Risk: Cleanup behavior permanently deletes matching backup archives according to retention settings.

Mitigation: Confirm the backup directory and retention values before cleanup, and list existing backups before deleting old archives.

## Reference(s):

- [Cron Backup on ClawHub](https://clawhub.ai/zfanmy/skills/cron-backup)
- [zfanmy Publisher Profile](https://clawhub.ai/user/zfanmy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and cron configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose backup, cleanup, listing, and cron setup commands for local shell execution.]

## Skill Version(s):

0.3.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
