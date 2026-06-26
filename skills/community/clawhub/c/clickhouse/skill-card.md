## Description: <br>
Query, optimize, and administer ClickHouse OLAP databases with schema design, performance tuning, and data ingestion patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, data engineers, and analytics teams use this skill to work with ClickHouse databases for OLAP analytics, log analysis, time-series data, real-time dashboards, query optimization, ingestion patterns, schema design, and cluster administration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help produce powerful database operations such as INSERT, ALTER, DROP, KILL, OPTIMIZE, TTL changes, and migrations. <br>
Mitigation: Review generated database commands before running them against production or otherwise important ClickHouse data. <br>
Risk: The skill can save database context locally under ~/clickhouse/, including connection profiles, schemas, and query patterns. <br>
Mitigation: Do not store database passwords or cloud secrets in ~/clickhouse/ or command URLs; use environment variables, ClickHouse client profiles, or a secret manager, and periodically inspect or delete retained local context. <br>


## Reference(s): <br>
- [ClawHub ClickHouse skill page](https://clawhub.ai/ivangdavila/clickhouse) <br>
- [ClickHouse skill homepage](https://clawic.com/skills/clickhouse) <br>
- [Setup guide](setup.md) <br>
- [Query patterns](queries.md) <br>
- [Performance tuning](performance.md) <br>
- [Data ingestion](ingestion.md) <br>
- [Memory template](memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose ClickHouse client commands, SQL statements, schema definitions, ingestion commands, performance checks, and local memory updates for user review.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
