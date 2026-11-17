## Description:

AgentRank helps agents find, compare, and evaluate MCP servers, agent tools, and AI skills using live scored search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superlowburn](https://clawhub.ai/user/superlowburn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent users use this skill to discover relevant MCP servers, agent tools, and AI skills when installing tools, comparing options, or encountering a capability gap during a project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to agentrank-ai.com and could expose confidential project details.

Mitigation: Keep queries generic and omit secrets, customer names, internal hostnames, private repository names, and other sensitive project details.

Risk: AgentRank scores may be mistaken for independent security validation.

Mitigation: Treat scores as one recommendation signal and separately review any selected tool or skill before adoption.

## Reference(s):

- [AgentRank ClawHub Skill Page](https://clawhub.ai/superlowburn/skills/agentrank)
- [AgentRank Search API](https://agentrank-ai.com/api/search)
- [AgentRank Tool Detail Page Example](https://agentrank-ai.com/tool/modelcontextprotocol/servers/)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown with links, AgentRank scores, ranks, and concise result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are based on user-provided query terms and may include links to AgentRank detail pages.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
