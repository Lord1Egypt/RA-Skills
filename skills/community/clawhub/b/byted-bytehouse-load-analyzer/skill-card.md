## Description: <br>
ByteHouse cluster load analysis and performance monitoring helper for resource usage, query throughput, table load, and performance bottleneck identification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database operators use this skill to analyze ByteHouse cluster load through the ByteHouse MCP server and produce resource, query, table-load, bottleneck, and recommendation reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ByteHouse credentials are required to run the analyzer and may be exposed through shared shells or logs. <br>
Mitigation: Use a least-privilege ByteHouse account and avoid entering or pasting credentials in shared terminals, logs, or tickets. <br>
Risk: Generated load reports can contain sensitive operational details about databases, tables, queries, and capacity. <br>
Mitigation: Review and redact reports before committing them, publishing them, or attaching them to broad support bundles. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/byted-bytehouse-load-analyzer) <br>
- [Volcengine ByteHouse MCP server dependency](https://github.com/volcengine/mcp-server@main#subdirectory=server/mcp_server_bytehouse) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON files, shell commands, guidance] <br>
**Output Format:** [Console text and structured JSON report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes timestamped load analysis reports under the skill output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
