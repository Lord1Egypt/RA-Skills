## Description:

Read-only health-check diagnostics for Alibaba Cloud load balancers (CLB/ALB/NLB), producing structured diagnosis reports without changing configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to diagnose Alibaba Cloud CLB, ALB, and NLB health-check failures, unhealthy backend servers, listener health-check configuration, forwarding rules, server groups, and backend probe status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the existing aliyun CLI credential profile to inspect Alibaba Cloud load balancer metadata.

Mitigation: Use the documented read-only RAM policy and avoid granting update, delete, modify, create, or set permissions.

Risk: Generated reports can contain cloud infrastructure and backend health metadata.

Mitigation: Store and share report files only with authorized operators.

Risk: Customer-facing self-check commands are intended to be run on backend servers.

Mitigation: Review commands before execution and replace placeholders with values from the diagnosis report.

## Reference(s):

- [CLB Diagnosis Guide](references/clb-guide.md)
- [ALB Diagnosis Guide](references/alb-guide.md)
- [NLB Diagnosis Guide](references/nlb-guide.md)
- [CLB API and Field Reference](references/clb-reference.md)
- [ALB API and Field Reference](references/alb-reference.md)
- [NLB API and Field Reference](references/nlb-reference.md)
- [Official API Documentation Links](references/api-doc-links.md)
- [Required RAM Permissions](references/ram-policies.md)
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-lb-healthcheck)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with structured tables, plus optional JSON output and customer-facing shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes reports to local output files when requested; generated reports may include cloud infrastructure metadata.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
