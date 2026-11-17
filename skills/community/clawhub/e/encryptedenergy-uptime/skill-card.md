## Description:

Know the second your OpenClaw agent goes silent with a hosted heartbeat monitor that posts OpenClaw health data once a minute and sends alerts when pings stop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmarbach](https://clawhub.ai/user/jmarbach)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor an OpenClaw agent from Encrypted Energy by installing a local cron heartbeat that reports health and status data and triggers hosted email/status-page alerts when the agent stops pinging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a persistent cron job that runs under the user's account every minute.

Mitigation: Review the cron entry before installation, avoid duplicate entries, and document a removal command for users who uninstall or rotate monitoring setup.

Risk: The heartbeat sends detailed OpenClaw operational telemetry to a hosted third-party service.

Mitigation: Use only when this telemetry sharing is acceptable, prefer minimal heartbeat payloads where possible, and review exactly what health and status fields are included.

Risk: The bearer token is shown in the crontab example and may be stored directly in the user's crontab.

Mitigation: Store the token with restrictive permissions outside crontab or rotate it if exposed, and avoid sharing crontab contents in logs or support requests.

## Reference(s):

- [Encrypted Energy homepage](https://encryptedenergy.com)
- [Encrypted Energy agent registration](https://encryptedenergy.com/agents/new)
- [ClawHub skill listing](https://clawhub.ai/jmarbach/skills/encryptedenergy-uptime)
- [Publisher profile](https://clawhub.ai/user/jmarbach)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown instructions with shell commands and environment variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ENCRYPTED_ENERGY_API_KEY, cron, bash, curl, jq, and the openclaw CLI.]

## Skill Version(s):

0.2.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
