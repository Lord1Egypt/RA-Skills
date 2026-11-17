## Description:

Diagnoses Alibaba Cloud OSS cross-account authorization failures by collecting read-only ownership and policy evidence, attributing AccessDenied or NoPermission causes, and emitting manual configuration templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to diagnose Alibaba Cloud OSS cross-account access, replication, migration, and AssumeRole authorization failures. It helps them identify ownership, bucket policy, RAM policy, trust policy, and explicit-deny causes while keeping remediation as manual reviewable templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scoped Alibaba Cloud diagnostic credentials can reveal OSS bucket metadata and bucket inventory.

Mitigation: Use least-privilege read-only credentials scoped to the buckets under investigation and limit raw diagnostic output to the incident team.

Risk: Generated authorization templates can include write or delete-related actions such as oss:PutObject or oss:ReplicateDelete.

Mitigation: Review every generated template before manual application, remove unneeded write or delete permissions, and apply changes through normal change control.

Risk: A missing or empty manifest version prevents the diagnostic scripts from running reliably.

Mitigation: Confirm the packaged references/manifest.json contains the intended release version before executing diagnostics.

## Reference(s):

- [Cross-Account Authorization Failure Decision Tree](references/cross-account-auth-decision-tree.md)
- [Authorization Configuration Templates](references/auth-config-templates.md)
- [Minimal Read-Only RAM Policy](references/ram-policies.md)
- [Alibaba Cloud OSS cross-account access by RAM role](https://help.aliyun.com/zh/oss/user-guide/cross-account-access-by-ram-role)
- [Alibaba Cloud OSS data replication permissions](https://help.aliyun.com/zh/oss/user-guide/introduction-to-data-replication-permissions)
- [Alibaba Cloud RAM AccessDenied troubleshooting](https://help.aliyun.com/zh/ram/support/how-to-troubleshoot-an-access-denied-error)
- [Alibaba Cloud RAM DecodeDiagnosticMessage API](https://api.aliyun.com/api/Ram/2015-05-01/DecodeDiagnosticMessage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only diagnostic reports include status, next action, evidence limitations, attribution, and manual remediation templates.]

## Skill Version(s):

0.0.1 (source: release evidence and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
