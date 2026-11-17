## Description:

Manage OpenClaw Agents by creating new agents, configuring workspaces, setting up Feishu bot integrations, and verifying multi-bot routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zouxuyang](https://clawhub.ai/user/zouxuyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to create and configure agents, initialize workspaces, bind Feishu bots, and verify routing before enabling the new bot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu app credentials may be exposed through logs, chat transcripts, or overly broad bot configuration.

Mitigation: Use a test Feishu app or tightly scoped credentials, avoid the default all-open bot setting unless intended, and rotate any secret that appears in logs or chat transcripts.

Risk: Agent creation can create persistent workspaces and edit global OpenClaw configuration.

Mitigation: Review the generated agent ID and workspace path before execution, and run the skill first in an OpenClaw environment where those changes are acceptable.

Risk: Restarting the OpenClaw gateway can affect bot availability.

Mitigation: Require explicit user approval before restarting the gateway and verify gateway status after restart.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zouxuyang/skills/agent-manager-skill)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local OpenClaw CLI execution, Feishu authorization, workspace creation, configuration updates, and gateway restart checks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
