## Description:

Tracks file-changing edit batches by creating path-scoped local Git recovery points before and after changes, then reports recent records and rollback guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songxf1024](https://clawhub.ai/user/songxf1024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill when a task will create, edit, move, delete, or generate files and the target paths are known. It creates local Git recovery points for those paths, records post-change results when needed, and provides reports plus rollback commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically mutates local Git repositories and may create durable local commits without a separate user confirmation step.

Mitigation: Review the declared target paths before running the workflow, and use it only when local Git recovery commits are desired.

Risk: Non-ignored generated files, binaries, or secret-containing files inside declared target paths may be captured in local snapshots.

Mitigation: Keep target paths narrow and confirm .gitignore and guarded-edit.ignore exclude generated output and sensitive files before snapshotting.

Risk: The helper may initialize Git, set repository-local Git identity, bypass commit hooks, and leave .git/.guarded-edit session records.

Mitigation: Run it in repositories where local history changes are acceptable, and inspect session records and rollback guidance after use.

## Reference(s):

- [File Change Tracker on ClawHub](https://clawhub.ai/songxf1024/skills/file-change-tracker)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires git plus bash or sh according to ClawHub metadata.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
