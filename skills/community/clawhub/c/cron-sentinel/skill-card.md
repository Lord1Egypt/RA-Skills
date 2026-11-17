## Description:

Monitors recurring jobs for failures and missed runs, with optional retries and guidance for setting up alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris](https://clawhub.ai/user/chris)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to detect failed or overdue scheduled jobs and set up a watchdog that can trigger their chosen alerting channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated crontab lines may schedule commands or alerts differently than intended.

Mitigation: Review generated lines before adding them to the scheduler.

Risk: Captured job output may contain credentials or other sensitive data despite best-effort redaction.

Mitigation: Use --no-output-tail for jobs that may print sensitive information.

## Reference(s):

- [Cron Sentinel on ClawHub](https://clawhub.ai/chris/skills/cron-sentinel)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with shell snippets and human-readable job status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated crontab entries require user review and installation; watchdog checks can exit non-zero to signal unhealthy jobs.]

## Skill Version(s):

1.2.0 (source: frontmatter, changelog, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
