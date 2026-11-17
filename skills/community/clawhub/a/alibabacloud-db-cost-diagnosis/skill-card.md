## Description:

Provides read-only cost diagnostics and audits for Alibaba Cloud database products, including bill breakdowns, cost trends, renewal and expiry risks, idle capacity, and optional paid features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Alibaba Cloud account owners, database operators, and finance teams use this skill to explain database charges and audit renewal, expiry, idle-capacity, and paid-feature risks using read-only reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit results may include unrelated purchases or misidentify idle databases.

Mitigation: Request database-only order filtering and corrected handling of missing measurements before relying on audit results.

Risk: Incomplete advice could lead to disruptive changes based on a diagnosis.

Mitigation: Independently verify recommendations, preserve required backups and audit logging, and review the official PolarDB unsubscription rules before cancelling a cluster.

Risk: Billing reports can expose private account cost information.

Mitigation: Use a dedicated read-only cloud profile and keep billing reports private.

## Reference(s):

- [Cost query orchestration](references/module1_cost_query.md)
- [Database cost FAQ](references/module2_cost_faq.md)
- [Cost audit guidance](references/module3_cost_audit.md)
- [Read-only RAM policies](references/ram-policies.md)
- [Alibaba Cloud RDS billing FAQ](https://help.aliyun.com/zh/rds/apsaradb-rds-for-mysql/billing-faq)
- [Alibaba Cloud PolarDB billing items](https://help.aliyun.com/zh/polardb/polardb-for-mysql/billing-item/)
- [Alibaba Cloud PolarDB unsubscribe instructions](https://www.alibabacloud.com/help/en/polardb/polardb-for-mysql/unsubscribe-instructions)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON, Guidance]

**Output Format:** [Evidence-based Markdown reports, with optional machine-readable JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Billing findings and audit suggestions based on returned account data; no resource changes are made.]

## Skill Version(s):

0.0.2 (source: references/manifest.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
