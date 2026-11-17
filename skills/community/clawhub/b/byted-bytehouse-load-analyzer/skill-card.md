## Description:

Analyzes ByteHouse cluster load, query throughput, table activity, resource usage, and performance bottlenecks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to inspect ByteHouse cluster load, query activity, table hot spots, and bottleneck indicators. It supports operational performance review and capacity-planning workflows for ByteHouse environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads mutable remote code at runtime with access to the process environment.

Mitigation: Pin the MCP server dependency to an immutable, reviewed source before deployment and run it only in a ByteHouse-scoped environment.

Risk: Generated reports may contain sensitive table names, operational metadata, and active SQL text.

Mitigation: Use low-privilege ByteHouse credentials, restrict report storage access, and treat generated output as sensitive operational data.

Risk: The skill depends on ByteHouse credentials and an MCP server that is configured outside this artifact.

Mitigation: Validate the dependent ByteHouse MCP server configuration and credential scope before running analysis.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/volcengine-skills/skills/byted-bytehouse-load-analyzer)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Files, Shell commands, Guidance]

**Output Format:** [JSON report files with console progress output and operational recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports may include table names, operational metadata, and active SQL text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
