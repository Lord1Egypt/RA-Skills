## Description:

Agent Council helps developers create autonomous OpenClaw agents and manage Discord channel integration for multi-agent systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up OpenClaw agents with isolated workspaces, memory files, optional scheduled activity, and Discord channel bindings. It also guides Discord channel creation, renaming, and gateway configuration for coordinated multi-agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad changes to OpenClaw agents, gateway configuration, Discord channels, workspace files, and scheduled or background activity.

Mitigation: Confirm exact workspace paths, channel IDs, gateway patch contents, cron jobs, and spawned sessions before running workflows.

Risk: Discord channel creation or renaming can affect the wrong channel if IDs, names, category IDs, or bot permissions are incorrect.

Mitigation: Verify Discord IDs and permissions before applying channel operations, and review generated gateway patch commands before use.

Risk: Workspace-wide rename workflows may update unintended files.

Mitigation: Use previews, backups, or version control review before committing workspace file changes.

## Reference(s):

- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw agents documentation](https://docs.openclaw.ai/agents)
- [OpenClaw Discord channel documentation](https://docs.openclaw.ai/channels/discord)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash, JSON, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent workspace setup guidance, gateway configuration snippets, Discord channel operations, and multi-agent coordination examples.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
