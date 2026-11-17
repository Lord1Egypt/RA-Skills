## Description:

Better Skill Creator helps agents create, modify, package, back up, compare, and roll back OpenClaw skills with proposal and validation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzzanezhou0829](https://clawhub.ai/user/zzzanezhou0829)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agent operators use this skill to scaffold new skills, package releases, manage skill versions, review changes, and roll back to previous versions when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backup, rollback, and installer scripts can overwrite or delete broad local data.

Mitigation: Use only in a disposable or well-backed-up skill workspace, inspect target paths before confirming deletion or rollback, and avoid elevated privileges.

Risk: Rollback behavior depends on local backup metadata and restored file contents.

Mitigation: Do not roll back from untrusted backup metadata, and preview differences before confirming a restore.

Risk: Backups may copy symlinks or secrets from skill directories.

Mitigation: Remove symlinks and secrets from skill directories before backup.

## Reference(s):

- [Configuration Reference](references/config.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, overwrite, or delete local skill directories and backup records when scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
