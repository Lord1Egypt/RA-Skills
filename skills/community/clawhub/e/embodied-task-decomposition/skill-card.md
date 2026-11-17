## Description:

Decomposes complex physical tasks from an image and natural language instruction into atomic subtasks for robot execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanaoisong](https://clawhub.ai/user/nanaoisong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics practitioners use this skill to convert scene images plus high-level task instructions into sequential, gripper-specific robot subtasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Action-bank changes can persistently expand the robot action vocabulary without explicit approval.

Mitigation: Require explicit approval, inspect proposed diffs, and avoid allowing routine decomposition requests to silently modify action definitions.

## Reference(s):

- [Atomic Action Bank](references/action-bank.md)
- [Task Decomposition Examples](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/nanaoisong/skills/embodied-task-decomposition)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown numbered lists with optional action-bank entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Subtasks use an action, target, optional location, and left/right/either gripper specification.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
