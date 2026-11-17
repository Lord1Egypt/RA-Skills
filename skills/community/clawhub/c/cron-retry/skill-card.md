## Description:

Auto-retry failed cron jobs on connection recovery. Use when cron jobs fail due to network errors and should be retried when connectivity is restored. Integrates with heartbeat to detect failed jobs and re-run them automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jrbobbyhansen-pixel](https://clawhub.ai/user/jrbobbyhansen-pixel)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to help an agent identify cron jobs that failed from transient network errors and retry eligible jobs after connectivity returns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic retry behavior can rerun cron jobs with repeated or duplicate side effects when safeguards are missing.

Mitigation: Install only for cron jobs that are idempotent or have duplicate-suppression protections, and add per-job opt-in, cooldowns using lastRunAtMs, retry limits, logging, and manual review for repeated failures.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is intended for heartbeat-based cron recovery workflows.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
