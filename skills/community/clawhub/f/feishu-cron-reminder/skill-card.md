## Description: <br>
Creates and manages scheduled Feishu reminder jobs in OpenClaw for one-time and recurring messages to users or groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzqsama066](https://clawhub.ai/user/zzqsama066) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to convert natural-language Feishu reminder requests into cron jobs for meetings, daily routines, workday reminders, weekly reminders, and group notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A reminder may be sent to the wrong Feishu user or group if the recipient ID is incorrect. <br>
Mitigation: Verify each user:ou_ or channel:oc_ recipient before approving the cron job, especially for group notifications. <br>
Risk: Timezone or recurrence mistakes can trigger reminders at unintended times or continue longer than expected. <br>
Mitigation: Confirm the timezone, UTC conversion for one-time jobs, cron expression, and recurrence before creating the job. <br>
Risk: Recurring reminders can retain sensitive message text or become stale over time. <br>
Mitigation: Keep reminder text minimal, review old recurring jobs periodically, and remove reminders that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zzqsama066/feishu-cron-reminder) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with OpenClaw cron command examples and Feishu recipient configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OpenClaw cron commands using Feishu delivery targets, timezone settings, recurrence rules, and optional one-time cleanup.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
