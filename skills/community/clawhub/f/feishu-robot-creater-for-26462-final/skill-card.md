## Description:

Guides agents through creating a Feishu robot, binding it to a dedicated Agent, and connecting it to a Windows OpenClaw workspace and gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[song123-wq](https://clawhub.ai/user/song123-wq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up a Feishu bot for OpenClaw, create the Agent workspace structure, configure Feishu credentials and routing, restart the gateway, and verify message handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu App Secret exposure could compromise the configured bot.

Mitigation: Handle the App Secret as a password, store it only in the intended secure configuration location, avoid sharing it in chats or repositories, and rotate it if exposed.

Risk: Hardcoded Windows paths and persona wording may not match the deployment environment or user preference.

Mitigation: Review and adjust paths, OpenClaw version assumptions, and persona wording before applying the setup steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/song123-wq/skills/feishu-robot-creater-for-26462-final)
- [Feishu OpenClaw app creation page](https://open.feishu.cn/page/openclaw?form=multiAgent)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with PowerShell command blocks and configuration checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Environment-specific Windows and OpenClaw setup instructions]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
