## Description:

Access Ahrefs SEO data through Model Context Protocol (MCP) for SEO analysis, keyword research, backlink analysis, site audits, and competitive intelligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonathan-sokol](https://clawhub.ai/user/jonathan-sokol)

### License/Terms of Use:


## Use Case:

SEO practitioners, marketers, developers, and analysts use this skill to connect an AI client to Ahrefs MCP and request domain, keyword, backlink, rank tracking, site audit, and competitor analysis data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting an AI client to Ahrefs MCP creates an authorized MCP-scoped API key for the account.

Mitigation: Review requested permissions during authorization, use trusted AI clients only, and revoke the MCP API key when access is no longer needed.

Risk: Large or repeated Ahrefs queries can consume monthly API units.

Mitigation: Set monthly API unit limits where possible, monitor account usage, and confirm query scope before running large requests.

## Reference(s):

- [Ahrefs MCP setup guide](references/setup.md)
- [Ahrefs MCP capabilities reference](references/capabilities.md)
- [Ahrefs MCP workflow patterns](references/workflows.md)
- [Ahrefs Claude Desktop and Web MCP guide](https://docs.ahrefs.com/docs/mcp/reference/claude-desktop-web)
- [Ahrefs Claude Mobile MCP guide](https://docs.ahrefs.com/docs/mcp/reference/claude-mobile)
- [Ahrefs ChatGPT Web MCP guide](https://docs.ahrefs.com/docs/mcp/reference/chatgpt-web)
- [Ahrefs API limits and consumption](https://docs.ahrefs.com/docs/api/reference/limits-consumption)
- [Ahrefs MCP server repository](https://github.com/ahrefs/ahrefs-mcp-server)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with natural-language MCP queries, setup steps, tables, and SEO recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Ahrefs account authorization steps, MCP connection URLs, and recommendations based on returned SEO data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
