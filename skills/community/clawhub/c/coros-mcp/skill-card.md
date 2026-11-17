## Description:

Install or refresh the COROS MCP connection inside OpenClaw through the global mcp.coros.com gateway, automatically pinning the connection to the CN, EU, or US cluster selected by the gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coros-open](https://clawhub.ai/user/coros-open)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and COROS users use this skill to install or refresh an OpenClaw MCP connection, complete browser-based COROS login, list current MCP tools, inspect tool schemas, and call selected tools through the COROS gateway.

### Deployment Geography for Use:

Global, routed by the COROS gateway to CN, EU, or US clusters.

## Known Risks and Mitigations:

Risk: The helper handles COROS account credentials and bearer tokens, and local OpenClaw MCP config or ~/.coros-mcp-skill-gateway state may contain reusable tokens.

Mitigation: Review before installing, protect local config and cache files, and clear saved state with logout when access should be removed.

Risk: Custom issuer or MCP URL values can redirect authentication or MCP requests to an untrusted endpoint.

Mitigation: Use the default COROS gateway unless the endpoint is fully trusted.

Risk: The legacy password flow asks for COROS credentials in the terminal.

Mitigation: Use the browser/device login flow and avoid --legacy password login unless explicitly required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coros-open/skills/coros-mcp)
- [COROS MCP gateway](https://mcp.coros.com)
- [COROS MCP CN cluster](https://mcpcn.coros.com)
- [COROS MCP EU cluster](https://mcpeu.coros.com)
- [COROS MCP US cluster](https://mcpus.coros.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON snippets, and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print browser login URLs, JSON tool catalogs, tool descriptions, tool-call results, and OpenClaw MCP setup status.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
