## Description:

根据条件筛选邮轮产品列表，支持多种过滤条件，快速获取您想要的邮轮产品。

This skill is ready for commercial/non-commercial use.

## Publisher:

[309441738](https://clawhub.ai/user/309441738)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this MCP skill to search and filter cruise products by criteria such as brand, departure city, price range, destination, duration, cruise line, and travel date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cruise search criteria are sent to an external CruiseSkillBridge/olavacations remote endpoint.

Mitigation: Confirm the remote endpoint is acceptable for the deployment context before installing or invoking the skill.

Risk: Users may include sensitive personal, payment, or secret information in search inputs.

Mitigation: Limit inputs to cruise search criteria and avoid secrets, payment details, and sensitive personal information.

## Reference(s):

- [MCP Server 接入](references/mcp.md)
- [ClawHub skill page](https://clawhub.ai/309441738/skills/cruise-product-list)
- [CruiseSkillBridge](https://cruiseskillbridge.com)
- [Remote MCP endpoint](https://cruise-mcp.olavacations.com/api/gw/mcp/1d6f83ba-00e5-4eeb-b6aa-cb5861a28fe0)
- [MCP server schema](https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or text responses from a remote MCP tool call]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the remote CruiseSkillBridge/olavacations MCP endpoint and the user's cruise search criteria.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
