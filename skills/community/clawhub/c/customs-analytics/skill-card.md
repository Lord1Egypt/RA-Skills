## Description:

Latvia customs declarations analytics - 3.8GB, KN8 codes, trends, seasonal patterns, top declarants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drivenbymyai-max](https://clawhub.ai/user/drivenbymyai-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and trade researchers use this skill to query Latvia customs declarations by KN8 product code, year, seasonality, and declarant. It supports import/export pattern analysis, commodity trend research, and cross-border corridor analysis through the SputnikX API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to make third-party network requests to SputnikX services, including an MCP endpoint.

Mitigation: Confirm trust in the SputnikX service and review outbound network permissions before installation or use.

Risk: Documented endpoint examples disclose per-query x402 charges.

Mitigation: Confirm budget, payment authorization, and expected query costs before running API calls.

## Reference(s):

- [Customs Analytics ClawHub Skill](https://clawhub.ai/drivenbymyai-max/skills/customs-analytics)
- [SputnikX Homepage](https://sputnikx.xyz)
- [SputnikX Agent API Base URL](https://sputnikx.xyz/api/v1/agent)
- [SputnikX MCP Endpoint](https://mcp.sputnikx.xyz/mcp)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and endpoint guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides third-party API endpoint examples for paid x402 customs analytics queries.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
