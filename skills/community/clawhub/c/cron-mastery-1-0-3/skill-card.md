## Description: <br>
Master OpenClaw's timing systems. Use for scheduling reliable reminders, setting up periodic maintenance (janitor jobs), and understanding when to use Cron vs Heartbeat for time-sensitive tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wt865143010](https://clawhub.ai/user/wt865143010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to choose reliable OpenClaw scheduling patterns for reminders, recurring jobs, cleanup tasks, and timezone-sensitive automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example reminder payloads include a hard-coded Telegram recipient. <br>
Mitigation: Replace example delivery destinations with channels and recipients controlled by the user before scheduling notifications. <br>
Risk: Recurring summaries may access mailbox contents or send email-derived content to third-party delivery channels. <br>
Mitigation: Schedule email summaries only after explicit user consent for mailbox access and the selected delivery channel. <br>
Risk: Manual cron state-file deletion can remove active reminders or damage scheduler state. <br>
Mitigation: Back up scheduler state and prefer normal job listing and deletion workflows before deleting cron state files manually. <br>


## Reference(s): <br>
- [Cron Examples & Templates](references/templates.md) <br>
- [ClawHub release page](https://clawhub.ai/wt865143010/cron-mastery-1-0-3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces scheduling recommendations and example cron job payloads; does not execute jobs by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
