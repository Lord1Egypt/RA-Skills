## Description: <br>
Manage ClickUp via natural language using the taazkareem.com remote MCP server, with a license key required for full tool access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taazkareem](https://clawhub.ai/user/taazkareem) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and ClickUp workspace users use this skill to configure an agent to manage ClickUp tasks, comments, tags, lists, folders, files, docs, chat, and time through a remote MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClickUp OAuth credentials and workspace data are transmitted to a third-party remote MCP server. <br>
Mitigation: Install only if you trust the taazkareem.com MCP operator, avoid sensitive workspaces, and revoke the ClickUp OAuth authorization when the skill is no longer used. <br>
Risk: The remote MCP server can perform broad project-management actions in ClickUp. <br>
Mitigation: Prefer read-only or no-delete tool filters and require explicit approval for destructive ClickUp actions. <br>


## Reference(s): <br>
- [ClickUp MCP Server repository](https://github.com/taazkareem/clickup-mcp-server) <br>
- [ClickUp remote MCP endpoint](https://clickup-mcp.taazkareem.com/mcp) <br>
- [ClickUp API v2](https://api.clickup.com/api/v2/*) <br>
- [ClawHub skill page](https://clawhub.ai/taazkareem/clickup-project-management) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLICKUP_MCP_LICENSE_KEY and ClickUp OAuth authentication for full tool access.] <br>

## Skill Version(s): <br>
1.0.10 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
