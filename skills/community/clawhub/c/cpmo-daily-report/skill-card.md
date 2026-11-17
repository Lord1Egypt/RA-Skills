## Description:

Generates Chinese-language CPMO morning reports and evening summaries by querying Apple Notes, macOS Calendar, reminders, local ledgers, and Feishu records for current project status, risks, and todos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayangai](https://clawhub.ai/user/ayangai)

### License/Terms of Use:

MIT-0

## Use Case:

Product operations and CPMO users use this skill to prepare daily project reports, summarize progress, track risks, and monitor todos from live personal and work data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read broad personal and work data from Notes, calendars, reminders, and local ledgers.

Mitigation: Scope access to the intended Notes folder, calendar names, reminders lists, and local ledger files before enabling the workflow.

Risk: The skill can write or synchronize summaries to Feishu and Apple Notes.

Mitigation: Confirm the Feishu destination and require review before any Notes or Feishu write-back.

Risk: Scheduled cron execution can run the workflow automatically.

Mitigation: Enable the morning and evening schedules only after confirming timing, data access, and review requirements.

## Reference(s):

- [Artifact skill definition](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/ayangai/skills/cpmo-daily-report)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with shell command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated from live queries and may include Feishu synchronization status.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
