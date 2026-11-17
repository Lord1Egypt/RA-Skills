## Description:

Guides agents through Alibaba Cloud KMS secret management, including create, delete, update, query, version-management, and rotation-policy workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to guide Alibaba Cloud KMS secret administration, including secret lifecycle management, managed credential rotation, RAM permission planning, and verification of KMS operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live Alibaba Cloud KMS administration where broad permissions may expose, overwrite, rotate, or irreversibly delete sensitive credentials.

Mitigation: Use a tightly scoped RAM identity, avoid wildcard policies, test in non-production first, and require explicit confirmation before write, rotation, policy, retrieval, or deletion operations.

Risk: Secret values and AK/SK credentials may be exposed through chat, shell history, logs, or command output.

Mitigation: Do not request AK/SK values in conversation, avoid printing SecretData, prefer secure local credential providers or files, and mask secret values unless plaintext retrieval is explicitly requested and confirmed.

Risk: Force deletion can remove secrets without recovery.

Mitigation: Describe the target secret first, confirm identity and usage with the user, and prefer recovery-window deletion when immediate unrecoverable removal is not required.

## Reference(s):

- [KMS Secret Management Skill](https://clawhub.ai/sdk-team/skills/alibabacloud-kms-secret-manage)
- [Related API List](references/related-apis.md)
- [RAM Permission Policies](references/ram-policies.md)
- [Managed Credentials Guide](references/managed-credentials.md)
- [Verification Methods](references/verification-method.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md)
- [Alibaba Cloud CLI Documentation](https://help.aliyun.com/zh/cli/)
- [KMS API Reference](https://help.aliyun.com/zh/kms/key-management-service/developer-reference/api-kms-2016-01-20-overview)
- [KMS RAM Authorization Information](https://help.aliyun.com/zh/kms/key-management-service/security-and-compliance/authorization-information)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Alibaba Cloud CLI commands and Python SDK code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands for live Alibaba Cloud KMS operations; secret values should be masked unless explicitly requested and confirmed.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
