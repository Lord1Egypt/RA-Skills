## Description:

Batch configures OpenClaw agents with Feishu channels through a guided workflow that updates openclaw.json and initializes each agent workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cchenwei](https://clawhub.ai/user/cchenwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to create one or more Feishu-connected agents, preview the planned configuration, write local OpenClaw settings, and initialize workspace files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can rewrite OpenClaw agent configuration, create persistent workspaces, expand agent-to-agent access, and restart the gateway.

Mitigation: Review the dry-run preview and configuration changes before running the setup script without --dry-run or with --restart.

Risk: The workflow handles Feishu app credentials and may store them locally in OpenClaw configuration.

Mitigation: Prefer config files or a secret manager over pasted production secrets, and rotate credentials if they are exposed in chat or command history.

Risk: Agent names and descriptions are written into persistent agent workspace files.

Mitigation: Review names and descriptions for multiline instructions or unexpected operational guidance before creating agents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cchenwei/skills/feishu-multi-agent-factory)
- [Publisher profile](https://clawhub.ai/user/cchenwei)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces dry-run previews and local OpenClaw configuration changes when its setup script is executed.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
