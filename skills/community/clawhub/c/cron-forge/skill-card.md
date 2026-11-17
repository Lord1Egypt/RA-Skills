## Description:

Human-readable cron job templates for OpenClaw provide pre-built schedules for daily reports, hourly checks, weekly summaries, and custom intervals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to choose plain-English cron schedules and adapt them into OpenClaw cron jobs for recurring summaries, monitoring, reporting, and other routine automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A scheduled prompt could read private data, inspect systems, or post content publicly if added without review.

Mitigation: Review each cron prompt before adding it and use isolated sessions where appropriate.

Risk: Active cron jobs can continue running after they are no longer needed.

Mitigation: Periodically list active crons and remove jobs that are no longer needed.

Risk: An incorrect cron expression can run at an unintended time or frequency.

Mitigation: Review the plain-English schedule and test cron expressions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/cron-forge)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [crontab.guru](https://crontab.guru)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with cron expressions and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes plain-English schedule descriptions and OpenClaw cron command examples.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
