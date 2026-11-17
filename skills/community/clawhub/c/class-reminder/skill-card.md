## Description:

Class Reminder parses Excel course schedules, including teacher-style timetable layouts, and helps agents answer date-based class queries or generate reminder text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[judysue](https://clawhub.ai/user/judysue)

### License/Terms of Use:

MIT-0

## Use Case:

Students, instructors, and agents assisting them use this skill to parse uploaded Excel timetables, answer today/tomorrow/specific-date schedule questions, and produce daily or weekly reminder text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-provided course spreadsheets that may contain personal schedule information.

Mitigation: Use only intended schedule files and keep parsed schedule data in a controlled workspace.

Risk: Automated cron or heartbeat reminders can run on an unintended schedule or stale file path.

Mitigation: Review the schedule file path, semester start date, and cron or heartbeat trigger before enabling automation.

Risk: The skill depends on openpyxl for spreadsheet parsing.

Mitigation: Install dependencies in a virtual environment and pin openpyxl when deploying.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/judysue/skills/class-reminder)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON or plain-text reminder outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads user-provided Excel spreadsheets and may write parsed schedule data to data/schedule.json.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
