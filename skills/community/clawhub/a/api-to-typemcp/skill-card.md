## Description:

Use when turning supplied API sources into a safe TypeMCP project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sjungwon03](https://clawhub.ai/user/sjungwon03)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert supplied local OpenAPI, Swagger UI, or Markdown/HTML API references into a reviewed TypeMCP stdio MCP project. It is intended for project generation first, with optional agent installation only after verification and explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A replace-generation path can overwrite files outside the chosen output folder.

Mitigation: Generate into a newly created empty directory, avoid --replace on directories that were not created and inspected for this run, and review paths before generation.

Risk: Agent installation can modify persistent MCP client configuration.

Mitigation: Prefer project-only generation, review the secret-free installation plan, and require explicit confirmation before applying any agent configuration changes.

Risk: Generated project verification installs npm dependencies and may be untrusted.

Mitigation: Run npm verification in a container, VM, or equivalent host sandbox for untrusted inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sjungwon03/skills/api-to-typemcp)
- [TypeMCP Runtime Contract](references/type-mcp-runtime.md)
- [Agent MCP Installation Reference](references/agent-mcp-installation.md)
- [Hermes MCP documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp)
- [Claude Code MCP documentation](https://docs.anthropic.com/en/docs/claude-code/mcp)
- [Codex CLI MCP reference](https://developers.openai.com/codex/cli/reference)
- [Cursor MCP documentation](https://cursor.com/docs/mcp)
- [VS Code MCP servers documentation](https://code.visualstudio.com/docs/agent-customization/mcp-servers)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus generated TypeScript project files and JSON/TOML MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated projects use a pinned TypeMCP runtime line and may include optional agent installation plans or portable MCP server exports.]

## Skill Version(s):

0.2.6 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
