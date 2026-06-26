## Description: <br>
Generates a daily brief including urgent emails, upcoming calendar events, tasks, and relevant news when the user asks for a morning summary, daily briefing, or status update on their day. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RajTejani61](https://clawhub.ai/user/RajTejani61) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to collect recent email, calendar, task, and news signals into a daily briefing. It can also be scheduled as an OpenClaw cron task that saves a local report and sends a short notification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read private email, calendar, and task data through locally configured tools. <br>
Mitigation: Use limited accounts or profiles where possible and review the configured email, calendar, and task tool access before enabling the skill. <br>
Risk: The skill can keep permanent local copies of daily reports that may contain sensitive personal or work information. <br>
Mitigation: Protect or periodically delete ~/.openclaw/cron/DailyDigest_logs/ if retained reports should not be kept. <br>
Risk: Scheduled runs can send summaries to the active messaging channel. <br>
Mitigation: Confirm the notification destination before enabling cron automation. <br>


## Reference(s): <br>
- [Setting Up the Daily Digest Cron Job](references/cron-guide.md) <br>
- [Daily Digest Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown report with embedded HTML plus a short notification summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save daily reports under ~/.openclaw/cron/DailyDigest_logs/ when the included digest script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
