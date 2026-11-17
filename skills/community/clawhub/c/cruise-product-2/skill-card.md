## Description:

Helps agents find cruise products by filtering product lists, retrieving product details, and searching by keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[309441738](https://clawhub.ai/user/309441738)

### License/Terms of Use:

MIT

## Use Case:

External users and travel-support agents use this MCP skill to browse cruise offerings, narrow choices by trip criteria, look up product details, and search products by keyword.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published instructions include a generic httpbin POST endpoint that is unrelated to the cruise MCP gateway.

Mitigation: Do not send real travel details, credentials, payment information, or conversation history to the placeholder endpoint; use the documented Cruise MCP gateway only after review.

Risk: The security verdict is suspicious because the skill documentation mixes the intended MCP endpoint with a test endpoint.

Mitigation: Require publisher cleanup and documentation of transmitted and logged data before installing in workflows that handle user or business information.

## Reference(s):

- [MCP Server 接入](references/mcp.md)
- [CruiseSkillBridge](https://cruiseskillbridge.com)
- [ClawHub Skill Page](https://clawhub.ai/309441738/skills/cruise-product-2)
- [MCP server schema](https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json)
- [Cruise MCP gateway](https://cruise-mcp.olavacations.com/api/gw/mcp/3ae0fa3d-2c56-4d01-be01-14ee8463cf04)

## Skill Output:

**Output Type(s):** [text, markdown, API Calls, configuration, guidance]

**Output Format:** [Markdown guidance with MCP tool calls and JSON request or response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include cruise product lists, product-detail lookups, and keyword search results from the configured MCP endpoint.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter and server.json report 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
