## Description:

Query, optimize, and administer ClickHouse OLAP databases with schema design, performance tuning, and data ingestion patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, data engineers, and analytics engineers use this skill to work with ClickHouse OLAP databases for log analysis, time-series analytics, real-time dashboards, schema design, ingestion planning, query optimization, and cluster administration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist ClickHouse connection profiles, schemas, query patterns, and workload notes under ~/clickhouse/.

Mitigation: Confirm what should be saved before use, avoid storing sensitive database details unless necessary, and review local memory files before sharing or deployment.

Risk: Database passwords may be stored in plain text if a user provides them for the local ClickHouse memory files.

Mitigation: Use environment variables, clickhouse-client profiles, or a secret manager instead of saving real passwords in ~/clickhouse/.

Risk: Generated SQL, ingestion commands, or administration commands can affect database performance, data retention, or running workloads.

Mitigation: Review proposed queries and commands before execution, prefer least-privileged database accounts, test changes on non-production data when possible, and use HTTPS for remote ClickHouse HTTP access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/clickhouse)
- [ClickHouse Skill Homepage](https://clawic.com/skills/clickhouse)
- [Setup and Connection](artifact/setup.md)
- [Memory Template](artifact/memory-template.md)
- [Query Patterns](artifact/queries.md)
- [Performance Tuning](artifact/performance.md)
- [Data Ingestion](artifact/ingestion.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with SQL, shell command, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose ClickHouse queries, schema definitions, ingestion commands, configuration steps, and local memory updates under ~/clickhouse/.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
