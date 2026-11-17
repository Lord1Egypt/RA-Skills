## Description:

Farm Task Manager helps farmers organize daily, weekly, and seasonal chores with task scheduling, priorities, status tracking, recurring tasks, filtering, and export options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johstracke](https://clawhub.ai/user/johstracke)

### License/Terms of Use:


## Use Case:

Farmers, homesteaders, and farm operators use this skill to track chores, assign responsibilities, manage recurring work, and export task plans for sharing or backup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The export command can overwrite arbitrary writable files in the user's home directory.

Mitigation: Export only to a dedicated task export folder and avoid pointing exports at existing files until path validation and overwrite behavior are fixed.

## Reference(s):

- [Farm Task Manager on ClawHub](https://clawhub.ai/johstracke/skills/farm-task-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and JSON or Markdown task exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores task data as JSON and can export filtered task lists as Markdown or JSON.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
