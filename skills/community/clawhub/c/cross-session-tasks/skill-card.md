## Description:

Provides a file-based task management pattern that helps an AI agent resume work across sessions, channels, or threads using active-task, closed-task, and per-project progress Markdown files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imchongliu](https://clawhub.ai/user/imchongliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to set up Markdown task indexes and progress notes so agents can continue ongoing work after a session, channel, or thread changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task notes can persist sensitive project details across sessions if users place them in ACTIVE-TASKS.md or project progress files.

Mitigation: Store only necessary non-secret task context in the Markdown files, and avoid credentials, private personal data, or sensitive customer details.

Risk: Adding recurring task-management rules to AGENTS.md changes how an agent checks and updates local workspace files across sessions.

Mitigation: Review the AGENTS.md changes before installation and keep the persistence behavior limited to the intended workspace and task files.

## Reference(s):

- [Cross-Session Task Manager ClawHub Page](https://clawhub.ai/imchongliu/skills/cross-session-tasks)
- [Skill Instructions](artifact/SKILL.md)
- [ACTIVE-TASKS Template](artifact/templates/ACTIVE-TASKS.md)
- [CLOSED-TASKS Template](artifact/templates/CLOSED-TASKS.md)
- [Progress Template](artifact/templates/progress.md)
- [Example Progress File](artifact/examples/example-progress.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command snippets, task templates, and configuration rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local Markdown task files and AGENTS.md rule changes; server security evidence reports no network access, credential handling, hidden code, or destructive behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
