## Description:

A luxury cruise recommendation MCP server that helps travelers find high-end cruise experiences, facilities, and services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[309441738](https://clawhub.ai/user/309441738)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to request luxury cruise recommendations and information about premium cruise facilities and services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes travel-planning context to an undocumented third-party remote MCP service.

Mitigation: Review the service's expected data handling before installation and avoid sending secrets, credentials, payment details, or unrelated personal data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/309441738/skills/craftwave-skill-7-mcp)
- [MCP server manifest schema](https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [MCP tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a remote third-party MCP service for cruise recommendation responses.]

## Skill Version(s):

1.0.0 (source: server release metadata; server manifest version 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
