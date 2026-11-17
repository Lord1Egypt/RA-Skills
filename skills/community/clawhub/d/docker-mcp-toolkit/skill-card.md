## Description:

Control and use an MCP Toolkit running in Docker. Use when setting up Docker MCP Toolkit (docker compose up/down), checking status/logs, configuring environment variables/secrets, listing available MCP tools/servers, or invoking MCP tools (typically via a local HTTP endpoint) to connect OpenClaw workflows to external systems like Postgres/Neon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pcauhi](https://clawhub.ai/user/pcauhi)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to operate Docker Desktop's MCP Toolkit from an agent workflow, including preflight checks, server management, tool discovery, and simple MCP tool invocation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Enabled Docker MCP servers can expose access to external systems such as databases or service APIs.

Mitigation: Review enabled servers before use and configure least-privilege credentials for each external service.

Risk: Publicly exposed MCP gateway endpoints could allow unintended remote tool access.

Mitigation: Keep gateway endpoints bound to localhost and use SSH tunnels or WireGuard when remote access is required.

Risk: Secrets pasted into chat or stored in broad-scope credentials can be reused beyond the intended workflow.

Mitigation: Prefer Docker Desktop secrets or keychain integration and rotate credentials immediately if they are pasted into chat.

Risk: The bundled tool-call wrapper supports only primitive JSON values, so nested tool arguments may fail or require manual invocation.

Mitigation: Inspect the target tool schema and run docker mcp tools call directly for tools that require object or array arguments.

## Reference(s):

- [Docker MCP Toolkit interface notes](references/toolkit-interface.md)
- [Security notes](references/security.md)
- [Compose template reference](references/compose-template.yml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local docker mcp commands through bundled shell scripts when the required CLI tools are available.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
