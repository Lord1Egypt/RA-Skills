## Description:

Diagnoses stuck or failed Alibaba Cloud OSS multipart uploads, identifies unfinished uploads, checks part settings, and provides manual-only cleanup guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to investigate interrupted, stuck, or failed OSS multipart uploads, locate unfinished fragments, and assess part settings without changing cloud resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud metadata access reveals bucket and unfinished-upload details.

Mitigation: Grant only sts:GetCallerIdentity, oss:GetBucketInfo, oss:ListBuckets, and oss:ListMultipartUploads to a dedicated diagnostic role.

Risk: Aborting an unfinished upload irreversibly removes its uploaded fragments.

Mitigation: Do not grant cleanup permissions to the diagnostic role; review any suggested cleanup commands and execute them manually only if intended.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-oss-multipart-upload-diagnosis)
- [Multipart Upload Playbook](artifact/references/multipart-playbook.md)
- [Fragment Cleanup Guide](artifact/references/fragment-cleanup-guide.md)
- [Minimal Read-Only RAM Policy](artifact/references/ram-policies.md)
- [Alibaba Cloud OSS multipart upload documentation](https://help.aliyun.com/zh/oss/user-guide/multipart-upload)
- [Alibaba Cloud OSS abort multipart upload documentation](https://help.aliyun.com/zh/oss/developer-reference/abortmultipartupload)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown with findings and manual cleanup command templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports diagnostic status, next action, evidence and limitations; cleanup is never executed by the skill.]

## Skill Version(s):

0.0.1 (source: server release and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
