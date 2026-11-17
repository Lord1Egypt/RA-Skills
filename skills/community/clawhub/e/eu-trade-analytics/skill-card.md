## Description:

Query 28M+ Eurostat COMEXT trade records for EU bilateral flows, product codes, prices, seasonality, and market concentration from 1988-2025.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drivenbymyai-max](https://clawhub.ai/user/drivenbymyai-max)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query EU trade analytics, compare bilateral flows, identify top partners, analyze price trends, and calculate market concentration for products and countries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes trade-data queries to SputnikX as an external provider, including free and paid x402-labeled endpoints.

Mitigation: Install only if the user trusts SputnikX, review any x402 payment flow before use, and avoid sending confidential business plans or sensitive queries unless that provider is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drivenbymyai-max/skills/eu-trade-analytics)
- [SputnikX homepage](https://sputnikx.xyz)
- [SputnikX agent API](https://sputnikx.xyz/api/v1/agent)
- [SputnikX MCP endpoint](https://mcp.sputnikx.xyz/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and endpoint guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces trade-data query guidance for SputnikX API and MCP endpoints; no local files or persistent state are created by the skill.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
