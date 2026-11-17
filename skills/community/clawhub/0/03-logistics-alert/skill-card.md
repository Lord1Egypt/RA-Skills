## Description:

Monitors Cainiao and marketplace logistics orders for delivery anomalies, warning levels, expected impact, and compensation estimates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

Internal control and logistics operations users can analyze single orders, batches, monitoring summaries, and confirmed incidents to classify logistics exceptions, prioritize response, and estimate compensation exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch anomaly workflows may lead to supplier risk records, linked-skill notifications, score deductions, or escalation actions without clear confirmation.

Mitigation: Require explicit human approval before recording supplier risk events, notifying linked skills, changing supplier scores, or starting limitation and escalation workflows.

Risk: Compensation estimates and policy thresholds may become stale or differ from current platform rules.

Mitigation: Verify compensation calculations and operational thresholds against current official policies before using the report for customer, supplier, or financial action.

Risk: The skill processes order, supplier, shipment, and compensation details that may be sensitive.

Mitigation: Use it only in an approved internal logistics triage setting and limit shared inputs to necessary operational data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nic-yuan/skills/03-logistics-alert)
- [Continuation examples and operating notes](artifact/references/continuation.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Markdown reports with tables, classification summaries, compensation estimates, and action recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include single-order alerts, batch anomaly summaries, compensation calculations, and supplier risk follow-up recommendations.]

## Skill Version(s):

1.7.0 (source: artifact/SKILL.md frontmatter; ClawHub release metadata version 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
