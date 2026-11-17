## Description:

Clawlist provides an opinionated workflow for planning, executing, tracking, and verifying multi-step, long-running, and ongoing agent tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arisylafeta](https://clawhub.ai/user/arisylafeta)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to structure projects, ongoing monitoring, parallel work, and completion checks across planning, execution, and verification phases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger language may cause the skill to steer too many agent interactions.

Mitigation: Review or narrow its triggers before deployment so it activates only for intended task-management workflows.

Risk: The workflow can create ongoing or persistent task state without clear opt-in.

Mitigation: Require explicit approval before saving project details, creating recurring tasks, or updating memory/tasks/ongoing-tasks.md.

Risk: Parallel-agent dispatch can expand scope or share task context unexpectedly.

Mitigation: Require confirmation before dispatching subagents and provide each subagent with a bounded scope and constraints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arisylafeta/skills/clawlist)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, plans, checklists, status summaries, and proposed commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update task-tracking files such as memory/tasks/ongoing-tasks.md for long-running work.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
