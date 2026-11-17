## Description:

Diagnoses Alibaba Cloud OSS browser and mini-program direct-upload and CORS failures using read-only checks, then provides manual remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose browser or mini-program uploads to Alibaba Cloud OSS that fail because of CORS, preflight requests, missing exposed headers, or PostObject policies, and to obtain manual configuration guidance without changing cloud resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials allow the agent to read OSS bucket metadata and CORS settings.

Mitigation: Use a temporary RAM role or narrowly scoped RAM user with only sts:GetCallerIdentity, oss:GetBucketInfo, oss:GetBucketCors, and oss:ListBuckets; do not grant mutation or administrator permissions.

Risk: Installing or upgrading the aliyun CLI changes local tooling.

Mitigation: Review any proposed CLI installation or upgrade before allowing it.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/sdk-team/skills/alibabacloud-oss-browser-upload-cors-diagnosis)
- [CORS rules and preflight reference](references/cors-rules.md)
- [Browser upload diagnosis tree](references/diagnosis-tree.md)
- [Read-only RAM policies](references/ram-policies.md)
- [Alibaba Cloud OSS: Configure CORS](https://help.aliyun.com/zh/oss/user-guide/configure-cross-origin-resource-sharing)
- [Alibaba Cloud OSS: PostObject](https://help.aliyun.com/zh/oss/developer-reference/postobject)
- [Alibaba Cloud OSS: Direct client uploads](https://help.aliyun.com/zh/oss/user-guide/uploading-objects-to-oss-directly-from-clients/)

## Skill Output:

**Output Type(s):** [Analysis, Configuration guidance]

**Output Format:** [Markdown guidance based on a structured JSON diagnostic report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only findings, status and next action, with CORS and PostObject templates for manual use.]

## Skill Version(s):

0.0.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
