## Description:

HTTP bridge that keeps MCP servers alive and exposes them via REST. Built for OpenClaw agents that need MCP tools without native MCP support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitbrujo](https://clawhub.ai/user/bitbrujo)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Cherry MCP to keep configured MCP servers running as child processes and expose their tools through local HTTP REST endpoints for OpenClaw agents or other clients without native MCP support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bridge exposes powerful MCP tool calls and restart actions over HTTP without built-in authentication.

Mitigation: Keep the service bound to localhost or protect it with real authentication, restrict CORS, and avoid exposing it directly to a network.

Risk: Configured MCP server commands and packages run as child processes on the host.

Mitigation: Pin and review MCP server packages before use, and run the bridge under a low-privilege account with minimal environment variables.

Risk: API keys stored through the CLI are saved in plain text in config.json.

Mitigation: Do not store secrets in config.json; provide credentials through the runtime environment and keep local configuration out of source control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bitbrujo/skills/cherry-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, and HTTP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes commands and configuration for running a local MCP-to-HTTP bridge.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
