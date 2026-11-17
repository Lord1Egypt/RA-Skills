## Description:

Alibaba Cloud OSS AI Content Awareness skill for enabling and querying OSS semantic search with AI-powered content understanding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to configure Alibaba Cloud OSS MetaQuery with AI content awareness, upload and index bucket objects, run scalar or semantic searches, and verify index status and results.

### Deployment Geography for Use:

Supported Alibaba Cloud OSS regions: cn-hangzhou, cn-shanghai, cn-qingdao, cn-beijing, cn-zhangjiakou, cn-shenzhen, cn-guangzhou, cn-chengdu, cn-hongkong, ap-southeast-1, and us-east-1.

## Known Risks and Mitigations:

Risk: Remote CLI installation and automatic plugin installation can introduce unreviewed code into the agent environment.

Mitigation: Verify installer sources independently, prefer preapproved package installation, and disable automatic plugin installation after setup.

Risk: The skill can create buckets, upload objects, close indexes, delete OSS resources, and generate presigned links when granted OSS authority.

Mitigation: Use a test bucket or tightly scoped RAM role and require exact bucket, object, index, upload, or presigned-link confirmation before execution.

Risk: Long-lived Alibaba Cloud AccessKeys increase exposure if stored in local CLI configuration or environment variables.

Mitigation: Prefer temporary STS credentials or role-based credentials and avoid printing, echoing, or sharing access-key material.

## Reference(s):

- [Acceptance Criteria](references/acceptance-criteria.md)
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md)
- [MetaQuery Query Condition Reference](references/metaquery.md)
- [OSS RAM Permission Policies](references/ram-policies.md)
- [Related APIs and CLI Commands](references/related-apis.md)
- [Verification Methods](references/verification-method.md)
- [Aliyun CLI Official Documentation](https://help.aliyun.com/zh/cli/)
- [OpenMetaQuery API Documentation](https://help.aliyun.com/zh/oss/developer-reference/openmetaquery)
- [GetMetaQueryStatus API Documentation](https://help.aliyun.com/zh/oss/developer-reference/getmetaquerystatus)
- [DoMetaQuery API Documentation](https://help.aliyun.com/zh/oss/developer-reference/dometaquery)
- [OSS Vector Search User Guide](https://help.aliyun.com/zh/oss/user-guide/vector-retrieval/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, XML query examples, Python script invocations, and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Alibaba Cloud OSS operations that require explicit user confirmation before changing or deleting resources.]

## Skill Version(s):

0.0.2 (source: server release metadata, created 2026-04-24T08:13:59Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
