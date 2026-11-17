## Description:

Control spawned Feishu background tasks with concise natural-language or slash-command workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wd041216-bit](https://clawhub.ai/user/wd041216-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Feishu chat users and agents use this skill to inspect running child tasks, stop a specific background task, or clean up all active background tasks in the current chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad stop-all or /stop request can cancel useful in-progress work.

Mitigation: Prefer stopping a specific task by id, label, or summary when the user intent is narrower than ending all active work.

Risk: An ambiguous natural-language target can stop the wrong background task.

Mitigation: List matching active tasks and ask the user to choose before stopping a task when the target cannot be resolved confidently.

## Reference(s):

- [OpenClaw command documentation](https://docs.openclaw.ai/commands)
- [ClawHub skill page](https://clawhub.ai/wd041216-bit/skills/feishu-task-control)

## Skill Output:

**Output Type(s):** [Guidance, Slash commands, Text]

**Output Format:** [Concise natural-language replies with slash-command guidance when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No files or persistent outputs are produced by the skill.]

## Skill Version(s):

1.0.1 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
