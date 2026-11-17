## Description:

FlowSwarm helps agents coordinate multi-agent coding workflows with RuFlo and Claude Code for test generation, feature builds, refactors, security audits, and quality loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[windseeker1111](https://clawhub.ai/user/windseeker1111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use FlowSwarm to plan and run multi-agent coding sessions for larger coding tasks such as generating tests, building features, refactoring, auditing security, and iterating on quality. It is intended for context-rich work where generated commands, code, and configuration changes can be reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can grant broad Claude/MCP authority and persist project-level coordination state.

Mitigation: Use the skill only in a disposable or well-isolated development environment and review generated code, commands, and configuration before applying them.

Risk: The setup script installs RuFlo globally, registers an MCP server, edits `.mcp.json`, and may start a background daemon.

Mitigation: Pin the RuFlo package version, inspect `.mcp.json` before and after setup, and start persistent background services only when explicitly intended.

Risk: Example launch commands use `--permission-mode bypassPermissions`, which reduces execution safeguards during coding runs.

Mitigation: Avoid bypassing permissions unless the workspace is disposable and the task has been reviewed for expected file and command access.

## Reference(s):

- [FlowSwarm Template Library](references/template-examples.md)
- [ClawHub skill page](https://clawhub.ai/windseeker1111/skills/flow-swarm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with prompt templates, shell commands, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup and verification instructions; users should review generated commands, code, and configuration before execution.]

## Skill Version(s):

2.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
