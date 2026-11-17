## Description:

SQL智能助手 helps agents execute SQL, rewrite and analyze queries, inspect schemas, profile data, complete SQL, and import or export database data with dbskiter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[magicczc](https://clawhub.ai/user/magicczc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and database operators use this skill to ask an agent for SQL execution, query optimization, quality analysis, data profiling, schema inspection, SQL completion, batch execution, and data import or export workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad SQL execution, imports, exports, and batch file execution against configured databases.

Mitigation: Use least-privileged or read-only database credentials by default, and require explicit user confirmation before writes, imports, exports, batch files, or production database actions.

Risk: User-provided SQL or file paths may be unsafe if passed directly through a shell command string.

Mitigation: Avoid shell-interpolated command strings; pass SQL and paths as structured arguments where possible, validate file paths, and review generated commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/magicczc/skills/dbskiter-sql-master)
- [Publisher profile](https://clawhub.ai/user/magicczc)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, SQL snippets, result summaries, and structured recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optimized SQL, SQL quality scores, schema descriptions, data profile summaries, and import/export command guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
