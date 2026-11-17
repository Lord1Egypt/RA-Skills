## Description:

Investigates reported Alibaba Cloud AccessKey exposure through read-only checks and produces an incident timeline, impact assessment, and remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Security responders and Alibaba Cloud administrators use this skill to investigate suspected AccessKey exposure, review related activity and affected identities, and prepare a report for manual incident follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The investigation may misidentify legitimate users as attackers and recommend deleting their accounts or credentials.

Mitigation: Verify each user's connection to the leaked key before cleanup. Use read-only credentials, protect saved reports, and independently verify every proposed deletion. The skill itself makes no cloud changes.

## Reference(s):

- [Investigation flow](artifact/references/investigation_flow.md)
- [ActionTrail audit](artifact/references/module3_actiontrail_audit.md)
- [Timeline report](artifact/references/module4_timeline_report.md)
- [Remediation best practices](artifact/references/module5_remediation_best_practices.md)
- [RAM read-only policies](artifact/references/ram-policies.md)
- [Alibaba Cloud AccessKey leakage solution](https://www.alibabacloud.com/help/en/ram/user-guide/solution-to-accesskey-leakage)
- [Alibaba Cloud AccessKey restrictive protection](https://www.alibabacloud.com/help/en/ram/user-guide/accesskey-restrictive-protection-description)
- [Alibaba Cloud identity and access control best practices](https://www.alibabacloud.com/help/en/ram/product-overview/best-practices-for-identity-and-access-control)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown incident report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only findings with an incident timeline, impact assessment, risk analysis, and manual remediation guidance.]

## Skill Version(s):

0.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
