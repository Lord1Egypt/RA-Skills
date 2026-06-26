## Description: <br>
Provides ClickHouse schema, query, and ingestion review guidance using 28 documented best-practice rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaniu001](https://clawhub.ai/user/shaniu001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database engineers use this skill to review ClickHouse CREATE TABLE and ALTER TABLE statements, SELECT and JOIN queries, materialized views, partitioning, and ingestion strategies. It helps produce prioritized findings and recommendations grounded in bundled ClickHouse rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested schema, mutation, or data-deletion changes could be harmful if applied directly to production databases. <br>
Mitigation: Review each recommendation with a database owner and test changes in staging before production rollout. <br>
Risk: ClickHouse guidance can depend on workload shape, data volume, engine choice, and version-specific behavior. <br>
Mitigation: Validate recommendations against the target cluster version, representative data, and observed query or ingestion metrics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shaniu001/clickhouse-best-practices) <br>
- [ClickHouse best practices](https://clickhouse.com/docs/best-practices) <br>
- [Selecting an insert strategy](https://clickhouse.com/docs/best-practices/selecting-an-insert-strategy) <br>
- [Avoid mutations](https://clickhouse.com/docs/best-practices/avoid-mutations) <br>
- [Use data skipping indices where appropriate](https://clickhouse.com/docs/best-practices/use-data-skipping-indices-where-appropriate) <br>
- [Minimize and optimize JOINs](https://clickhouse.com/docs/best-practices/minimize-optimize-joins) <br>
- [Using materialized views](https://clickhouse.com/docs/best-practices/using-materialized-views) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown review with rule citations, findings, recommendations, and SQL or code examples where relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
