## Description:

Analyzes user records from a MySQL database to assess suspected fraudulent task completion using timing, publisher concentration, duplicate-task, and top-refresh patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[star1986c](https://clawhub.ai/user/star1986c)

### License/Terms of Use:


## Use Case:

Operations, risk, and fraud-review users use this skill to investigate accounts, tasks, publishers, or IP addresses for suspected task-fraud patterns and generate a risk assessment. It is suited to case-scoped review where access to the underlying user and transaction data is authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published artifact includes a reusable database password.

Mitigation: Rotate the exposed credential and replace embedded secrets with authenticated, scoped access before any use.

Risk: The workflow can expose sensitive user, login, device, payment, and account data through broad command-line lookups.

Mitigation: Rebuild access behind a case-scoped service with read-only least privilege, masking, audit logging, and controls that prevent arbitrary user or IP enumeration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/star1986c/skills/check-user-fraud)
- [README](artifact/README.md)
- [Fraud analysis guide](artifact/references/fraud_analysis_guide.md)
- [User records SQL reference](artifact/references/query_user_records.sql)
- [Top refresh SQL reference](artifact/references/query_top_refresh.sql)
- [Account transactions SQL reference](artifact/references/query_account_trans.sql)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON and console text reports with fraud indicators, supporting records, and risk summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive user, login, device, payment, and account fields.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
