## Description:

Secure, sandboxed filesystem access enabling agents to list, read, write, create, move, delete, search files and directories within allowed paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buddhasource](https://clawhub.ai/user/buddhasource)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to configure filesystem access for agents that need to inspect, edit, organize, or generate files within explicitly allowed directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead agents to use filesystem tools with broad read, write, move, and delete authority.

Mitigation: Grant access only to narrow project directories, prefer read-only mode unless writes are required, and require review before bulk moves, overwrites, or deletes.

Risk: Routine startup with mutable package resolution can run code that has not been reviewed for the current deployment.

Mitigation: Use a pinned, reviewed package version instead of routine npx -y startup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/buddhasource/skills/filesystem-mcp)
- [Model Context Protocol servers repository](https://github.com/modelcontextprotocol/servers)
- [Filesystem server source](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
- [Model Context Protocol documentation](https://modelcontextprotocol.io/)
- [MCP security best practices](https://modelcontextprotocol.io/docs/concepts/security)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance and usage examples for configuring a filesystem MCP server.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
