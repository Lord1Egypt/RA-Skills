## Description:

Provides ClickHouse schema, query, and ingestion review guidance using 28 best-practice rules for table design, JOINs, materialized views, mutations, partitioning, data types, and batch writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaniu001](https://clawhub.ai/user/shaniu001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to review ClickHouse CREATE TABLE, ALTER TABLE, SELECT, JOIN, aggregation, ingestion, mutation, and configuration decisions. It produces prioritized findings and recommendations grounded in the bundled rule files and ClickHouse documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated database changes could include destructive or expensive ClickHouse operations such as DROP PARTITION, DELETE, TTL, ALTER, or table migration.

Mitigation: Review and test generated SQL against representative data before execution; require operator approval for destructive or migration steps.

Risk: Responses may lean Chinese unless the host agent or user asks otherwise, which can reduce review clarity for teams expecting another language.

Mitigation: Ask for the preferred review language before production use and request English output where required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shaniu001/skills/clickhouse-best-practices)
- [ClickHouse Best Practices](https://clickhouse.com/docs/best-practices)
- [Choosing a Primary Key](https://clickhouse.com/docs/best-practices/choosing-a-primary-key)
- [Choosing a Partitioning Key](https://clickhouse.com/docs/best-practices/choosing-a-partitioning-key)
- [Select Data Types](https://clickhouse.com/docs/best-practices/select-data-types)
- [Minimize and Optimize JOINs](https://clickhouse.com/docs/best-practices/minimize-optimize-joins)
- [Selecting an Insert Strategy](https://clickhouse.com/docs/best-practices/selecting-an-insert-strategy)
- [Avoid Mutations](https://clickhouse.com/docs/best-practices/avoid-mutations)
- [Use Data Skipping Indices Where Appropriate](https://clickhouse.com/docs/best-practices/use-data-skipping-indices-where-appropriate)
- [Using Materialized Views](https://clickhouse.com/docs/best-practices/using-materialized-views)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with SQL, Python, shell, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review output follows a structured checklist of checked rules, findings, compliant items, and prioritized recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
