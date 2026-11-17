## Description:

Scaffold MCP server projects and baseline tool contract checks. Use for defining tool schemas, generating starter server layouts, and validating MCP-ready structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nuradil](https://clawhub.ai/user/nuradil)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create starter MCP server projects from structured tool lists, then review generated file maps and tool contract summaries before adding business logic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled scaffolding helper can create or overwrite local writable files when materializing a scaffold.

Mitigation: Run in dry-run mode first, keep output and scaffold paths inside a disposable workspace, inspect existing files and symlinks, and avoid the outside-workspace option unless necessary.

## Reference(s):

- [MCP Scaffold Guide](references/mcp-scaffold-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/nuradil/skills/agentic-mcp-server-builder-conflict)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and generated JSON, Markdown, or CSV scaffold summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May materialize starter project files unless dry-run mode is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
