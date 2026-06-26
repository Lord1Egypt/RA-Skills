## Description: <br>
Alicloud OSS AI Content Awareness Skill for enabling and querying OSS semantic search with AI-powered content understanding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to configure Alibaba Cloud OSS MetaQuery, enable AI content awareness, and run scalar or semantic searches across bucket contents. <br>

### Deployment Geography for Use: <br>
OSS buckets in cn-hangzhou, cn-shanghai, cn-qingdao, cn-beijing, cn-zhangjiakou, cn-shenzhen, cn-guangzhou, cn-chengdu, cn-hongkong, ap-southeast-1, and us-east-1. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect live Alibaba Cloud OSS buckets, including creating buckets, uploading objects, enabling MetaQuery, and closing indexes. <br>
Mitigation: Use scoped RAM or STS credentials for the exact bucket and require explicit review before create, delete, close-index, or other state-changing actions. <br>
Risk: Credential misuse could expose sensitive Alibaba Cloud access keys or broaden access beyond the intended bucket. <br>
Mitigation: Use a dedicated RAM user or temporary credentials, avoid root or account-wide keys, and do not print, echo, or request access key secrets in conversation or command output. <br>
Risk: Indexing large buckets or enabling AI content awareness can incur cloud costs and may take significant processing time. <br>
Mitigation: Check bucket object counts and confirm costs before enabling MetaQuery, especially for buckets with more than 1000 objects. <br>
Risk: Installer and CLI setup commands fetch external tooling before the workflow can run. <br>
Mitigation: Verify installer sources and plugin updates before running setup commands in managed or production environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-oss-manage-metaquery) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [MetaQuery Query Condition Reference](references/metaquery.md) <br>
- [ossutil Installation Guide](references/ossutil-installation-guide.md) <br>
- [RAM Permission Policies](references/ram-policies.md) <br>
- [Related APIs and CLI Commands](references/related-apis.md) <br>
- [Verification Methods](references/verification-method.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, text] <br>
**Output Format:** [Markdown with shell commands, XML and JSON query snippets, and Python script guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Aliyun CLI commands and bundled Python helper scripts for OSS bucket, MetaQuery, upload, and query workflows.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
