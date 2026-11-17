## Description:

Create, deploy, and manage MCP (Model Context Protocol) servers using the MCPHero platform via the mcpheroctl CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arterialist](https://clawhub.ai/user/arterialist)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, configure, deploy, and manage MCPHero-hosted MCP servers that wrap APIs, databases, or other integrations for MCP-compatible clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to install and authenticate a third-party CLI before creating or managing MCPHero servers.

Mitigation: Verify the mcpheroctl package source before installation and use the skill only with MCPHero accounts and servers the user intends to manage.

Risk: Authentication tokens, bearer tokens, and integration secrets may be passed through commands or stored in client configuration.

Mitigation: Avoid putting real tokens or passwords directly in shell commands when safer input methods exist, use narrowly scoped credentials, and protect any client config containing bearer tokens.

## Reference(s):

- [Create MCP Server on ClawHub](https://clawhub.ai/arterialist/skills/create-mcp-server)
- [MCPHero Dashboard](https://mcphero.app)
- [MCPHero Production API](https://api.mcphero.app/api)
- [Publisher profile: arterialist](https://clawhub.ai/user/arterialist)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include placeholders for server IDs, bearer tokens, environment-variable IDs, URLs, and CLI arguments.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
