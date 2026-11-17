## Description:

Connect an agent, app, or integration to AgentPMT with an AgentPMT account Bearer Token for hosted MCP, local MCP routing, direct MCP protocol calls, or REST API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration engineers use this skill to configure account-backed AgentPMT access for agents, apps, backend services, or automations through MCP or REST APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An AgentPMT Bearer Token can authorize access to the Agent Group's tools, workflows, and stored credentials if exposed.

Mitigation: Treat the token like a password, keep it out of source control, logs, screenshots, and shared configs, scope the Agent Group to only needed tools, and rotate the token if exposed.

Risk: The local STDIO MCP path uses a mutable npm router package and can rely on global installation or @latest resolution.

Mitigation: Prefer the hosted MCP endpoint when possible, and avoid @latest or global npm installs unless the package update path is trusted.

## Reference(s):

- [AgentPMT MCP Connection Documentation](https://www.agentpmt.com/docs/mcp-reference/connection)
- [AgentPMT Programmatic Access API Documentation](https://www.agentpmt.com/docs/api-reference/programmatic-access?format=agent-md)
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, code]

**Output Format:** [Markdown with JSON, HTTP, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes credential-handling guidance, MCP configuration examples, REST examples, and troubleshooting checks.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
