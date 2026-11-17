## Description:

DBA多AI协作系统用于处理架构设计、日常运维、故障排查、性能优化和数据迁移等数据库DBA工作，覆盖Oracle、MySQL、PostgreSQL、SQL Server、国产数据库以及MongoDB、Redis和ClickHouse。

This skill is ready for commercial/non-commercial use.

## Publisher:

[pc-study](https://clawhub.ai/user/pc-study)

### License/Terms of Use:

MIT-0

## Use Case:

Database administrators, developers, and operations teams use this skill to route database-related requests to specialist roles and produce coordinated DBA plans, troubleshooting guidance, optimization advice, migration guidance, inspection reports, and backup validation outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically stores database environment details, task history, and user preferences in local memory files.

Mitigation: Use the skill only where persisted DBA context is acceptable, and disable or tightly control memory behavior before sharing confidential database details.

Risk: DBA requests may include passwords, connection strings, hostnames, incident details, topology, query results, or other confidential production data.

Mitigation: Redact sensitive values before use and limit workspace access to authorized users.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured sections and optional code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or update local memory files for environment details, task history, and user preferences when memory behavior is enabled.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
