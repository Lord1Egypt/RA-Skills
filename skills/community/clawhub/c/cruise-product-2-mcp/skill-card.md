## Description:

A cruise-product MCP server that helps users discover cruise offerings and filter options across multiple dimensions to find suitable trips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[309441738](https://clawhub.ai/user/309441738)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this hosted MCP server to search cruise products and narrow results by multiple travel-preference filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cruise-search queries may be sent to the listed remote service.

Mitigation: Review data-sharing expectations before installing or using the hosted MCP endpoint.

Risk: The package description and README are Chinese-only.

Mitigation: Provide translation or bilingual review for non-Chinese-speaking users before deployment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/309441738/skills/cruise-product-2-mcp)
- [Remote MCP endpoint](https://cruise-mcp.olavacations.com/api/gw/mcp/3ae0fa3d-2c56-4d01-be01-14ee8463cf04)
- [Model Context Protocol server schema](https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json)

## Skill Output:

**Output Type(s):** [text, API Calls, guidance]

**Output Format:** [Text or structured MCP tool responses from a hosted remote service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries are sent to the listed remote MCP service.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
