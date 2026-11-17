## Description: <br>
Calendar Reminder Paid helps teams aggregate multiple calendars, schedule progressive reminders, detect conflicts, synchronize availability, and generate calendar analytics reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Teams, assistants, and operations staff use this skill to coordinate Outlook-based team calendars, send Feishu or Telegram reminders, flag scheduling conflicts, and export weekly CSV reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connected calendars may contain sensitive personal or work details that could be shared with admins or Feishu or Telegram channels. <br>
Mitigation: Review exactly which calendars are connected and who receives notifications before installation; avoid sensitive calendars unless recipients and retention are tightly controlled. <br>
Risk: Recurring scans and weekly reports can repeatedly process and store calendar information. <br>
Mitigation: Enable the cron job and CSV report export only when recurring scans and reports are intended, and store reports in a controlled location. <br>
Risk: Team synchronization requires calendar access for team members. <br>
Mitigation: Confirm member authorization scope before enabling synchronization and prefer busy/free availability data where detailed event contents are not required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/calendar-reminder-paid) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Source skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with Python, Bash, JSON, text report, and CSV examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create scheduled reminders, messaging notifications, calendar reports, and CSV exports when executed by an agent with the required integrations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
