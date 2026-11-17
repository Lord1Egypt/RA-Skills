## Description:

Inspect ClickHouse databases, review schemas, and run SQL analytics queries via the ClickHouse HTTP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and analytics engineers use this skill to discover ClickHouse schemas, inspect tables, and run read-only SQL analytics queries from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses ClawLink to store ClickHouse connection details and mediate queries and results.

Mitigation: Review ClawLink credential handling and revocation processes before installation.

Risk: Database queries can expose sensitive data or consume excessive ClickHouse resources if account permissions are broad.

Mitigation: Use a dedicated ClickHouse account with server-enforced read-only permissions, minimal database and table access, and query or resource limits.

Risk: Large result sets or expensive queries can affect performance.

Mitigation: Explore schemas first, keep queries targeted with WHERE clauses and LIMIT, and require user confirmation for large result sets or expensive queries.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/clickhouse-analytics)
- [ClickHouse Documentation](https://clickhouse.com/docs)
- [ClickHouse SQL Reference](https://clickhouse.com/docs/en/sql-reference/)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=clickhouse-analytics)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown with inline bash and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guide schema discovery, connection checks, and read-only query execution through ClawLink tools.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
