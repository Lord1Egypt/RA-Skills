## Description:

Automatically scans and cleans completed C tasks weekly, compressing selected insights into MEMORY.md and generating cleanup reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[largetool](https://clawhub.ai/user/largetool)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users of the documented Chinese C-task workflow use this skill to periodically clear completed C-class tasks, preserve selected insights, and keep a cleanup report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled cleanup may remove completed C-task entries before a user has reviewed them.

Mitigation: Run the skill manually first, keep backups, and review cleanup reports before enabling the weekly cron schedule.

Risk: The skill assumes the documented Chinese C-task workflow and local task and memory paths.

Mitigation: Install it only for that workflow and confirm the target files and paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/largetool/skills/c-task-cleanup)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown files and terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Updates a memory markdown file and writes a dated cleanup report.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
