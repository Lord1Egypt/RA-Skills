## Description:

Connect to and explore PostgreSQL, MySQL, SQLite, MongoDB, and Redis databases to inspect schemas, run queries, export data, and debug database issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect to common databases, inspect schemas, run read-oriented diagnostic queries, export selected data, and troubleshoot database health or performance issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database exploration can expose credentials or sensitive data.

Mitigation: Use least-privilege read-only credentials, avoid placing passwords in command-line arguments, and limit query results before displaying or exporting data.

Risk: Restore, import, migration, or write-like operations can modify or overwrite database state.

Mitigation: Require explicit user confirmation before restore, import, migration, INSERT, UPDATE, DELETE, DROP, or COMMIT operations, and preview the exact command before execution.

Risk: Exports and backups can leave sensitive data in local files.

Mitigation: Store exports or backups only in protected locations and define cleanup expectations after the task is complete.

Risk: Broad database administration guidance can enable unsafe operational actions if used without review.

Mitigation: Review the skill before deployment and restrict agent access to database credentials and environments appropriate for the intended use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lrg913427-dot/skills/gavin-db-explorer)
- [Publisher Profile](https://clawhub.ai/user/lrg913427-dot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with inline shell and SQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce CSV or JSON export files when the user asks for database exports.]

## Skill Version(s):

2.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
