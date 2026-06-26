## Description: <br>
Weekly report generator that compiles progress from tasks, emails, and calendar activity into one summary for Friday cron or on-demand use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ceobotson-bot](https://clawhub.ai/user/ceobotson-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals, managers, and teams use this skill to compile weekly progress reports from configured task sources, calendars, and email accounts, covering wins, meetings, communications, blockers, metrics, and next-week priorities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weekly reports may expose sensitive task, email, meeting, client, or business details through selected inputs, delivery channels, or recipients. <br>
Mitigation: Limit the task source, inbox, calendars, archive folder, delivery channel, and recipients before use; review at least one report before enabling scheduled delivery. <br>
Risk: Shared Telegram or Discord delivery can disclose report contents to an audience that should not receive them. <br>
Mitigation: Use shared chat delivery only when the included client, email, meeting, and business details are appropriate for that audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ceobotson-bot/doctorclaw-weekly-report) <br>
- [DoctorClaw website](https://www.doctorclaw.ceo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown weekly report with optional scheduling, delivery, and archive guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use configured task, calendar, email, delivery channel, and archive sources when the user grants access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
