## Description:

Set up and operate dual Discord bots on one machine with isolated memory, channel allowlists, mention-gated reviewer bot behavior, optional one-way reviewer-to-primary context bridge, and safe backup/rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nbdxrycyl](https://clawhub.ai/user/nbdxrycyl)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure and recover a two-bot Discord setup with separated bot workspaces, channel allowlists, mention-gated reviewer behavior, and backup or rollback commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scripts can edit live OpenClaw bot configuration.

Mitigation: Review generated configuration changes before restarting gateways and run the skill only in the intended bot environment.

Risk: Backups may include sensitive bot configuration.

Mitigation: Store backups outside repositories or shared folders with private permissions.

Risk: Environment variables can alter script targets.

Mitigation: Run scripts with trusted environment variables and dedicated least-privileged bot accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nbdxrycyl/skills/discord-dual-bot-orchestrator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses placeholders for bot names, tokens, IDs, guilds, channels, and base directories.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
