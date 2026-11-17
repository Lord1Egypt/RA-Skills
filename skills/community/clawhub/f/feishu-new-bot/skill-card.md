## Description:

Guides an agent through creating and configuring a new Feishu bot, including app creation, workspace setup, configuration, file synchronization, identity files, and connection validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinchenjia](https://clawhub.ai/user/jinchenjia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide creation of a new Feishu bot and prepare its OpenClaw workspace. It is intended for setup workflows that require user-created Feishu app credentials, configuration updates, workspace file synchronization, and connection testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks the agent to handle Feishu APP SECRET values.

Mitigation: Use a secret manager, environment variable, or protected input path instead of pasting secrets into chat; avoid plaintext storage unless permissions and rotation procedures are clear.

Risk: The workflow copies USER.md, MEMORY.md, AGENTS.md, and TOOLS.md content into a new bot workspace.

Mitigation: Review and minimize personal, workspace, and memory files before copying them into the new workspace.

Risk: The workflow updates openclaw.json and restarts the gateway.

Mitigation: Require explicit user approval before configuration changes, confirm the target workspace path, and validate the bot connection after restart.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jinchenjia/skills/feishu-new-bot)
- [Feishu Open Platform bot creation page](https://open.feishu.cn/page/openclaw?form=multiAgent)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, markdown]

**Output Format:** [Markdown guidance with checklists, file names, paths, and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in workspace files and configuration changes after user approval.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
