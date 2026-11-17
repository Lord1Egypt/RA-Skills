## Description:

Complete toolkit for creating autonomous AI agents and managing Discord channels for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[izletenadam-creator](https://clawhub.ai/user/izletenadam-creator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Agent Council to create OpenClaw agents, bind them to Discord channels, and manage channel setup or renaming for multi-agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scripts can make durable OpenClaw gateway, workspace, Discord channel, and optional cron changes.

Mitigation: Review the scripts and generated config patches before installing or running them, and back up OpenClaw gateway configuration first.

Risk: Agent names, IDs, models, workspaces, and channel IDs are treated as trusted input for generated files and configuration.

Mitigation: Limit use to trusted operators and validate these values before executing the scripts.

Risk: Discord channels and agent memory may contain sensitive or personal data.

Mitigation: Avoid sensitive health or personal data in Discord channels and agent memory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/izletenadam-creator/skills/agent-council-skip)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw Agents Documentation](https://docs.openclaw.ai/agents)
- [OpenClaw Discord Channels Documentation](https://docs.openclaw.ai/channels/discord)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown files, JSON gateway patches, shell commands, and console guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can make durable OpenClaw gateway, workspace, Discord channel, and optional cron changes when scripts are executed.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
