## Description:

Audits Alibaba Cloud CEN down-cloud route redundancy across dedicated lines and VPN connections, identifying missing paths, route policy impacts, conflicting routes, and cases needing manual review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and network engineers use this skill to review Alibaba Cloud CEN route evidence for missing or policy-affected redundancy paths before a planned failover. It produces a coverage-aware audit and identifies policy-based routing or failover behavior that needs manual confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the release suspicious because its read-only audit framing is paired with software installation, credential-change, and infrastructure-change instructions.

Mitigation: Review the setup and deployment instructions before use, use only an approved least-privilege cloud identity, and keep any infrastructure-changing activity outside the read-only audit workflow.

Risk: Security analysis is incomplete: 8 of 9 components were fully analyzed and one was partially analyzed.

Mitigation: Treat the scan as incomplete evidence and review the remaining component before installation.

## Reference(s):

- [Detailed route inspection algorithm](references/reference.md)
- [Success verification method](references/verification-method.md)
- [Aliyun CLI installation guide](references/cli-installation-guide.md)
- [Alibaba Cloud CLI documentation](https://www.alibabacloud.com/help/en/cli/)
- [CEN RAM permissions](https://www.alibabacloud.com/help/en/cen/developer-reference/api-cbn-2017-09-12-ram)
- [VPC RAM permissions](https://www.alibabacloud.com/help/en/vpc/developer-reference/api-vpc-2016-04-28-ram)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with route tables, coverage findings, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only configuration audit; calls out uncovered scope and items requiring manual confirmation.]

## Skill Version(s):

0.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
