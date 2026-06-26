## Description: <br>
Analyzes ByteHouse slow queries, query performance statistics, execution-plan signals, historical trends, and optimization suggestions for database performance tuning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database engineers use this skill to inspect recent ByteHouse query_log activity, identify slow queries, summarize query performance, and generate optimization recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill launches a remote MCP server dependency from a branch reference while passing the local environment, including ByteHouse credentials. <br>
Mitigation: Install only from a trusted source, pin the dependency to a reviewed commit, and run it in a clean environment containing only required BYTEHOUSE_* variables. <br>
Risk: Database access used for slow-query analysis can expose query text, operational metrics, and other sensitive information in generated JSON reports. <br>
Mitigation: Use a read-only, least-privileged ByteHouse account and handle generated reports as sensitive data. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/volcengine-skills/byted-bytehouse-slow-query) <br>
- [volcengine-skills publisher profile](https://clawhub.ai/user/volcengine-skills) <br>
- [ByteHouse MCP server dependency](https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_bytehouse) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Console progress text plus timestamped JSON analysis reports containing slow-query data, query statistics, and optimization suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports under the analyzer script output directory and may include sensitive query text or operational database metrics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
