## Description:

Checks Huawei Cloud CTS audit logs for anomalous operations, including account debt status, failed operations, sensitive actions, and security-relevant audit patterns, then presents findings in user-readable reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenyujie](https://clawhub.ai/user/chenyujie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud operators, and security reviewers use this skill to inspect Huawei Cloud CTS activity for failed, sensitive, deletion, permission-change, and other audit-relevant operations. It supports routine account checks, security auditing, troubleshooting, and compliance review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates 24-hour Huawei Cloud temporary credentials and checks billing data, which can expose sensitive account context if run with broad privileges or without consent.

Mitigation: Review before installing, run only with a tightly scoped Huawei Cloud identity, and require explicit approval before temporary credential creation or billing checks.

Risk: Generated reports may contain sensitive audit, account, user, and resource data.

Mitigation: Limit access to report outputs, avoid broad cron logging or email forwarding, and route findings only to approved security or operations channels.

Risk: CTS results depend on the selected region, project ID, tracker state, and granted permissions, so incomplete scope can produce misleading reassurance.

Mitigation: Confirm the intended region and project before execution, verify CTS is enabled, and document any permission or data-scope limits with the report.

## Reference(s):

- [CTS Anomaly Types Reference](references/anomaly-types.md)
- [CTS Anomaly Check Examples](references/examples.md)
- [Huawei Cloud CTS API Reference](https://support.huaweicloud.com/api-cts/cts_04_0001.html)
- [Huawei Cloud CTS User Guide](https://support.huaweicloud.com/usermanual-icts/cts_01_0001.html)
- [Huawei Cloud IAM Best Practices](https://support.huaweicloud.com/bestpractice-iam/iam_01_0001.html)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text report or JSON, with command examples in Markdown documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include Huawei Cloud audit events, user names, resource names, operation status, region, timing, and billing status signals.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
