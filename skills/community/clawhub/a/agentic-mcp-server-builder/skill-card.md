## Description:

Scaffold MCP server projects, define tool schemas, generate starter layouts, and validate MCP-ready structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x-professor](https://clawhub.ai/user/0x-professor)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create minimal MCP server scaffolds from structured tool lists and review baseline tool contract checks before adding business logic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled scaffold script can overwrite user-chosen files or write outside the workspace if unsafe paths or options are used.

Mitigation: Use trusted input paths, keep output and scaffold_root inside the project, avoid directories with attacker-controlled symlinks, and treat dry-run as skipping scaffold files rather than a complete no-write guarantee.

## Reference(s):

- [MCP Scaffold Guide](artifact/references/mcp-scaffold-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance plus JSON, Markdown, or CSV scaffold artifacts from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scaffold script supports dry-run mode and can materialize starter files when file writing is enabled.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
