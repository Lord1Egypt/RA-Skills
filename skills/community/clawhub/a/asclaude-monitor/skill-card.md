## Description:

Monitors local system resources, OpenClaw gateway status, scheduled jobs, and background automation signals to help detect workflow issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miaoxingjun](https://clawhub.ai/user/miaoxingjun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to check local system health, inspect cron jobs, and monitor background automation status so workflow failures are easier to detect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Future Feishu or chat notification behavior could send cron names or task details to an unintended recipient or endpoint.

Mitigation: Confirm the notification recipient, endpoint, and exact status data before enabling notification behavior.

Risk: The helper reports local OpenClaw gateway and cron status, which may reveal operational details in shared outputs.

Mitigation: Review generated status output before sharing it outside the intended workspace or operations context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/miaoxingjun/skills/asclaude-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local command output from OpenClaw status and cron listing checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
