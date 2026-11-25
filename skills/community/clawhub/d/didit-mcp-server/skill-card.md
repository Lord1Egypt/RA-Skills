## Description:

Use when connecting an AI assistant or agent to a Didit account through the Didit MCP server (Model Context Protocol), not for backend REST integration code. Covers installing the hosted server in Claude Code, claude.ai, Claude Desktop, ChatGPT, OpenAI Codex, Cursor, VS Code, Windsurf, Zed or any MCP client; signing in with a Didit console account (OAuth 2.1) or connecting with an application API key; running the local stdio server or self-hosting the HTTP server, with device-code login; toolsets and read-only mode; and having an agent act in the Didit Business Console: workflows, sessions, standalone checks, users, transactions and rules, Travel Rule, lists, cases, webhooks, reports and billing. Covers scopes, roles, confirmations and file inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and account operators use this skill to connect an AI client to Didit and configure or manage verification workflows, sessions, and related account data through the MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected tools can change workflows and records or delete data.

Mitigation: Use read-only mode when changes are unnecessary, and get explicit approval before write or destructive actions.

Risk: Credentials and credential-bearing links can expose access to an account or application.

Mitigation: Use restricted, expiring credentials through client environment references; treat returned credentials and download links as secrets.

Risk: Security review confidence is medium because some referenced material could not be resolved.

Mitigation: Review the authentication and credential-handling instructions, and pin the Docker image when using the deployment example.

## Reference(s):

- [Didit MCP overview](https://docs.didit.me/integration/mcp/overview)
- [MCP authentication](https://docs.didit.me/integration/mcp/authentication)
- [MCP tools reference](https://docs.didit.me/integration/mcp/tools)
- [MCP toolsets and read-only mode](https://docs.didit.me/integration/mcp/toolsets)
- [Pricing](https://docs.didit.me/getting-started/pricing)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, API calls]

**Output Format:** [Markdown with inline configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
