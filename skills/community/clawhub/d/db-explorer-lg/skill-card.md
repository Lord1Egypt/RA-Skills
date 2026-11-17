## Description:

Connect to and explore databases including PostgreSQL, MySQL, SQLite, MongoDB, and Redis, with guidance for querying, schema inspection, diagnostics, exports, backups, and restores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and support engineers use this skill to inspect database schemas, run read-oriented diagnostic queries, export data, and prepare database maintenance commands with explicit safeguards for writes and restores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may receive database credentials and produce commands that access sensitive data.

Mitigation: Use least-privilege or read-only database accounts, prefer environment variables or secret stores, and avoid placing passwords directly in commands.

Risk: Restore, import, migration, and full export workflows can overwrite data, expose large datasets, or affect production systems.

Mitigation: Require explicit user confirmation, verify the target database, preview commands before execution, and test against non-production data where possible.

Risk: Broad scans such as Redis KEYS or unrestricted exports can create performance and availability issues.

Mitigation: Use bounded queries, limits, pagination, or safer scan patterns, and avoid production-wide scans unless the user explicitly approves them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lrg913427-dot/skills/db-explorer-lg)
- [ClawHub publisher profile](https://clawhub.ai/user/lrg913427-dot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline SQL and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include database CLI commands, SQL snippets, export paths, schema summaries, and safety prompts for destructive operations.]

## Skill Version(s):

2.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
