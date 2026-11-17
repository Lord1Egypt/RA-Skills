## Description:

Create a new OpenClaw agent and bind it to a dedicated Telegram group with workspace ~/claw-<agent-name>.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheetaa](https://clawhub.ai/user/sheetaa)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to provision a dedicated OpenClaw agent, workspace, and Telegram group binding for one-agent-one-group deployments. It is intended for repeatable setup flows that require explicit user approval before browser automation, local OpenClaw configuration changes, or gateway restart.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provisions a persistent OpenClaw agent bound to a Telegram group that can respond without being mentioned.

Mitigation: Use a dedicated group limited to trusted participants and verify no-mention reply mode only for the intended group.

Risk: The skill modifies local OpenClaw configuration and creates backup files that may persist after deprovisioning.

Mitigation: Require explicit approval before modifying openclaw.json, review backup file permissions, and remove bindings, workspaces, and backups manually when deprovisioning.

Risk: Browser automation and gateway restart can affect the user's active Telegram or OpenClaw session.

Mitigation: Confirm with the user before triggering browser automation or restarting the gateway, then verify that the updated configuration is applied.

## Reference(s):

- [Create Agent With Telegram Group on ClawHub](https://clawhub.ai/sheetaa/skills/create-agent-with-telegram-group)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown status summaries with shell commands and JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local OpenClaw configuration, workspace files, and Telegram group bindings after explicit user approval.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
