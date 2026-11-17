## Description:

Monitors the AWS Health Dashboard for active incidents and sends configurable notifications through Feishu, Telegram, Slack, Discord, or similar channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shimotsuk1-rei](https://clawhub.ai/user/shimotsuk1-rei)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to monitor AWS regional service health, configure filters for watched regions or services, and receive outage updates through an existing notification channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A misconfigured notification target can send AWS outage messages to the wrong channel or recipient.

Mitigation: Set AWS_HEALTH_NOTIFY_TARGET carefully and verify the destination before enabling scheduled polling.

Risk: Broad monitoring or cron scheduling can create unwanted recurring outbound requests and notifications.

Mitigation: Use AWS_HEALTH_WATCH_REGIONS and AWS_HEALTH_WATCH_SERVICES filters, and add the cron entry only when continuous polling is intended.

## Reference(s):

- [AWS Health public current events endpoint](https://health.aws.amazon.com/public/currentevents)
- [AWS Health status dashboard](https://health.aws.amazon.com/health/status)
- [AWS Health ignore configuration example](references/aws-health-ignore.example.json)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Notifications are sent only when new incidents, changed incident messages, or resolved incidents are detected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
