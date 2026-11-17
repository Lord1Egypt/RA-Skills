## Description:

Create, edit, delete and toggle Dumb Panel cron tasks via its HTTP API, when ddp.exe has no command or a daidai.db edit won't load.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c0s1n3](https://clawhub.ai/user/c0s1n3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use this skill to create, update, enable, disable, run, stop, and delete Dumb Panel scheduled tasks through the panel API when ddp.exe lacks those controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The task manager borrows a panel user's identity and permits authenticated actions beyond task management.

Mitigation: Review before using it on a live panel. Use an explicitly authorized account, restrict raw requests to task endpoints, and reject expired sessions.

## Reference(s):

- [Dumb Panel Task API Reference](references/api_reference.md)
- [Dumb Panel Task CLI on ClawHub](https://clawhub.ai/c0s1n3/skills/daidai-panel-task-crud)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Python CLI commands and task API requests, with JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task operations can change scheduled jobs on the panel.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
