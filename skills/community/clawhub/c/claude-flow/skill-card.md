## Description:

Claude Flow helps Claude Code users orchestrate specialized agents for software engineering workflows, including coding, review, testing, architecture, documentation, and memory-assisted task reuse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to install and configure Claude Flow/Ruflo in Claude Code, start specialist agents or multi-agent swarms, and route software engineering tasks such as implementation, review, testing, architecture, and documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install guidance includes one-line installer commands and mutable package references such as ruflo@latest.

Mitigation: Review installers before execution and prefer pinned, reviewed package versions for installation and MCP startup.

Risk: The workflow requires API keys and can place credentials in shell or MCP configuration.

Mitigation: Pass only required credentials and keep API keys out of shell history and plaintext configuration where possible.

Risk: The skill registers a user-scoped MCP server and uses local vector memory that may persist workflow data.

Mitigation: Understand how to remove the MCP registration and clear vector memory before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cn-big-cabbage/skills/claude-flow)
- [Claude Flow homepage](https://github.com/ruvnet/claude-flow)
- [npm package: claude-flow](https://www.npmjs.com/package/claude-flow)
- [Installation guide](guides/01-installation.md)
- [Quickstart guide](guides/02-quickstart.md)
- [Advanced usage guide](guides/03-advanced-usage.md)
- [Troubleshooting guide](troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing instructions for installing, configuring, orchestrating agents, and troubleshooting Claude Flow/Ruflo workflows.]

## Skill Version(s):

0.1.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
