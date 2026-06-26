## Description: <br>
Uses Asana through mcporter-backed remote MCP tools for tasks, projects, portfolios, goals, and team workspaces via the hosted Asana MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dam1k](https://clawhub.ai/user/dam1k) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams use this skill to search, read, create, and update Asana tasks, projects, and workspace data through a connected Asana OAuth account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connected OAuth account allows the agent to read and change Asana workspace data. <br>
Mitigation: Install only when this access is intended, confirm impactful changes before execution, and disconnect OAuth access when it is no longer needed. <br>
Risk: Task, project, due date, completion, and follower updates can affect shared work tracking. <br>
Mitigation: Review proposed changes before allowing create, update, move, complete, or follower-management actions. <br>


## Reference(s): <br>
- [Asana MCP server](https://mcp.asana.com/v2/mcp) <br>
- [ClawHub skill listing](https://clawhub.ai/dam1k/asana-remote-mcp) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/dam1k) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with tool names, parameter guidance, and operational instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected Asana MCP OAuth token; tool calls may read or modify Asana workspace data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
