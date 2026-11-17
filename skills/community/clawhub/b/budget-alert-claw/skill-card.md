## Description:

支出预警管控虾 helps agents check spending requests against budget rules, flag overspending or anomalous activity, and draft approval or notification recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, operations, and budget owners use this skill to review expense requests, batch-check expense records against budget configurations, generate budget execution reports, and prepare alerts for yellow or red threshold cases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce unsafe financial recommendations if its budget checks are treated as automatic approval or rejection decisions.

Mitigation: Treat outputs as recommendations only and require human approval for yellow, red, or missing-budget cases.

Risk: Incorrect or malformed budget and expense inputs can affect the resulting alerts and reports.

Mitigation: Validate input files independently before using the skill in production or approval workflows.

Risk: Direct integration with notifications, budget updates, or automatic approvals could amplify an incorrect recommendation.

Mitigation: Avoid wiring the skill directly to Feishu notifications, budget updates, or automatic approvals until scope limits and fail-closed validation are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tujinsama/skills/budget-alert-claw)
- [Budget rules](references/budget-rules.md)
- [Anomaly detection rules](references/anomaly-detection.md)
- [Notification templates](references/notification-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and tables, JSON check results, CSV batch outputs, and notification text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided budget and expense data; financial recommendations should be reviewed before action.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
