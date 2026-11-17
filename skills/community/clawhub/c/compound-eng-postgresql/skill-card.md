## Description:

PostgreSQL schema design, query optimization, indexing, and administration. Use when working with PostgreSQL, JSONB, partitioning, RLS, CTEs, window functions, or EXPLAIN ANALYZE.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to design PostgreSQL schemas, review and optimize queries and indexes, and make safer migration and administration decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security assessment flags a mismatch between the stated PostgreSQL purpose and reported evaluation commands, and says the scan is incomplete because a local path-like reference was unresolved.

Mitigation: Review the evaluation commands and resolve the flagged reference before running commands.

Risk: The server security assessment says failover advice involving pg_rewind could cause data loss if followed without safeguards.

Mitigation: Before using the failover guidance, verify the source and target, confirm pg_rewind prerequisites, and preserve a recoverable backup.

## Reference(s):

- [Concurrency patterns](artifact/references/concurrency-patterns.md)
- [Full-text search](artifact/references/full-text-search.md)
- [Operations](artifact/references/operations.md)
- [Performance patterns](artifact/references/performance-patterns.md)
- [Query and index patterns](artifact/references/query-and-index-patterns.md)
- [Schema and migrations](artifact/references/schema-and-migrations.md)
- [Security and operations](artifact/references/security-and-operations.md)
- [PostgreSQL transaction retry guidance](https://www.postgresql.org/docs/18/mvcc-serialization-failure-handling.html)
- [PostgreSQL multicolumn indexes](https://www.postgresql.org/docs/18/indexes-multicolumn.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with SQL examples and explanatory guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

5.1.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
