## Description:

Create and manage OpenClaw cron jobs following established conventions for periodic tasks, reminders, automated checks, and scheduled work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brennerspear](https://clawhub.ai/user/brennerspear)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to draft and manage OpenClaw cron job configurations for recurring checks, reminders, notifications, and maintenance tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated cron jobs may repeatedly send workspace data or task output to a fixed Telegram destination.

Mitigation: Review each cron job before enabling it, replace the Telegram target with a destination you control, and avoid sending secrets or private workspace data.

Risk: Recurring jobs created from this skill may continue running after their purpose or recipient changes.

Mitigation: Audit enabled cron jobs regularly and delete or disable jobs whose schedule, task message, or delivery target is no longer explicitly intended.

## Reference(s):

- [Cron Setup on ClawHub](https://clawhub.ai/brennerspear/skills/cron-setup)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON configuration examples and inline command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated cron job guidance should be reviewed before enabling recurring execution or external delivery.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
