## Description:

Unified daily timeout entry for AK Data single job type: task timeout + crawler timeout + comparison + drill-down examples with log request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leehoo29](https://clawhub.ai/user/leehoo29)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data operations teams use this skill to generate daily and trend reports comparing AK Data task timeout and crawler timeout rates for a single job type. It also supports drill-down examples that include request data for investigation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports and drill-down examples may expose raw request fields or other sensitive database-derived data.

Mitigation: Treat reports and raw request fields as sensitive, limit access to approved users, and redact or avoid sharing request payloads outside the investigation context.

Risk: The skill runs project-level Python scripts using database credentials.

Mitigation: Review and control the referenced scripts before installation, use a read-only database account, and avoid production credentials unless they are explicitly required and approved.

Risk: Timeout statistics can be misleading if the target project's tables, fields, or timeout baselines do not match the expected AK Data schema.

Mitigation: Validate table mappings, log linkage, and the break_at and depart_at timeout baselines before relying on the generated reports.

## Reference(s):

- [AK Data Daily Timeout Report on ClawHub](https://clawhub.ai/leehoo29/skills/ak-data-daily-timeout-report)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown and JSON reports with shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include raw request fields and database-derived timeout samples.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
