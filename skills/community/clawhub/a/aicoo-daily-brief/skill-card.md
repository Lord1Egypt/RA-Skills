## Description:

Generates an executive daily brief from Aicoo context, then derives top COO strategies and an Eisenhower matrix view.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xisen-w](https://clawhub.ai/user/xisen-w)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to request a concise daily briefing from Aicoo, identify top strategic priorities, and organize urgent and important work into an Eisenhower matrix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Daily briefing content may include notes, calendar, tasks, or email-derived summaries sent to Aicoo as a third-party processor.

Mitigation: Use only with approved Aicoo data sharing, avoid sensitive content unless authorized, and review generated summaries before acting on them.

Risk: Recurring /loop, /routine, or cron setup can trigger automatic repeated API calls.

Mitigation: Enable scheduling only intentionally, review cadence and logging, and disable recurring jobs when no longer needed.

## Reference(s):

- [Aicoo API base URL](https://www.aicoo.io/api/v1)
- [Aicoo Daily Brief ClawHub page](https://clawhub.ai/xisen-w/skills/aicoo-daily-brief)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with concise bullets and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AICOO_API_KEY; can be run manually or on a recurring schedule with /loop, /routine, or cron.]

## Skill Version(s):

0.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
