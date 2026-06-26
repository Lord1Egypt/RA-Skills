## Description: <br>
Install or refresh the COROS MCP connection inside OpenClaw through the global mcp.coros.com gateway, automatically pinning the connection to the CN, EU, or US cluster selected by the gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coros-open](https://clawhub.ai/user/coros-open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect OpenClaw to the COROS MCP gateway, complete COROS authentication, configure the saved MCP server entry, and inspect or call supported COROS MCP tools. <br>

### Deployment Geography for Use: <br>
Global, with runtime service routing through CN, EU, or US COROS MCP clusters. <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves COROS tokens locally and enables authenticated COROS MCP access through OpenClaw. <br>
Mitigation: Install only when you intend to authorize this access, prefer the browser login flow, and use the logout command to clear saved local login state when finished. <br>
Risk: Authenticated MCP tool calls can let the agent list and call COROS tools on the user's behalf. <br>
Mitigation: Review tool schemas before sensitive actions and call only the intended COROS tools. <br>
Risk: Legacy password mode increases credential-handling exposure. <br>
Mitigation: Avoid legacy password mode unless necessary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coros-open/skills/coros-mcp) <br>
- [COROS MCP gateway](https://mcp.coros.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON tool or configuration output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit browser login URLs, OpenClaw MCP configuration updates, tool schemas, and MCP tool call results.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
