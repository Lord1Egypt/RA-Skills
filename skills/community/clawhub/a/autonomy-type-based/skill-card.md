## Description:

Type-Based Autonomy guides an agent to pull from a tagged task queue and work only on research, writing, and analysis tasks while scheduled processes handle maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luciusrockwing](https://clawhub.ai/user/luciusrockwing)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to structure autonomous work around typed task queues, focusing agent effort on research, writing, and analysis while leaving maintenance, backup, and security tasks to scheduled processes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow writes task, memory, goal, and learning notes that may persist sensitive workspace context.

Mitigation: Use the skill only in workspaces intended for autonomous tracking, and keep checkpoints and learning notes free of secrets, credentials, and sensitive personal information.

Risk: Ambiguous or poorly tagged tasks can cause the agent to pick work outside the intended autonomy scope.

Mitigation: Keep queued tasks specific, require explicit type labels, and review the ready queue before enabling autonomous heartbeat runs.

Risk: Completed task history can accumulate operational details that should not be retained indefinitely.

Mitigation: Archive completed tasks only when history is needed, and routinely clear or prune done items according to workspace retention expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luciusrockwing/skills/autonomy-type-based)
- [Publisher profile](https://clawhub.ai/user/luciusrockwing)
- [Checkpoint formats](references/checkpoints.md)
- [Queue template](templates/QUEUE.md)
- [Heartbeat template](templates/HEARTBEAT.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration]

**Output Format:** [Markdown instructions and templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces task queue structure, heartbeat procedure, checkpoint formats, and guidance for autonomous task selection.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
