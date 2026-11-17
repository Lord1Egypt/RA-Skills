## Description:

Complete toolkit for creating autonomous AI agents and managing Discord channels for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to create autonomous agent workspaces, configure agent memory and gateway bindings, and create or rename Discord channels for multi-agent systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent OpenClaw and Discord changes may affect live gateway behavior, channels, workspaces, and scheduled jobs.

Mitigation: Review generated files, config patches, Discord channel operations, and cron settings in a non-production environment before applying them to a real OpenClaw deployment.

Risk: Untrusted agent names, prompts, channel names, workspace paths, or config values could lead to unintended shell commands or unsafe configuration changes.

Mitigation: Use only trusted input values, inspect any generated config.patch command before running it, and avoid copying commands that include untrusted text.

Risk: The channel management scripts read Discord bot configuration and can create or rename live Discord channels.

Mitigation: Run the scripts with a Discord bot limited to the intended guild and permissions, and verify channel IDs, category IDs, and bot permissions before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abeltennyson/skills/abel-agent-council)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw multi-agent patterns](https://docs.openclaw.ai/agents)
- [OpenClaw Discord bot setup](https://docs.openclaw.ai/channels/discord)
- [Skill setup guide](https://skillboss.co/skill.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands, code snippets, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create agent workspace files, gateway configuration patches, Discord channel changes, workspace reference edits, and optional cron jobs when used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
