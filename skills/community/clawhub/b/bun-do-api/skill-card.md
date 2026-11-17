## Description:

Manage bun-do tasks and projects by adding, editing, deleting, marking done, managing subtasks, and logging project progress entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricardofrantz](https://clawhub.ai/user/ricardofrantz)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to manage local-first bun-do task and project data through the bun-do REST API, including deadlines, reminders, recurring payments, subtasks, and project progress logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify or delete persistent local task, project, and payment-tracking records.

Mitigation: Require explicit user confirmation before delete, clear-done, mark-done, and autonomous progress-logging actions.

Risk: Broad task-management triggers may cause the skill to act on important personal, project, or bill-tracking data.

Mitigation: Review intended actions before execution and prefer a pinned local installation without elevated privileges.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose REST API calls that create, update, mark done, or delete local task and project records.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
