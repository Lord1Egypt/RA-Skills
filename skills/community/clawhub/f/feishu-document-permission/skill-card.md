## Description:

Sets Feishu cloud documents to "anyone with the link can view" so external users can access shared documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrot90-code](https://clawhub.ai/user/harrot90-code)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers who share Feishu documents outside their organization use this skill to verify or set link-readable document permissions through Feishu APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a plaintext Feishu app secret.

Mitigation: Revoke and replace the shipped secret, and require users to provide credentials through secure local configuration or environment variables.

Risk: The skill can make Feishu documents readable to anyone with the link.

Mitigation: Require explicit user approval before changing public-link permissions and verify that external sharing is intended for the document.

Risk: The artifact records full document tokens in a persistent log.

Mitigation: Avoid logging full document tokens; redact or hash tokens when audit records are necessary.

## Reference(s):

- [Feishu Tenant Access Token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu Drive Public Permissions API endpoint](https://open.feishu.cn/open-apis/drive/v2/permissions/${DOC_TOKEN}/public?type=docx)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Feishu document token and user-provided Feishu app credentials; should avoid logging full document tokens.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact notes v1.0.0 dated 2026-04-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
