## Description:

Connect to and explore databases (PostgreSQL, MySQL, SQLite, MongoDB, Redis). Run queries, inspect schemas, export data. Use when user wants to query a database, explore schema, check data, export results, or debug database issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect to relational, document, and key-value databases, inspect schemas, run diagnostic queries, export results, and troubleshoot database issues from terminal tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples may place database passwords in command lines or connection strings where they can be exposed through shell history or process listings.

Mitigation: Use environment variables, prompt-based credential entry, or secret-managed connection profiles, and avoid echoing or logging credentials.

Risk: Restore, import, migration, or write commands can overwrite or corrupt data if run against the wrong database or without preparation.

Mitigation: Use least-privilege read-only accounts by default, create backups first, show the exact command, and require explicit confirmation before execution.

Risk: Unbounded Redis key listing with KEYS "*" can degrade production Redis performance.

Mitigation: Use bounded SCAN-style inspection with limits and sampling instead of full keyspace scans.

Risk: Schema exploration and exports can expose sensitive production data.

Mitigation: Limit query results, export only the minimum necessary fields, and route outputs to approved secure locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lrg913427-dot/skills/db-explorer-lrg913427)
- [ClawHub publisher profile](https://clawhub.ai/user/lrg913427-dot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with SQL and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should favor read-only inspection, bounded query results, and explicit confirmation before write, restore, import, or migration operations.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
