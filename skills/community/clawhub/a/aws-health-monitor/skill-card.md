## Description: <br>
Monitors AWS Health Dashboard for active incidents and sends configurable notifications through Feishu, Telegram, Slack, Discord, and similar channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shimotsuk1-Rei](https://clawhub.ai/user/Shimotsuk1-Rei) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations teams use this skill to monitor active AWS Health incidents, filter watched regions and services, and configure outbound incident notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default watch scope can include all AWS regions and services, creating noisy or unwanted notifications. <br>
Mitigation: Set AWS_HEALTH_WATCH_REGIONS and AWS_HEALTH_WATCH_SERVICES to the intended monitoring scope before enabling recurring checks. <br>
Risk: Incident notifications are sent to the configured external channel and target. <br>
Mitigation: Set AWS_HEALTH_NOTIFY_CHANNEL and AWS_HEALTH_NOTIFY_TARGET deliberately, and verify the recipient before running the monitor. <br>
Risk: Adding the cron entry enables recurring network checks and repeated outbound notifications. <br>
Mitigation: Only add the cron entry when continuous monitoring is desired, and review the local state file and log path during operation. <br>


## Reference(s): <br>
- [AWS Health status page](https://health.aws.amazon.com/health/status) <br>
- [AWS Health current events endpoint](https://health.aws.amazon.com/public/currentevents) <br>
- [aws-health-ignore.example.json](references/aws-health-ignore.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces monitoring setup guidance and notification message content; the script records local state and sends configured outbound notifications.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
