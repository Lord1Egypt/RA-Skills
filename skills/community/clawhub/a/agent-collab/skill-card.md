## Description:

Multi-agent collaboration framework for OpenClaw that defines Dispatch, Collaborate, and Direct Chat workflows with organization hierarchy, HANDOFF file exchange, and scope-isolated memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylin19860916](https://clawhub.ai/user/kylin19860916)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams configuring OpenClaw multi-agent deployments use this skill to route one-shot tasks, persistent cross-agent collaboration, and direct department-specific conversations while coordinating handoffs across workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad session visibility and cross-workspace handoffs can expose or propagate sensitive context across agents.

Mitigation: Narrow session visibility where possible, avoid sensitive data in handoffs, and require confirmation before spawning sessions or writing HANDOFF files.

Risk: Deleting a received HANDOFF file can remove the only copy of task context or results.

Mitigation: Archive the handoff or log receipt before removing the active file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kylin19860916/skills/agent-collab)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OpenClaw session, subagent, workspace, and HANDOFF conventions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
