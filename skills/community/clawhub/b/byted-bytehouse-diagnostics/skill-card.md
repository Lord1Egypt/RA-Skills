## Description:

Runs ByteHouse cluster health diagnostics, including node status, replica and partition checks, system table access checks, and recent query statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to inspect ByteHouse cluster health, diagnose node and replica issues, review partition and system table status, and summarize recent query behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs mutable remote code for the ByteHouse MCP server.

Mitigation: Prefer a version pinned to an audited MCP server commit and exact dependencies before production use.

Risk: The skill passes the full local environment to the MCP server process, which can expose unrelated secrets.

Mitigation: Run in an isolated environment with only required ByteHouse variables and remove unrelated secrets before execution.

Risk: Generated reports can contain sensitive operational database information.

Mitigation: Treat diagnostic reports as sensitive operational data and restrict storage, sharing, and retention.

Risk: Database diagnostics require live ByteHouse access.

Mitigation: Use a dedicated least-privilege ByteHouse account for health checks and query-log inspection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-bytehouse-diagnostics)
- [Volcengine ByteHouse MCP server reference](https://github.com/volcengine/mcp-server@main#subdirectory=server/mcp_server_bytehouse)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON diagnostic reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes timestamped ByteHouse diagnostic JSON reports under a local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
