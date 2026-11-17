## Description:

Diagnoses Alibaba Cloud OSS presigned URL failures and guides V1-to-V4 signature migration using URL analysis and documented failure modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support engineers use this skill to investigate failing OSS signed links, distinguish confirmed causes from candidate causes, and plan V4 migration or link recovery without accessing cloud credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advisory questions can trigger outbound documentation requests and write a local documentation cache despite claims of offline, read-only operation.

Mitigation: Review before use in strictly offline environments; disable the documentation lookup path when network access or local cache writes are prohibited.

Risk: Presigned URLs may contain sensitive signing parameters.

Mitigation: Do not paste secrets or credentials; review and mask URL parameters before sharing diagnostic input or output.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-oss-presigned-url-v4-diagnosis)
- [Presigned URL failure catalog](references/presigned-url-failure-catalog.md)
- [V4 upgrade checklist](references/v4-upgrade-checklist.md)
- [Scope and limitations](references/scope-and-limitations.md)
- [Alibaba Cloud OSS URL signing documentation](https://help.aliyun.com/zh/oss/developer-reference/add-signatures-to-urls)

## Skill Output:

**Output Type(s):** [Diagnostic guidance, Markdown]

**Output Format:** [Markdown with root-cause directions and documentation links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Distinguishes confirmed diagnoses from candidate failure modes and provides V4 upgrade or link-recovery steps.]

## Skill Version(s):

0.0.1 (source: ClawHub release metadata and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
