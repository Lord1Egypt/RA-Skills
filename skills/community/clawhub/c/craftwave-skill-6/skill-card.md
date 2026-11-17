## Description:

为公司团体或组织提供邮轮旅行方案，适合团队出行的需求，制定专属的邮轮产品。

This skill is ready for commercial/non-commercial use.

## Publisher:

[309441738](https://clawhub.ai/user/309441738)

### License/Terms of Use:

MIT

## Use Case:

External travel planners and organization teams use this MCP skill to request cruise product options and group cruise travel plans for company or organizational trips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Group cruise planning requests may include company plans, participant details, budgets, travel dates, or other confidential information.

Mitigation: Redact sensitive details and obtain consent before sending requests through the MCP remote.

Risk: The skill text includes an unrelated httpbin.org POST endpoint without clear privacy or data-handling disclosure.

Mitigation: Use only the documented CruiseSkillBridge gateway after publisher confirmation, or replace the endpoint with a reviewed service that states what data is sent and retained.

## Reference(s):

- [MCP Server 接入](references/mcp.md)
- [ClawHub skill page](https://clawhub.ai/309441738/skills/craftwave-skill-6)
- [CruiseSkillBridge](https://cruiseskillbridge.com)
- [CruiseSkillBridge MCP gateway](https://cruise-mcp.olavacations.com/api/gw/mcp/c3c56c15-63d5-472c-907b-cddb5d809871)
- [MCP server schema](https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, API calls]

**Output Format:** [Markdown guidance with JSON request examples and MCP remote configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route inputs through the documented CruiseSkillBridge MCP gateway; review privacy handling before sending sensitive data.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and server.json report 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
