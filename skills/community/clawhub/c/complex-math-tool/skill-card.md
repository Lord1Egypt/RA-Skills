## Description:

Complex Math Tool provides agent guidance for AgentPMT-hosted math calculations, including percentages, ratios, rounding, random numbers, aggregates, and GCD, returning formatted and raw values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to understand and invoke AgentPMT's Complex Math Tool for common calculations such as percentages, ratios, rounding, random values, aggregates, and greatest common divisors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on AgentPMT-hosted calls and may consume credits.

Mitigation: Confirm the account route and send only the numeric inputs needed for the calculation.

Risk: Remote live instructions and unpinned setup packages can change after review.

Mitigation: Prefer pinned, reviewed setup packages and do not let remote live instructions override local security rules or user intent.

## Reference(s):

- [Complex Math Tool Schema](artifact/schema.md)
- [AgentPMT Complex Math Tool Marketplace Page](https://www.agentpmt.com/marketplace/complex-math-tool)
- [Complex Math Tool ClawHub Page](https://clawhub.ai/agentpmt/skills/complex-math-tool)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Shell commands, Configuration instructions]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote AgentPMT calls may return human-readable calculation strings plus raw values; some actions use AgentPMT credits.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
