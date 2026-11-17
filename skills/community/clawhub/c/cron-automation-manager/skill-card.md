## Description:

Manage scheduled cron jobs, automated monitoring tasks, reminders, periodic reports, and push notifications for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mr-chen-05](https://clawhub.ai/user/mr-chen-05)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external OpenClaw users use this skill to create, inspect, modify, and delete recurring cron-based automation workflows. It is suited for monitoring pipelines, daily or weekly reports, reminders, price alerts, GitHub tracking, AI news monitoring, and notification routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and manage persistent cron jobs.

Mitigation: Require explicit user confirmation before creating, modifying, or deleting jobs, and maintain clear rules for which recurring jobs are allowed.

Risk: Automation outputs are written to mandatory local intelligence logs.

Mitigation: Define retention and redaction practices for intel/daily files and avoid logging secrets, private content, or credentials.

Risk: External delivery channels can send generated reports outside the local workspace.

Mitigation: Keep external channels disabled by default and enable only the specific channels with configured, authorized credentials.

## Reference(s):

- [Cron Automation Manager README](artifact/README.md)
- [Cron Automation Manager Skill](artifact/SKILL.md)
- [Delivery Configuration Example](artifact/config/delivery-config.example.json)
- [ClawHub Skill Page](https://clawhub.ai/mr-chen-05/skills/cron-automation-manager)
- [ClawHub Publisher Profile](https://clawhub.ai/user/mr-chen-05)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with cron expressions, configuration snippets, and structured task summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent local intelligence logs and route generated reports through configured delivery channels.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
