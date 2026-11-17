## Description:

Schedule OpenClaw tasks using natural language with cron lifecycle management, timezone support, failure alerts, and execution logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariusfit](https://clawhub.ai/user/mariusfit)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to schedule recurring agent tasks in plain English, inspect upcoming runs, manage job lifecycle state, and review execution logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled tasks run persistently through cron and may repeatedly perform actions such as reading email, calling APIs, writing memory files, deleting logs, or archiving data.

Mitigation: Review each task before scheduling it, keep high-impact actions narrow, and use logs plus pause or remove commands to stop unwanted jobs.

Risk: Failure alerts sent through WhatsApp or Telegram may disclose job names, timing, or error details to the configured provider or recipient.

Mitigation: Enable alert channels only for acceptable recipients and avoid putting sensitive data in job names or task descriptions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mariusfit/skills/clawhub-skill-smart-cron)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local cron scheduling instructions, job lifecycle commands, alert configuration, and log review guidance for OpenClaw tasks.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
