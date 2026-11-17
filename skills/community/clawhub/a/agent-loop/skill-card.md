## Description:

Agent Loop gives agents a structured Read, Plan, Execute, Verify, Report protocol for tasks with side effects, reducing false completion reports, blind retries, and scope creep.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cycy2xxx](https://clawhub.ai/user/cycy2xxx)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to make agents follow a disciplined execution loop before file edits, shell commands, multi-step work, or irreversible actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task plans and progress notes may contain sensitive details when the skill is paired with agent-task-tracker.

Mitigation: Avoid putting secrets or sensitive data into saved plans and progress notes.

Risk: The workflow can still produce incorrect or misleading guidance if an agent follows an unsound plan.

Mitigation: Review planned actions before execution and verify outcomes with concrete evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cycy2xxx/skills/agent-loop)
- [Publisher profile](https://clawhub.ai/user/cycy2xxx)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with plans, verification notes, and concise task reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save task plans and progress notes when paired with agent-task-tracker.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
