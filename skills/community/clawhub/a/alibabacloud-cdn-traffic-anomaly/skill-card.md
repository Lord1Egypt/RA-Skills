## Description:

Read-only diagnostics for Alibaba Cloud CDN traffic and bandwidth anomalies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to investigate unexpected CDN traffic, bandwidth, or billing increases. It compares usage trends, analyzes available access logs, and prepares evidence-based findings and manual remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access logs and reports can contain client IP addresses and full URLs.

Mitigation: Protect stored logs and reports with appropriate access controls, and retain downloaded logs only when needed.

Risk: Cloud account access is required for read-only diagnostics.

Mitigation: Confirm the CLI account, target domain, and analysis window; grant only the listed read-only permissions.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/sdk-team/skills/alibabacloud-cdn-traffic-anomaly)
- [Anomaly detection flow](references/anomaly-detection-flow.md)
- [Protection capabilities](references/protection-capabilities.md)
- [RAM policies](references/ram-policies.md)
- [Report template](references/report-template.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown report, Guidance]

**Output Format:** [Structured Markdown diagnosis report (optional JSON output)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are based on returned usage data and available access logs; missing data is reported as a limitation.]

## Skill Version(s):

0.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
