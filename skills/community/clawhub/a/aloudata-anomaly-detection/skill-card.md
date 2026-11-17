## Description:

Detects anomalies in business metrics by obtaining metric data through the metric-query skill, comparing it with baselines, thresholds, or trends, and returning a structured anomaly report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackyujun](https://clawhub.ai/user/jackyujun)

### License/Terms of Use:

MIT-0

## Use Case:

Business analysts and operators use this skill to check whether sales, inventory, member, or other metrics are within expected ranges, identify concerning dimensions, and decide when to continue with attribution analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may query business metric data through the metric-query workflow.

Mitigation: Limit metric access to approved business scopes and review anomaly reports before operational use.

Risk: Broad Chinese health-check wording may route vague requests into anomaly detection.

Mitigation: Tighten trigger phrases or require clarification when the metric, domain, or detection scope is unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackyujun/skills/aloudata-anomaly-detection)
- [Publisher profile](https://clawhub.ai/user/jackyujun)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown structured anomaly reports with optional Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegates data retrieval to metric-query and performs anomaly judgment after data is available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
