## Description: <br>
EduClaw is a personal IELTS study-planning skill that creates detailed study plans, schedules sessions on Google Calendar through gcalcli, and manages study materials and progress tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moclaw](https://clawhub.ai/user/moclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners and agents use this skill to plan IELTS preparation, discover study materials, schedule approved sessions, and maintain progress records across calendar, Markdown, and SQLite tracking surfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs Google Calendar access through gcalcli and may create or inspect study events. <br>
Mitigation: Use a dedicated Google OAuth client where possible, review requested scopes, and approve calendar changes only after inspecting the proposed schedule. <br>
Risk: Required API and bot tokens could expose calendar, model, search, or notification access if shared. <br>
Mitigation: Store tokens outside shared files and source control, rotate them if exposed, and use least-privilege projects or bots. <br>
Risk: Discord or Telegram reminders and reports may reveal personal study schedule or progress details. <br>
Mitigation: Send notifications only to private channels or chats and disable notification integrations that are not needed. <br>
Risk: Cron jobs can repeatedly send reminders, query local progress data, or refresh study materials. <br>
Mitigation: Enable only desired cron jobs, review their schedules and channels, and keep the local SQLite tracker in the intended workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/moclaw/educlaw-ielts-planner) <br>
- [README](artifact/README.md) <br>
- [Setup guide](artifact/SETUP.md) <br>
- [Workflow guide](artifact/WORKFLOW.md) <br>
- [SQLite tracker schema](artifact/schema.sql) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown responses with inline shell commands, calendar-event details, setup guidance, and study-plan documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Google Calendar study events, a Markdown study plan, and a local SQLite progress tracker when the user approves those actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
