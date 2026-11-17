## Description:

Production blueprint for orchestrating multiple OpenClaw agents via Feishu with file-driven task queues, cron scheduling, and workspace sandbox workarounds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evan966890](https://clawhub.ai/user/evan966890)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to configure an OpenClaw multi-agent workflow through Feishu bots, file-based task queues, cron-driven activity, and troubleshooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent cron jobs can continue running agents and sending Feishu-connected actions after initial setup.

Mitigation: Review each cron job before enabling it, set narrow schedules and timeouts, and document who can approve or disable recurring jobs.

Risk: The workflow uses shell commands to reach managed agent workspaces, which can bypass normal workspace isolation expectations.

Mitigation: Use a dedicated shared queue or broker with validation, producer identity, audit logs, and least-privilege filesystem permissions before production use.

Risk: Proactive user-facing Feishu messages may create consent, frequency, or content-control issues.

Mitigation: Define explicit consent, recipient scope, rate limits, and escalation rules for automated messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evan966890/skills/feishu-multi-agent)
- [Feishu Open Platform](https://open.feishu.cn)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with JSON, shell, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational checklists, troubleshooting guidance, and reusable SOUL.md and HEARTBEAT.md templates.]

## Skill Version(s):

1.0.0 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
