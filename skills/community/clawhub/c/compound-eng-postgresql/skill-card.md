## Description:

PostgreSQL schema design, query optimization, indexing, and administration. Use when working with PostgreSQL, JSONB, partitioning, RLS, CTEs, window functions, or EXPLAIN ANALYZE.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill for PostgreSQL schema changes, query and index design, performance analysis, and operational patterns involving migrations, concurrency, security, and administration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan questions whether some evaluation and diagnostic commands match the skill's stated PostgreSQL purpose.

Mitigation: Review each command and its expected effects before running it; the scan guidance notes that one referenced script could not be resolved and its behavior was not determined.

Risk: Operational guidance may put database data at risk or disrupt active work.

Mitigation: Use disposable data for writes, confirm authorization and rollback scope before executing queries, and check lock duration and transaction boundaries.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/iliaal/skills/compound-eng-postgresql)
- [Concurrency Patterns](references/concurrency-patterns.md)
- [Full-Text Search](references/full-text-search.md)
- [Operations](references/operations.md)
- [Performance Patterns](references/performance-patterns.md)
- [Query and Index Patterns](references/query-and-index-patterns.md)
- [Schema and Migrations](references/schema-and-migrations.md)
- [Security and Operations](references/security-and-operations.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with SQL and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Context-specific PostgreSQL recommendations and verification steps.]

## Skill Version(s):

5.1.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
