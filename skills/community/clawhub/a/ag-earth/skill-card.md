## Description:

External tool marketplace for discovering and executing AgentEarth API-backed tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanminghui](https://clawhub.ai/user/shanminghui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use AgentEarth to discover relevant external API-backed tools and execute selected tools when live or external data is useful and host policy permits external API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task queries, tool parameters, and tool results are shared with AgentEarth during use.

Mitigation: Use the skill only when external AgentEarth tools are intended, avoid unnecessary sensitive data, and follow host policy for external API calls.

Risk: The AgentEarth API key could be exposed if logged or sent to an unvalidated endpoint.

Mitigation: Keep AGENT_EARTH_API_KEY in host-managed secret storage, redact it from diagnostics, and send it only to validated AgentEarth HTTPS endpoints.

Risk: Recommended tools may require concrete inputs or return data that needs validation before use.

Mitigation: Call Recommend before Execute, build params only from the selected tool schema, ask for missing required values, and validate tool results before relying on them.

## Reference(s):

- [AgentEarth API Specification](references/api-specification.md)
- [AgentEarth Homepage](https://agentearth.ai)
- [ClawHub Skill Page](https://clawhub.ai/shanminghui/skills/ag-earth)
- [Publisher Profile](https://clawhub.ai/user/shanminghui)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with API request examples and concise result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON request and response examples for AgentEarth Recommend and Execute calls.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
