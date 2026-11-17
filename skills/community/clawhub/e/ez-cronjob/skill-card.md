## Description:

Fix common cron job failures in Clawdbot/Moltbot - message delivery issues, tool timeouts, timezone bugs, and model fallback problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[promadgenius](https://clawhub.ai/user/promadgenius)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to diagnose Clawdbot/Moltbot cron job failures, create more reliable scheduled messages, and apply safe troubleshooting steps for delivery, timezone, timeout, and fallback-model issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cron job deletion, immediate runs, or gateway restarts can remove scheduled work, send messages unexpectedly, or briefly disrupt service.

Mitigation: Verify the job ID, target service, and intended action with the user before running destructive, immediate-execution, or restart commands.

Risk: Telegram delivery commands can send scheduled messages to the wrong chat or channel.

Mitigation: Confirm the destination channel and chat ID before creating or testing delivery-enabled jobs.

Risk: Log inspection can expose local operational data.

Mitigation: Limit log review to cron-relevant lines and avoid sharing unrelated local log contents.

## Reference(s):

- [Clawdbot Cron Documentation](https://docs.molt.bot/tools/cron)
- [Timezone Database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
- [Cron Expression Generator](https://crontab.guru/)
- [EZ Cronjob ClawHub Page](https://clawhub.ai/promadgenius/skills/ez-cronjob)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
