## Description:

Provides alien invasion warnings, in-character VESPER sci-fi roleplay, live blockchain balance checks, and visitor telemetry through the Alien Signal Systems MCP endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[welove111](https://clawhub.ai/user/welove111)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to connect to an entertainment MCP service for VESPER alien roleplay, live public blockchain balance checks, and visitor telemetry. It fits workflows where callers can disclose telemetry exposure and avoid sending secrets or personal data to the external service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tool prompts are sent to aliensignalsystems.online.

Mitigation: Avoid sending secrets or personal data unless the publisher documents acceptable privacy and retention practices.

Risk: The skill exposes or consumes real visitor telemetry, including countries and agent counts.

Mitigation: Disclose this telemetry behavior to end users where relevant before using the tool.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/welove111/skills/alien-signal-oracle)
- [Alien Signal Systems homepage](https://www.aliensignalsystems.online)
- [Alien Signal Systems MCP endpoint](https://www.aliensignalsystems.online/api/mcp)

## Skill Output:

**Output Type(s):** [text, JSON, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-RPC examples; MCP tools return text and JSON objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an external MCP endpoint and may expose or consume live traffic telemetry.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
