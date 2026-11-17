## Description:

Provides agent instructions for AgentPMT-hosted remote tool calls that return current air quality, pollutant levels, pollen forecasts, historical air quality, and map data for locations worldwide.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to check air quality and pollen conditions, compare pollutants across locations, review recent history, and generate temporary environmental map URLs for planning or health-related workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned setup and install instructions can pull changing dependencies or setup skills.

Mitigation: Review linked setup skills separately and prefer pinned or otherwise verified installation sources before deployment.

Risk: Location inputs may include precise home, workplace, or other sensitive addresses.

Mitigation: Send only the minimum location precision needed for the task and avoid sensitive addresses unless necessary.

Risk: Generated map URLs are remotely stored artifacts that may remain available for up to 7 days.

Mitigation: Treat returned map links as shareable remote artifacts and avoid generating maps for sensitive locations or contexts.

## Reference(s):

- [Air Quality Pollen Information Schema](artifact/schema.md)
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/air-quality-pollen-information)
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/air-quality-pollen-information)
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, API Calls, JSON, Shell commands]

**Output Format:** [Markdown instructions with JSON request examples and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides calls that can return English JSON responses and temporary map download URLs retained for up to 7 days.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
