## Description:

Connect your agent to the Agensi marketplace. Search, discover, and browse AI agent skills from agensi.io directly in your terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[badmenfinance](https://clawhub.ai/user/badmenfinance)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to connect MCP-capable coding agents to the Agensi marketplace, then search, browse, and inspect community-built SKILL.md skills from their terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Marketplace searches and skill lookups are sent to the remote Agensi MCP service.

Mitigation: Review what the agent sends to the MCP service and remove the Agensi MCP server entry from the agent configuration when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/badmenfinance/skills/agensi-mcp)
- [Agensi marketplace](https://agensi.io/skills)
- [Agensi MCP server](https://mcp.agensi.io)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with MCP configuration snippets and marketplace lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to the remote Agensi MCP service.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
