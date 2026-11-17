## Description:

Monitors OpenClaw cron job health, identifies failures, timeouts, and delivery issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinthqod](https://clawhub.ai/user/qinthqod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check OpenClaw cron jobs for recent failures, timeout patterns, delivery issues, and recurring error states. It supports manual checks and scheduled monitoring after cron job changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cron job definitions and run logs may contain operational error details.

Mitigation: Run the skill only in trusted local OpenClaw environments and review health reports before sharing them.

Risk: Scheduled monitoring can create recurring executions if configured unintentionally.

Mitigation: Use the scheduled cron example only when recurring monitoring is desired, and update the example path to the actual installed skill location.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qinthqod/skills/fox-cron-health-check)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text health report or JSON summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit codes 0, 1, and 2 indicate healthy, warning, and critical results.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
