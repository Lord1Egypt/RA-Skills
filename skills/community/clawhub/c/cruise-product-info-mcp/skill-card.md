## Description:

cruise-product-info MCP Server retrieves detailed information about specific cruise products, including features and services that support decision-making.

This skill is ready for commercial/non-commercial use.

## Publisher:

[309441738](https://clawhub.ai/user/309441738)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to connect to a remote MCP service that provides cruise product details for product comparison and decision-making.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a remote MCP service at the disclosed olavacations.com endpoint.

Mitigation: Confirm the endpoint is acceptable for the intended environment before installation or use.

Risk: The reviewed documentation is in Chinese.

Mitigation: Confirm that Chinese-language documentation is sufficient for operators and reviewers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/309441738/skills/cruise-product-info-mcp)
- [Publisher profile](https://clawhub.ai/user/309441738)
- [Remote MCP endpoint](https://cruise-mcp.olavacations.com/api/gw/mcp/478d82fd-8ff7-46e2-9cda-7576fb74ed83)
- [MCP server schema](https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Text and configuration metadata returned through a remote MCP server]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a disclosed remote streamable-http MCP endpoint; no local execution, credential handling, persistence, or destructive behavior was identified in the reviewed artifacts.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
