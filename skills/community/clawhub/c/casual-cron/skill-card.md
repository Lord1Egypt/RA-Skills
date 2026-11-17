## Description:

Casual Cron helps agents turn natural-language reminder requests into OpenClaw cron commands for one-shot or recurring delivered messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gostlightai](https://clawhub.ai/user/gostlightai)

### License/Terms of Use:


## Use Case:

External users and developers use Casual Cron to schedule reminders or messages through OpenClaw-supported delivery channels such as Telegram, WhatsApp, Slack, Discord, and Signal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create scheduled messages that continue running until removed.

Mitigation: Review each parsed schedule, recurrence, destination, and delivery channel before approving execution; use one-shot jobs with delete-after-run when the reminder should not recur.

Risk: A parsed time, channel, or destination may not match the user's intent.

Mitigation: Confirm the parsed time, job name, job id, channel, and destination before finalizing the cron job.

Risk: Default channel configuration can route a reminder to an unintended delivery channel.

Mitigation: Verify CRON_DEFAULT_CHANNEL and explicit channel mentions before creating the OpenClaw cron command.

## Reference(s):

- [Casual Cron on ClawHub](https://clawhub.ai/gostlightai/skills/casual-cron)
- [Publisher profile: gostlightai](https://clawhub.ai/user/gostlightai)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; helper script output is JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and openclaw; CRON_DEFAULT_CHANNEL can set the default delivery channel.]

## Skill Version(s):

1.2.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
