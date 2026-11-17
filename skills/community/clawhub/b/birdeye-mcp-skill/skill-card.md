## Description:

Use Birdeye MCP through UXC for token market data, trending and discovery workflows, price monitoring, and DEX-related reads with help-first live tool discovery and API-key auth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to configure and query Birdeye MCP via UXC for token market data, trending discovery, price monitoring, and DEX-related read workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Birdeye API key and a persistent credential binding for the Birdeye MCP host.

Mitigation: Use the documented X-API-KEY binding only for mcp.birdeye.so/mcp, store the secret in an environment variable or secret manager, and review the binding before use.

Risk: The Birdeye MCP tool surface is described as beta and may change over time.

Mitigation: Run host help and operation help before execution, avoid hardcoded tool or argument assumptions, and keep automation focused on stable JSON envelope fields.

Risk: Market-data and discovery workflows could be misused as trading or transaction execution guidance.

Mitigation: Treat the skill as read-only market and discovery access, use narrow queries, and do not treat live MCP output as a trading executor.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Birdeye MCP Endpoint](https://mcp.birdeye.so/mcp)
- [ClawHub Skill Page](https://clawhub.ai/jolestar/skills/birdeye-mcp-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON response parsing guidance for MCP reads; not a trading or transaction execution surface.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
