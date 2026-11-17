## Description:

Local-first agent storage — SQLite database, virtual filesystem, and memory in one .db file. Use when persisting agent state, querying CSV/JSONL/logs with SQL, or using fs_read/fs_write via the agt0 CLI or Node API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuhao6741](https://clawhub.ai/user/liuhao6741)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use agt0 to persist local agent state, store files and memory in SQLite, and query CSV, JSONL, logs, and virtual filesystem content with SQL or the agt0 CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global npm CLI installation can alter the user's local environment or install an unexpected package version.

Mitigation: Pin or verify the @seekcontext/agt0 package version before installation and avoid elevated privileges.

Risk: Deletion commands such as rm, delete, and --yes can remove stored local data.

Mitigation: Require explicit confirmation before running destructive commands and keep backups of important .db files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuhao6741/skills/agt0)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown guidance with shell and SQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local CLI commands and SQL examples; deletion examples require user confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
