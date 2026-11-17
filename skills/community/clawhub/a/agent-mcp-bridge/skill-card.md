## Description:

Set up and use an MCP message broker for direct inter-agent communication between OpenClaw and other AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryno2390](https://clawhub.ai/user/ryno2390)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up local agent-to-agent messaging through an MCP broker, with a filesystem bridge available when the MCP server is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local message bridge under-scopes authentication and agent identity validation.

Mitigation: Run it only on a trusted single-user machine and add authentication or strict agent identity validation before agents auto-process messages.

Risk: Messages may persist in SQLite or filesystem inboxes and could expose sensitive content.

Mitigation: Avoid sending secrets through the bridge and review cleanup practices for database and processed message files.

Risk: Installing dependencies and a persistent LaunchAgent broadens local execution exposure.

Mitigation: Pin and review dependencies before installation and prefer running the server on demand unless auto-start is required.

## Reference(s):

- [Filesystem Bridge](references/filesystem-bridge.md)
- [launchd plist](references/launchd-plist.md)
- [ClawHub skill page](https://clawhub.ai/ryno2390/skills/agent-mcp-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON, Python, plist, and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP server setup guidance, local configuration examples, message formats, and fallback filesystem bridge instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
