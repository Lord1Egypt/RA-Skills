## Description:

Employee Reminder Ops helps internal operations teams set up Google Sheets-driven birthday reminders, special-event reports, chat routing, and scheduled daily reporting jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vt-mmm](https://clawhub.ai/user/vt-mmm)

### License/Terms of Use:

MIT-0

## Use Case:

Internal operations teams use this skill to configure and run Google Sheets based birthday and special-event reminders, then preview or send daily reports to approved Telegram or Discord destinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled scripts can post employee reminder data to a default Discord channel when send or prod-send modes are used.

Mitigation: Replace bundled spreadsheet, account, and Discord channel defaults with explicit local configuration and use a test channel before enabling production sends.

Risk: Scheduled production sends can disclose employee birthday and event data to an unapproved destination.

Mitigation: Enable scheduled prod-send only after confirming the destination audience is approved for employee birthday and event data.

Risk: Broad local environment sourcing or unnecessary Drive authorization can increase credential exposure.

Mitigation: Keep tokens outside the skill package, avoid broad .env sourcing where possible, and remove unnecessary Drive authorization.

## Reference(s):

- [Employee Reminder Ops](artifact/SKILL.md)
- [Plan A Architecture](artifact/references/architecture.md)
- [Employee Reminder Ops Deployment](artifact/references/deployment.md)
- [Google Sheet Schema for Employee Reminder Ops](artifact/references/google-sheet-schema.md)
- [Employee Reminder Ops Troubleshooting](artifact/references/troubleshooting.md)
- [Plan A Deep Test Plan](artifact/references/PLAN_A_TEST.md)
- [Plan A Demo Usage](artifact/references/PLAN_A_DEMO_USAGE.md)
- [Employee Reminder Ops on macOS](artifact/references/macos.md)
- [Employee Reminder Ops on Windows](artifact/references/windows.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, JavaScript workflow scripts, text reports, and JSON previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime execution depends on local Google Sheets access, chat destination configuration, and scheduler setup.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
