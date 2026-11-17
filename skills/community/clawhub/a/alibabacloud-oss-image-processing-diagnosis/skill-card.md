## Description:

Read-only diagnostics for Alibaba Cloud OSS image processing issues, including x-oss-process errors, image style or watermark failures, forced downloads, original image protection 403s, unsupported-format BadRequest responses, WebP conversion errors, HEIC thumbnail errors, and image-processing action order differences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud support engineers use this skill to diagnose Alibaba Cloud OSS image-processing failures with read-only checks and evidence-based recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use Alibaba Cloud credentials against arbitrary OSS endpoints and may enumerate account buckets.

Mitigation: Use a tightly scoped, short-lived Alibaba Cloud role, avoid Resource:* where possible, do not provide arbitrary endpoint values, and allow bucket enumeration only when account inventory exposure is acceptable.

Risk: Installing or upgrading the aliyun CLI changes the local system.

Mitigation: Review and approve any aliyun CLI installation or upgrade before running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-oss-image-processing-diagnosis)
- [Image Processing Diagnosis Playbook](artifact/references/image-processing-playbook.md)
- [x-oss-process Parameters and Official Limits](artifact/references/params-limits.md)
- [Minimal Read-Only RAM Policy](artifact/references/ram-policies.md)
- [Alibaba Cloud OSS image processing overview](https://help.aliyun.com/zh/oss/user-guide/overview-17/)
- [Alibaba Cloud OSS image processing limits](https://help.aliyun.com/zh/oss/user-guide/limits)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with structured findings, status, next action, cited documentation, and read-only command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conclusions should be grounded in the diagnostic script output and should declare degraded evidence or auto-filled parameters when present.]

## Skill Version(s):

0.0.1 (source: release evidence, artifact/references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
