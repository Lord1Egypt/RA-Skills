## Description:

Deep Planner helps agents handle complex tasks by creating a visible step-by-step plan, persisting progress locally, coordinating domain skills, and prompting for confirmation at critical decision points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jzw6](https://clawhub.ai/user/jzw6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to structure complex, multi-step work into visible plans, persisted progress records, and checkpointed execution before delegating to domain-specific tools or skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plans, assumptions, filenames, and progress notes may be saved under .todolist/, which can expose sensitive prompt details on the local filesystem.

Mitigation: Use the skill only when local persistence is acceptable, and avoid including sensitive details in persisted plans.

Risk: Structured plans can carry incorrect assumptions or outdated claims into downstream work if critical details are not checked.

Mitigation: Review assumptions at decision points and verify time-sensitive or sourced claims before relying on the plan.

## Reference(s):

- [Task Type Templates](references/task-types.md)
- [Deep Planner ClawHub Page](https://clawhub.ai/jzw6/skills/deep-planner)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown task plans, progress updates, and persisted .todolist Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans and progress notes may be persisted locally under .todolist/.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
