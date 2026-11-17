## Description:

Diagnoses Alibaba Cloud OSS backup-tool integration issues and retrieval-fee causes, providing configuration guidance without changing cloud resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support engineers use this skill to troubleshoot Veeam, Synology, rclone, and other S3-compatible backup integrations with Alibaba Cloud OSS, including signature, endpoint, whitelist, and retrieval-fee issues. It offers advice only; users or support staff make any changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Official-document verification may contact help.aliyun.com and cache public document indexes locally.

Mitigation: Use only when that network access and local caching are acceptable; review the retrieved guidance before relying on it.

Risk: Incorrect configuration advice could affect backup access or billing if applied without checking.

Mitigation: Review recommendations against the affected environment and official documentation; have users or support staff approve and perform changes. Do not provide credentials.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-oss-backup-integration-diagnosis)
- [Integration playbook](references/integration-playbook.md)
- [OSS S3 compatibility notes](references/s3-compat-notes.md)
- [Retrieval fee guide](references/retrieval-fee-guide.md)
- [Alibaba Cloud OSS data processing fees](https://help.aliyun.com/zh/oss/product-overview/data-processing-fees)
- [Alibaba Cloud OSS storage fees](https://help.aliyun.com/zh/oss/product-overview/storage-fees)

## Skill Output:

**Output Type(s):** [Text, Configuration guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the diagnosis, missing inputs, documentation verification where applicable, and that no change was executed.]

## Skill Version(s):

0.0.2 (source: server-resolved release and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
