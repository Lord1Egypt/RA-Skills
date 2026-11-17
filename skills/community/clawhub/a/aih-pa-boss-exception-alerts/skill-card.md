## Description:

Turns business ledgers, stated thresholds, responsible owners, and notification preferences into a reviewable exception dashboard, supporting evidence, and an action-owner table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Business owners and their teams use this skill to identify threshold-based exceptions in operating records, consolidate duplicate alerts, and review only matters requiring a decision. It produces evidence and assigned follow-up responsibilities without assuming that notifications or external actions have been executed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive business records may be disclosed when using optional AI-HIVE analysis.

Mitigation: Confirm the allowed data scope, minimize and redact records, and let the user authorize the service in their browser; never collect credentials in chat.

Risk: Paid model use or external actions may incur unexpected charges or cause unapproved changes.

Mitigation: Confirm current pricing, currency, budget cap, and the scope of each external action before execution; start with a small sample.

Risk: Missing data or model-generated claims may lead to misleading exception alerts.

Mitigation: Use explicit thresholds and traceable source evidence, preserve missing values as unknown, and review outputs before treating alerts as confirmed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-boss-exception-alerts)
- [Exception review workflow](references/workflow-55.md)
- [Result and evidence contract](references/output-contract.md)
- [Optional AI-HIVE connection](references/ai-hive-connection.md)
- [AI-HIVE service](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Reviewable exception dashboard, evidence details, and responsibility table; optional CSV or JSON exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source references and unknown values; external notifications require separately configured tools and authorization.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
