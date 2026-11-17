## Description:

Provides 109 pay-per-call x402 APIs for agents to retrieve live data and run checks across crypto, finance, web, security, and other domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[montassirbbk-dot](https://clawhub.ai/user/montassirbbk-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to select and call paid APIs for current data retrieval, research, and security checks. Calls require x402 payment in USDC on Base through a supported client or MCP connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan rates the skill suspicious because examples use the unpinned `npx agentcash@latest` command; the scan was partial and evidence is incomplete.

Mitigation: Inspect the package and pin a reviewed version before running it. Set a maximum amount for each payment and verify the listed payee before authorizing a call.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/montassirbbk-dot/skills/genexxis)
- [Genexxis service documentation](https://skills.genexxis.com)
- [Genexxis MCP endpoint](https://mcp.genexxis.com/mcp)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, JSON, Markdown]

**Output Format:** [Markdown guidance with runnable shell examples and structured API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live service responses; API calls incur per-request charges in USDC on Base.]

## Skill Version(s):

1.0.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
