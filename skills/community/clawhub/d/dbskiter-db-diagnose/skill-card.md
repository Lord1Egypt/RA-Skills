## Description:

数据库诊断与优化 helps agents run dbskiter diagnostics for SQL issues, slow queries, index recommendations, performance snapshots, locks, and bottleneck analysis across MySQL, Oracle, and PostgreSQL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[magicczc](https://clawhub.ai/user/magicczc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to select dbskiter diagnostic commands, inspect slow queries and locks, collect performance snapshots, identify bottlenecks, and obtain SQL or index optimization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger database inspections too broadly.

Mitigation: Require explicit database targets and operator approval before running diagnostics against real databases.

Risk: Command templates include database names and SQL values that could be unsafe if interpolated into a shell command.

Mitigation: Use read-only database credentials and pass database names and SQL as structured arguments through a trusted runner.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/magicczc/skills/dbskiter-db-diagnose)
- [Publisher profile](https://clawhub.ai/user/magicczc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include database diagnostic summaries, ranked findings, command suggestions, and optimization recommendations.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
