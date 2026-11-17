## Description:

Manage a team of AI sub-agents organized into departments for delegating tasks, tracking outputs, assigning roles, and coordinating multi-agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trypto1019](https://clawhub.ai/user/trypto1019)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to organize AI workers into departments, assign and complete tasks, review active work, and generate department reports for complex projects or autonomous-business workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task descriptions and completion outputs are persisted on local disk and may contain sensitive workflow details if users enter them.

Mitigation: Avoid entering secrets or sensitive business data unless local persistence in ~/.openclaw/department-manager/departments.json is acceptable; use the data directory override when isolation is needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/trypto1019/skills/arc-department-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores department and task data locally in ~/.openclaw/department-manager/departments.json unless a data directory override is supplied.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
