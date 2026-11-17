## Description:

Automated security scanner for identifying and reporting misconfigurations across cloud infrastructure providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users, security teams, DevOps engineers, and cloud architects use this skill to initiate cloud configuration scans and review JSON findings about misconfigurations, severity, remediation recommendations, and compliance impact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to send cloud credentials and cloud inventory data to an external scanning API without clear scope, retention, or least-privilege details in the evidence.

Mitigation: Use a dedicated, temporary, read-only identity scoped to the exact account, project, subscription, regions, and APIs needed for the scan; do not provide root, owner, administrator, production long-lived, or organization-wide credentials.

Risk: The evidence does not establish the provider's retention, logging, deletion, or credential redaction practices.

Mitigation: Confirm the provider's retention, logging, deletion, and credential redaction practices before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/cloud-misconfig-scanner)
- [Cloud Misconfiguration Scanner API route](https://api.mkkpro.com/security/cloud-misconfig-scanner)
- [Cloud Misconfiguration Scanner API docs](https://api.mkkpro.com:8018/docs)
- [ToolWeb OpenClaw page](https://toolweb.in/openclaw/)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, JSON, Guidance]

**Output Format:** [JSON responses with scan status, findings, severity, recommendations, compliance impact, and summary counts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires provider credentials and a cloud provider identifier in the request body.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
