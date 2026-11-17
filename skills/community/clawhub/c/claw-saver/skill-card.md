## Description:

Back up the full OpenClaw environment (~/.openclaw) to a Git repository. Supports scheduled backups, interactive restore, and Git LFS for large model files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jixsonwang](https://clawhub.ai/user/jixsonwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to back up a full OpenClaw home directory to a configured Git repository, schedule recurring backups, inspect backup status, and restore from recent backup commits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The backup repository can contain a near-complete copy of the OpenClaw home directory, including credentials, identity keys, tokens, memory, and knowledge data.

Mitigation: Use a private repository, a narrowly scoped or expiring token, and consider encrypting the backup before it enters Git history.

Risk: Scheduled backups can upload data unattended and can expose the backup token through local cron or Git configuration.

Mitigation: Enable cron only after accepting unattended uploads, and periodically review local crontab and Git remote configuration for token exposure.

Risk: Generated RESTORE.md exclusion claims may be unreliable for sensitive-data exposure.

Mitigation: Inspect repository contents and exclusions directly before relying on RESTORE.md to describe what was or was not backed up.

Risk: Restore operations can overwrite the current OpenClaw directory with files from a selected backup commit.

Mitigation: Restore only from a trusted repository and verified commit, and preserve current local data before confirming the restore.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jixsonwang/skills/claw-saver)
- [Skill homepage](https://clawhub.ai/skills/claw-saver)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Markdown, Configuration]

**Output Format:** [CLI output, Git commits and backup files, and RESTORE.md Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires git, git-lfs, a configured backup repository, and OPENCLAW_BACKUP_GIT_TOKEN.]

## Skill Version(s):

1.6.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
