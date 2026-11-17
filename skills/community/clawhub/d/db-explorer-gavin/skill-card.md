## Description:

Connect to and explore databases (PostgreSQL, MySQL, SQLite, MongoDB, Redis). Run queries, inspect schemas, export data. Use when user wants to query a database, explore schema, check data, export results, or debug database issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect database schemas, run diagnostic queries, export data, and troubleshoot PostgreSQL, MySQL, SQLite, MongoDB, and Redis systems from terminal-based tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles database connection details and can expose sensitive data.

Mitigation: Use least-privileged, read-only credentials by default and avoid putting real passwords in command-line arguments.

Risk: Suggested restore, import, migration, or write commands could change production data.

Mitigation: Approve the exact command and target before execution, and use transaction or dry-run checks where the database supports them.

Risk: Exports and backups can create sensitive local files.

Mitigation: Write outputs only to private, access-controlled paths and clean them up when no longer needed.

Risk: Broad Redis key scans such as `KEYS *` can be unsafe on production-sized datasets.

Mitigation: Prefer scoped patterns or incremental scan commands before querying large keyspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lrg913427-dot/skills/db-explorer-gavin)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash and SQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include database CLI commands, query examples, export commands, and safety prompts for user review.]

## Skill Version(s):

2.5.2 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
