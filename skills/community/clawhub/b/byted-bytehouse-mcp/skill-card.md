## Description:

Starts a local ByteHouse MCP Server and helps agents connect to ByteHouse, run database queries through MCP tools, and generate database asset catalog and lineage analysis outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to configure a ByteHouse MCP connection, inspect databases and tables, run SELECT, DML, and DDL queries, and produce schema, catalog, and lineage reports for ByteHouse data assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads changing remote MCP server code at install or run time.

Mitigation: Review the referenced MCP server source and service scripts before use, and install only when that runtime dependency is acceptable.

Risk: The MCP server process can receive the full local environment, including ByteHouse credentials.

Mitigation: Run it in a clean environment containing only required BYTEHOUSE_* variables and avoid privileged shells or CI environments with broad secrets.

Risk: Database access and generated outputs can expose sensitive schema, catalog, lineage, or log metadata.

Mitigation: Use a dedicated low-privilege, preferably read-only ByteHouse account and treat generated files and logs as sensitive database metadata.

Risk: The skill can run a background service through start, stop, restart, and status scripts.

Mitigation: Review service management scripts before running them and monitor PID and log files during operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-bytehouse-mcp)
- [Volcengine ByteHouse MCP server runtime source](https://github.com/volcengine/mcp-server@main#subdirectory=server/mcp_server_bytehouse)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell and Python code examples; runtime scripts can produce JSON schema, catalog, and lineage files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ByteHouse connection environment variables and may start a background MCP server process that writes PID and log files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
