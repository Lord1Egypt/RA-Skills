## Description:

Use when the user asks to connect an AI agent to external apps via Composio, or when Composio CLI or MCP setup fails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afonsoft](https://clawhub.ai/user/afonsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure, verify, and troubleshoot Composio CLI and MCP access so agents can connect to external applications through Composio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup helper can persistently modify multiple agent MCP configuration files.

Mitigation: Run the helper with --dry-run and --platform first, then review the exact config diff before applying changes.

Risk: A Composio consumer key can be copied into local MCP configuration as plaintext.

Mitigation: Prefer environment variables or a supported secret store, avoid committing config files containing keys, and rotate the consumer key if it may have been exposed.

Risk: Composio tools can act on connected external applications and may mutate data or send messages.

Mitigation: Inspect schemas and use dry-run checks before mutating actions; avoid --skip-checks unless the request and target account are already verified.

## Reference(s):

- [Composio Connect documentation](https://docs.composio.dev/docs/composio-connect)
- [Composio GitHub repository](https://github.com/ComposioHQ/composio)
- [Composio consumer project boundaries and auth selection](https://docs.composio.dev/kb/guide/consumer-project-boundaries-and-auth-selection)
- [Composio MCP configuration reference](references/mcp-config.md)
- [Composio CLI reference](references/cli-reference.md)
- [MCP platform config quirks](references/platform-quirks.md)
- [Composio tool inventory](references/tools-inventory.md)
- [Composio troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional helper scripts for MCP setup and verification; may propose config-file edits and Composio CLI commands.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
