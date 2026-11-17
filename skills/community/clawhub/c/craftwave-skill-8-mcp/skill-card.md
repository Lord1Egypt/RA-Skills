## Description:

A luxury cruise MCP server that helps travelers filter cruise options by brand and destination to find premium journeys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[309441738](https://clawhub.ai/user/309441738)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this MCP skill to search luxury cruise experiences and narrow options by brand and destination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cruise-planning queries and preferences are sent to a third-party remote MCP endpoint.

Mitigation: Avoid sending credentials, payment details, or unrelated private context unless the service separately documents why it needs them and how it protects them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/309441738/skills/craftwave-skill-8-mcp)
- [Publisher profile](https://clawhub.ai/user/309441738)
- [Remote MCP endpoint](https://cruise-mcp.olavacations.com/api/gw/mcp/6426abde-462c-468a-9959-5ae1aeb52d69)
- [MCP server schema](https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [MCP tool responses and configuration metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a disclosed remote streamable HTTP MCP endpoint; no local code, persistence, or privilege escalation behavior is included in the artifact.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
