## Description:

Connect to and explore databases (PostgreSQL, MySQL, SQLite, MongoDB, Redis), run queries, inspect schemas, export data, and debug database issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect database schemas, run read-oriented diagnostic queries, export selected data, and plan controlled database maintenance workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database credentials and connection strings can expose sensitive access if placed in command arguments, shell history, logs, or shared transcripts.

Mitigation: Use protected credential mechanisms such as environment variables or secret stores, avoid echoing passwords, and redact connection strings before sharing output.

Risk: Export, restore, import, migration, and write operations can expose or alter sensitive database records.

Mitigation: Require explicit user confirmation, show the exact command before execution, prefer read-only access, write exports to private permission-restricted paths, and clean up generated files after use.

Risk: Unbounded or poorly targeted queries can affect database performance, especially on production systems.

Mitigation: Default to limited result sets, avoid production targets unless intended, and use focused diagnostic queries for schema, count, and health checks.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command and query examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include database CLI commands, SQL or database-shell queries, schema summaries, export guidance, backup and restore steps, and confirmation prompts for sensitive operations.]

## Skill Version(s):

2.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
