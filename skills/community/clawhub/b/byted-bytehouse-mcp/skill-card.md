## Description: <br>
Helps an agent start and use a local ByteHouse MCP Server to connect to ByteHouse, query databases, interact through MCP tools, and generate data asset catalog and lineage analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to configure ByteHouse credentials, start or manage the ByteHouse MCP server, list databases and tables, run ByteHouse queries, and create data catalog or lineage outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches ByteHouse MCP server code from a moving branch at runtime. <br>
Mitigation: Review and pin the upstream server source before use, or install only from a trusted reviewed revision. <br>
Risk: The skill uses ByteHouse credentials and can expose database-changing DML/DDL tools. <br>
Mitigation: Use a least-privilege or read-only ByteHouse account unless write operations are explicitly required. <br>
Risk: Generated schema, catalog, lineage, and log files may contain sensitive database metadata. <br>
Mitigation: Store generated outputs and logs in protected locations and remove them when no longer needed. <br>
Risk: The background MCP service can remain active after the agent workflow finishes. <br>
Mitigation: Check service status and stop the MCP service when the task is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/byted-bytehouse-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/volcengine-skills) <br>
- [Volcengine MCP server runtime source referenced by the skill](https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_bytehouse) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python examples, and JSON-oriented analysis outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start a local background MCP service and may create logs, PID files, and schema, catalog, or lineage JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
