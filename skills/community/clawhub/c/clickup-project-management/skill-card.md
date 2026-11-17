## Description:

Manage ClickUp via natural language using the taazkareem.com remote MCP server, with a license key required for full tool access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taazkareem](https://clawhub.ai/user/taazkareem)

### License/Terms of Use:

MIT

## Use Case:

Developers and ClickUp workspace users use this skill to configure agent access to ClickUp task, document, chat, and time-tracking workflows through a remote MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClickUp OAuth credentials and workspace contents are sent to a third-party remote MCP server.

Mitigation: Install only after trusting the server operator, use narrow ClickUp scopes, and avoid high-privilege admin accounts.

Risk: Persistent mcporter configuration changes can alter which ClickUp tools the agent may call.

Mitigation: Manually review and approve mcporter configuration changes, especially persona or tool-filtering headers.

## Reference(s):

- [ClickUp MCP Server](https://github.com/taazkareem/clickup-mcp-server)
- [ClickUp Remote MCP Endpoint](https://clickup-mcp.taazkareem.com/mcp)
- [ClickUp API v2](https://api.clickup.com/api/v2/*)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides mcporter setup, authentication, and tool-filtering command patterns; agent actions depend on user-provided license and OAuth credentials.]

## Skill Version(s):

1.0.10 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
