## Description:

Connects OpenClaw to the AutoSend email MCP server through mcporter for managing email campaigns, templates, contacts, and senders via AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shindebhau](https://clawhub.ai/user/shindebhau)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and email operations teams use this skill to configure an AutoSend MCP connection in OpenClaw and manage email campaigns, templates, contacts, senders, and analytics through AI-assisted MCP tool calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth tokens are stored locally in ~/.mcporter/autosend/tokens.json and could grant account access if exposed.

Mitigation: Treat the token file like a password: keep it out of repositories, logs, shared folders, and insecure backups, restrict local file access where possible, and revoke or re-authenticate after suspected exposure.

Risk: The setup installs mcporter without a pinned package version.

Mitigation: Install only if you trust the mcporter package and, where policy requires, pin or review the package before use.

Risk: The exposed MCP tools can create, update, duplicate, and delete AutoSend campaign and template assets.

Mitigation: Review agent-proposed changes before execution, especially actions that modify or delete campaign content, templates, or sender-related configuration.

## Reference(s):

- [AutoSend MCP Docs](https://docs.autosend.com/ai/mcp-server)
- [mcporter GitHub](https://github.com/steipete/mcporter)
- [mcporter on ClawHub](https://clawhub.ai/steipete/mcporter)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AutoSend account, mcporter, OAuth authentication, and local token storage.]

## Skill Version(s):

0.1.3 (source: server release metadata; artifact frontmatter is 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
