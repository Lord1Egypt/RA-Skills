## Description:

Add Foresea forecasting tools to OpenClaw agents through Foresea's public remote MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pareelamre](https://clawhub.ai/user/pareelamre)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to connect OpenClaw agents to Foresea for probability forecasts, prediction-market analysis, market scans, edge rankings, and calibration evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forecasting questions may be sent to Foresea's remote MCP service.

Mitigation: Avoid private or sensitive scenarios unless sharing those query details with Foresea is acceptable.

Risk: Forecasts and prediction-market analysis can be mistaken for financial advice.

Mitigation: Present forecasts as decision support and preserve evidence links and caveats in final answers.

## Reference(s):

- [Foresea homepage](https://foresea.ink)
- [Foresea agent guide](https://foresea.ink/agents)
- [Foresea MCP endpoint](https://foresea.ink/mcp/)
- [Foresea agent manifest](https://foresea.ink/.well-known/agent.json)
- [Foresea OpenAPI](https://foresea.ink/openapi.json)
- [ClawHub skill page](https://clawhub.ai/pareelamre/skills/foresea)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include evidence links, forecast rationale, market analysis, ranked disagreements, and decision-support caveats.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
