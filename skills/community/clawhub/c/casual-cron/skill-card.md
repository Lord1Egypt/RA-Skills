## Description: <br>
Create Clawdbot cron jobs from natural language with strict run-guard rules for one-shot and recurring reminders or messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gostlightai](https://clawhub.ai/user/gostlightai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to have an agent convert natural language reminder requests into OpenClaw cron jobs for delivery through configured channels such as Telegram, Slack, Discord, WhatsApp, or Signal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled messages are delivered through external channels and may contain incorrect recipients, message text, recurrence, or one-shot cleanup settings. <br>
Mitigation: Confirm the timezone, recipient, message text, recurrence, and delete-after-run behavior before finalizing a job. <br>
Risk: Clock-time schedules default to America/New_York, which may not match the user's intended timezone. <br>
Mitigation: Ask users outside America/New_York to confirm the intended timezone or convert the schedule before creating the cron job. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gostlightai/casual-cron) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with OpenClaw cron command examples and confirmations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and openclaw; CRON_DEFAULT_CHANNEL can override the default delivery channel.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
