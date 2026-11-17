## Description:

Generates daily completion reports by aggregating task results, daily completion report records, 30-day WelcomeBackCard summaries, pending items, and tenant completion-rate statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a scheduled daily reporting job for tenant task completion, fairness metrics, 30-day return summaries, and related notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs database authority through PG_DSN and can create or update daily report and tenant notification rows.

Mitigation: Use a least-privilege database role scoped to the expected reporting and notification tables, and review notification side effects before production deployment.

Risk: The security evidence notes under-disclosed inspection of cookie-file metadata and alert logs.

Mitigation: Deploy only where COOKIE_SAVE_DIR and alert log inputs are intended for this reporting job, and restrict file access to the minimum required paths.

Risk: The authoritative scanner verdict is suspicious.

Mitigation: Perform a production review before installation and confirm the database writes, local inspections, and notification behavior match operational expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/completion-report-generator)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Configuration]

**Output Format:** [JSON status object emitted by a Python reporting script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and PG_DSN for database-backed reporting; falls back to a simulated report when the database is unavailable.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
