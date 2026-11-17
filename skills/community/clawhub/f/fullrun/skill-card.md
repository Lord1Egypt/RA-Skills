## Description:

Automatically execute tasks from checklist.md with state management and scheduled checking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lightconsen](https://clawhub.ai/user/lightconsen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill in Claude Code projects to run checklist.md task queues with local state tracking, scheduled checks, and resumable execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer adds a Claude Code SessionStart hook that can start monitoring automatically in a project.

Mitigation: Inspect .claude/settings.local.json after installation and remove or disable the fullrun SessionStart hook unless automatic monitoring is intended.

Risk: Checklist entries can drive agent work in the current project.

Mitigation: Use the skill only in repositories where checklist.md is trusted and review pending tasks before running or enabling monitoring.

Risk: Installation grants broad permission for the copied project-local fullrun shell scripts.

Mitigation: Review the generated permission rule in .claude/settings.local.json and install only in projects where those scripts are expected to run.

Risk: Uninstall may remove or alter local Claude settings when cleaning up fullrun configuration.

Mitigation: Inspect or back up .claude/settings.local.json before uninstalling, especially in projects with other local Claude hooks or permissions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash commands and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates project-local state, log, PID, and Claude settings files during installation and execution.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
