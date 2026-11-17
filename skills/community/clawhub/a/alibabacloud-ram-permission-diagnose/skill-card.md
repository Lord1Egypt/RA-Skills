## Description:

Alibaba Cloud RAM permission diagnosis and repair assistant for permission-related errors across Alibaba Cloud resources, including 403, NoPermission, Forbidden, AccessDenied, and InvalidSecurityToken cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud operators, and support engineers use this skill to triage Alibaba Cloud RAM permission failures, identify missing or denying policies, and generate least-privilege repair recommendations. When explicitly approved by the user, it can provide or execute Aliyun CLI repair steps and console guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and plugin update steps can change the local Aliyun CLI environment in ways the user may not have reviewed.

Mitigation: Review Aliyun CLI installation and plugin update steps before use; avoid curl-to-bash and blanket auto-updates where possible.

Risk: RAM repair workflows can modify IAM policies, trust policies, or role attachments with account-wide impact.

Mitigation: Use a tightly scoped diagnostic identity first, require explicit user approval before every write repair, and back up existing policy and trust documents before changes.

Risk: Broad policies such as AliyunRAMFullAccess can grant extensive IAM authority.

Mitigation: Prefer least-privilege custom policies and grant AliyunRAMFullAccess only when a cloud administrator accepts the account-wide IAM risk.

## Reference(s):

- [Diagnose Flow Reference](artifact/references/diagnose-flow.md)
- [Alibaba Cloud RAM Permission ErrorCode Reference](artifact/references/error-codes.md)
- [Popular Services RAM Action Reference](artifact/references/hot-services-ram.md)
- [RAM-Related aliyun CLI Command Reference](artifact/references/ram-cli-commands.md)
- [RAM Hints for ram-permission-diagnose Skill](artifact/references/ram-policies.md)
- [Alibaba Cloud RAM Troubleshooting Documentation](https://help.aliyun.com/document_detail/93733.html)
- [Alibaba Cloud RAM Authorization Action List](https://help.aliyun.com/document_detail/28630.html)
- [Alibaba Cloud RAM Policies Console](https://ram.console.aliyun.com/policies)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic summaries, Aliyun CLI commands, RAM policy JSON, permission request materials, undo commands, and console repair guidance.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
