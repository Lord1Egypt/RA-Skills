## Description:

Turn any CLI or MCP server into an Agent Skill. Use when you want to replace an MCP server with a zero-overhead CLI skill, or generate a skill from any command-line tool's --help output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2233admin](https://clawhub.ai/user/2233admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use cli2skill to generate Agent Skill markdown from command-line tools or MCP servers so agents can call those tools through shell commands without a persistent MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated skill files may preserve unsafe or misleading behavior from untrusted CLI or MCP output.

Mitigation: Review and scan generated skill files before placing them in an active agent skill directory.

Risk: Running the generator against untrusted CLIs or MCP servers can expose the agent workflow to commands with broad shell authority.

Mitigation: Use trusted and pinned tools, run with a minimal environment, and write first to a staging output directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2233admin/skills/cli2skill)
- [Agent Skills](https://agentskills.io)
- [Anthropic: Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Claude Code issue 38228](https://github.com/anthropics/claude-code/issues/38228)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown skill files with YAML frontmatter and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated skill markdown to a chosen output directory or print it to stdout.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact pyproject.toml reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
