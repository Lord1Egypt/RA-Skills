## Description:

Connects a self-hosted local MCP server, DevSpace, to the ChatGPT web UI by guiding environment checks, dependency setup, DevSpace configuration, Tailscale Funnel exposure, ChatGPT connector creation, and OAuth authorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hawklithm](https://clawhub.ai/user/hawklithm)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to connect ChatGPT to a local DevSpace MCP server so ChatGPT can work with selected local project files and shell tools. It is also used to diagnose connector, OAuth, Tailscale Funnel, DevSpace configuration, and cross-platform setup failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose a local command-capable DevSpace server to ChatGPT through a public tunnel.

Mitigation: Use one low-risk allowedRoots project, exclude secrets and production or customer data, and close Tailscale Funnel when finished.

Risk: The connected server can read and write selected local project files and run shell commands with the local user's permissions.

Mitigation: Review the selected roots before startup and avoid broad paths such as a home directory or entire disk.

Risk: Setup may install dependencies or require elevated approval for Tailscale and related tooling.

Mitigation: Run read-only checks first and review every install command before approving installation or elevation prompts.

Risk: Browser automation may handle the DevSpace ownerToken during OAuth authorization.

Mitigation: Prefer manual ownerToken authorization when appropriate, and do not print, paste, log, or pass the token as a command-line argument.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hawklithm/skills/chatgpt-mcp-connector)
- [Publisher profile](https://clawhub.ai/user/hawklithm)
- [Repository metadata link](https://github.com/hawklithm/chatgpt-mcp-connector)
- [README](README.md)
- [Environment and DevSpace setup](references/env-setup.md)
- [DevSpace configuration and startup](references/devspace-config.md)
- [Tailscale Funnel setup](references/tailscale-funnel.md)
- [ChatGPT connector and authorization](references/chatgpt-connector.md)
- [Cross-platform compatibility](references/cross-platform.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include staged setup steps, checks, fallback instructions, and user-action prompts.]

## Skill Version(s):

0.0.2 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
