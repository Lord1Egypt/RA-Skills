## Description:

Install and configure the DefiLlama MCP server for DeFi analytics, including setup commands, OAuth authentication guidance, verification steps, and optional workflow-skill installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reynardoew](https://clawhub.ai/user/reynardoew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to connect supported agents to DefiLlama's MCP server for DeFi analytics, OAuth authentication, and access to market, protocol, yield, token, bridge, and related tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install remote workflow skills without confirmation.

Mitigation: Review and pin the package or repository before running any workflow-skill installer.

Risk: OAuth tokens are stored in the agent environment and callback URLs may be shared through messaging channels.

Mitigation: Use trusted environments, avoid shared or logged channels for full callback URLs, and confirm token storage expectations before setup.

## Reference(s):

- [DefiLlama MCP server endpoint](https://mcp.defillama.com/mcp)
- [DefiLlama subscription page](https://defillama.com/subscribe)
- [ClawHub skill page](https://clawhub.ai/reynardoew/skills/defillama-setup)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup instructions and configuration snippets; does not itself provide API credentials.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
