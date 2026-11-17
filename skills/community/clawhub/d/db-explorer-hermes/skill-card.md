## Description:

Connect to and explore databases (PostgreSQL, MySQL, SQLite, MongoDB, Redis). Run queries, inspect schemas, export data. Use when user wants to query a database, explore schema, check data, export results, or debug database issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect database schemas, run diagnostic queries, export selected data, and troubleshoot PostgreSQL, MySQL, SQLite, MongoDB, and Redis systems from the terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database backup, restore, migration, and export commands can affect sensitive or production data if run with broad privileges or unclear scope.

Mitigation: Use read-only, least-privilege credentials by default; require explicit approval for exports, backups, restores, migrations, and any write operation; confirm scope and rollback plans before production use.

Risk: Database credentials can be exposed through command history, process listings, logs, or exported files.

Mitigation: Prefer environment variables or secure prompts for credentials, avoid passwords in command lines, and write exports or backups only to protected output locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lrg913427-dot/skills/db-explorer-hermes)
- [ClawHub publisher profile](https://clawhub.ai/user/lrg913427-dot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline SQL, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include database queries, export commands, backup and restore commands, migration helpers, and safety checks.]

## Skill Version(s):

2.4.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
