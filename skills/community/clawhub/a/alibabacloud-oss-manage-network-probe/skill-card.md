## Description:

Alicloud Service Scenario-Based Skill for diagnosing local-to-OSS network state, upload and download bandwidth, download time, and local symlink issues with `aliyun ossutil probe`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to prepare Aliyun CLI and ossutil probe workflows, then interpret OSS connectivity, throughput, download-time, and local symlink diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The selected Alibaba Cloud profile may have access to production OSS buckets or broad object scopes.

Mitigation: Use a least-privilege, test-only bucket or prefix and avoid copying Resource '*' policies into production.

Risk: Credential or signed URL material can be exposed through direct handling, command history, logs, or final output.

Mitigation: Do not let the agent handle raw AK/SK values, redact presigned URL query strings, and avoid the documented fixed /tmp presigned-URL script pattern unless replaced with a private temporary directory or pipe-based handling.

Risk: Broad CLI installation, plugin update, credential, and delete-permission guidance can change the local environment or affect OSS objects.

Mitigation: Verify CLI binaries and plugins through trusted package channels, confirm profile validity before plugin operations, and grant delete permissions only when cleanup of confirmed test objects is required.

## Reference(s):

- [Acceptance Criteria](references/acceptance-criteria.md)
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md)
- [Implementation Boundaries](references/implementation-boundaries.md)
- [RAM Policies](references/ram-polices.md)
- [Related APIs and Commands](references/related-apis.md)
- [Verification Method](references/verification-method.md)
- [Aliyun CLI Official Documentation](https://help.aliyun.com/zh/cli/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash command blocks and diagnostic summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes parameter confirmation, credential safety gates, probe result interpretation, and cleanup guidance.]

## Skill Version(s):

0.0.2 (source: server release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
