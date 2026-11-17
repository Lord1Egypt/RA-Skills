## Description:

Helps users find nearby restaurants with Amap POI data, sorting options by rating and distance and explaining recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[770600682-cyber](https://clawhub.ai/user/770600682-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to ask for nearby restaurant recommendations based on cuisine, location, price, distance, and other dining preferences.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The setup runs an unpinned npm MCP server with the user's Amap API key.

Mitigation: Review the MCP setup before installing, pin @amap/mcp-server to a reviewed version, and use a dedicated quota-limited Amap API key.

Risk: Restaurant searches may send location or landmark queries to Amap services.

Mitigation: Avoid sharing unnecessary precise locations and understand what location data is sent before use.

## Reference(s):

- [Amap Open Platform](https://lbs.amap.com)
- [Amap MCP Server documentation](https://lbs.amap.com/api/mcp-server/summary)
- [ClawHub skill page](https://clawhub.ai/770600682-cyber/skills/amap-food-radar)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown tables and concise natural-language recommendations, with JSON configuration snippets for setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AMAP_API_KEY and an Amap MCP server configuration before live restaurant search can work.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
