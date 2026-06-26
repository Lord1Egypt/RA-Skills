## Description: <br>
Inspect ClickHouse databases, review schemas, and run SQL analytics queries via the ClickHouse HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and operators use this skill to inspect ClickHouse schemas, verify available databases and tables, and run read-only SQL analytics queries for business intelligence from an agent chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a connected ClickHouse account and may depend on sensitive credentials managed outside chat. <br>
Mitigation: Review the permissions granted to the agent environment and avoid providing secrets in chat unless the task requires them. <br>
Risk: SQL analytics queries can produce large result sets or expensive scans. <br>
Mitigation: Use schema discovery first, keep queries targeted with WHERE clauses and LIMIT, and request user confirmation for large or expensive queries. <br>


## Reference(s): <br>
- [ClickHouse Documentation](https://clickhouse.com/docs) <br>
- [ClickHouse SQL Reference](https://clickhouse.com/docs/en/sql-reference/) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/clickhouse-analytics) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and SQL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to use ClawLink ClickHouse tools for schema discovery, connection checks, and read-only query execution.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
