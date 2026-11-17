## Description:

Connect to and explore databases (PostgreSQL, MySQL, SQLite, MongoDB, Redis). Run queries, inspect schemas, export data. Use when user wants to query a database, explore schema, check data, export results, or debug database issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect to supported databases, inspect schemas and data, run bounded queries, export results, and diagnose database health or performance issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database credentials or connection strings can grant broad access to sensitive data.

Mitigation: Use read-only, least-privilege credentials by default and avoid production databases unless the user explicitly intends production access.

Risk: Export, backup, restore, import, or migration commands can create sensitive local files or alter data.

Mitigation: Review each command before execution, require explicit confirmation for write or restore operations, and clean up local files that may contain sensitive data.

Risk: Broad queries or Redis key enumeration can expose more data than intended.

Mitigation: Limit result sets, scope commands to the requested database or keys, and summarize samples before expanding access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lrg913427-dot/skills/db-explorer-tool)
- [Publisher profile](https://clawhub.ai/user/lrg913427-dot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and database query snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include database queries, export or backup commands, and safety confirmation prompts.]

## Skill Version(s):

2.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
