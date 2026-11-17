## Description:

Aligns a Claude Pro/Max usage window to working hours by guiding setup of an opt-in scheduled primer through the official Claude Code CLI on an always-on machine, without increasing quota.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daryn-louw](https://clawhub.ai/user/daryn-louw)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and Claude Pro/Max subscribers use this skill to configure, preview, and schedule a low-volume CLI primer so Claude usage windows line up with their working day. It is intended for users who already run an authenticated official Claude Code CLI on an always-on VPS or similar host.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring scheduled jobs may repeatedly invoke an authenticated Claude CLI on the user's host.

Mitigation: Review every generated crontab or scheduled-task line before installing it, keep the schedule low-volume, and document how to remove the entries.

Risk: Cron entries are generated from user-editable configuration.

Mitigation: Keep config.json trusted and simple, avoid piping generated output directly into crontab, and inspect the exact commands before activation.

Risk: Misuse could be framed as bypassing limits or could involve unsafe credential handling.

Mitigation: Use only the official Claude Code CLI logged in on the same machine, do not copy tokens or use shared accounts, and describe the behavior as usage-window alignment rather than quota bypass.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daryn-louw/skills/claude-session-warmer)
- [Project website](https://decisionvex.github.io/claude-session-warmer/)
- [Terms-of-service position](references/tos.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce cron entries and scheduled-task commands for user review before installation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
