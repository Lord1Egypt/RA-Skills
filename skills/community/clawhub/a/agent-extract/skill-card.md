## Description:

Agent Extract helps separate a feature or skill from the main OpenClaw agent into an isolated agent with its own session, workspace, memory, identity files, and heartbeat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kings0527](https://clawhub.ai/user/kings0527)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to split a feature or skill into a dedicated agent while preserving the original main agent workspace, sessions, channels, identity, and memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a second persistent agent with a recurring heartbeat.

Mitigation: Set an expiration or removal plan for the heartbeat and periodically review whether the new agent still needs to run.

Risk: The skill may copy identity and memory files too broadly into the new workspace.

Mitigation: Approve each copied file explicitly and avoid copying unrelated memories or identity material.

Risk: The rollback guidance includes deleting the created workspace.

Mitigation: Use a validated backup or quarantine workflow before removal instead of relying on immediate recursive deletion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kings0527/skills/agent-extract)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a verification shell script for checking the created agent, workspace, cron job, channel configuration, and copied files.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact/skill.json declares 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
