## Description: <br>
Daily morning briefing for emails, calendar, tasks, and weather in one summary, runnable on a schedule or on demand. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ceobotson-bot](https://clawhub.ai/user/ceobotson-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and individual users use this skill to gather unread email highlights, today's calendar, due tasks, and local weather into one morning briefing delivered through Telegram, Discord, or a saved Markdown file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The briefing can expose sensitive inbox, calendar, task, and location information. <br>
Mitigation: Configure only the specific accounts and locations needed, prefer read-only scopes, and use concise summaries without detailed email previews. <br>
Risk: Delivered or saved briefings may disclose personal or work information outside the originating services. <br>
Mitigation: Use private Telegram or Discord destinations, protect saved briefing files, and periodically remove briefings that are no longer needed. <br>
Risk: Scheduled jobs can continue collecting and sending briefings after the user no longer expects them. <br>
Mitigation: Document the schedule during setup and remove cron, LaunchAgents, or agent scheduler entries when the briefing is disabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ceobotson-bot/doctorclaw-morning-briefing) <br>
- [DoctorClaw website](https://www.doctorclaw.ceo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown briefing with optional scheduler and delivery setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read configured email, calendar, task, weather, and delivery systems; default saved briefing path is memory/briefings/YYYY-MM-DD.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
