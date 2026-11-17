## Description:

Comprehensive Claude Code CLI reference covering interactive mode, CLI flags, commands, environment variables, hooks, channels, checkpointing, plugins, and tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awalesagar](https://clawhub.ai/user/awalesagar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Claude Code users use this skill as a quick reference for CLI commands, configuration, workflows, keyboard shortcuts, permissions, hooks, plugins, channels, checkpointing, and tool behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Readers may copy guidance for permission bypass, remote control, development channels, hooks, scheduled tasks, tokens, telemetry, or proxies without considering privacy or system integrity impact.

Mitigation: Treat the skill as a reference aid; review advanced settings against project policy before applying them and keep credentials out of shared configuration.

Risk: Hook, channel, and MCP examples can connect external events or tools to an agent session.

Mitigation: Use trusted local configurations, gate inbound messages from untrusted sources, and keep approval controls enabled for actions that affect files, systems, or services.

Risk: Checkpoint guidance may be mistaken for full version control coverage.

Mitigation: Use Git or another source control system for durable history because checkpoints do not cover bash, manual, external, or concurrent-session file changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/awalesagar/skills/code-with-claude)
- [CLI Reference](references/cli-reference.md)
- [Commands](references/commands.md)
- [Interactive Mode](references/interactive-mode.md)
- [Hooks Reference](references/hooks.md)
- [Plugins Reference](references/plugins.md)
- [Channels Reference](references/channels.md)
- [Checkpointing](references/checkpointing.md)
- [Tools Reference](references/tools.md)
- [Environment Variables](references/env-vars.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reference guidance with inline code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; does not execute code directly.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
