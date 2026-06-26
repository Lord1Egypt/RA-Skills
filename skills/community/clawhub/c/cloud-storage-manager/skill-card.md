## Description: <br>
Manage multiple cloud storage providers with file upload and download, bucket management, sync, multipart upload, cross-provider copy, and CDN integration workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and operate multi-cloud object storage workflows across AWS S3, Aliyun OSS, Tencent COS, and Azure Blob. It supports agent guidance for uploads, downloads, listing, deletion, signed URLs, sync, and cross-provider transfer patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide use of cloud credentials for storage accounts. <br>
Mitigation: Use least-privilege credentials scoped to specific buckets, containers, and prefixes, and avoid production-wide keys. <br>
Risk: Sync and delete workflows can remove or overwrite stored data if configured incorrectly. <br>
Mitigation: Test operations on non-critical data, review delete and sync options before execution, and keep recoverable backups for important data. <br>
Risk: The submitted artifact references storage and sync modules that are not included in the submitted files. <br>
Mitigation: Review the complete implementation package before relying on real cloud operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kaiyuelv/cloud-storage-manager) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Basic usage example](artifact/examples/basic_usage.py) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include environment variable names, provider configuration examples, and cloud storage operation plans.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact version fields) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
