## Description:

Automates exporting Alibaba Cloud SLS (Log Service) logs to OSS (Object Storage) for cold storage archival.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to configure, create, inspect, start, stop, and delete Alibaba Cloud SLS-to-OSS export tasks for Security Center backup, log archival, and cold storage workflows.

### Deployment Geography for Use:

Alibaba Cloud regions that support SLS OSS export, with the SLS Project and OSS Bucket in the same region.

## Known Risks and Mitigations:

Risk: The skill can install or update external CLI code and plugins.

Mitigation: Prefer a verified package-manager path or manually reviewed CLI installation path before use.

Risk: The skill can create, stop, or delete Alibaba Cloud SLS OSS export jobs using sensitive cloud credentials.

Mitigation: Use tightly scoped RAM users or temporary credentials and confirm the exact SLS project, LogStores, OSS bucket, region, encryption, retention, and access policy before making changes.

Risk: Delete or force-delete operations can stop future log archival.

Mitigation: Treat destructive export-task actions as human-confirmed changes and verify task state after the operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-sas-log-to-oss)
- [SLS OSS Export API reference](references/reference.md)
- [RAM permission policy document](references/ram-policies.md)
- [Success verification method](references/verification-method.md)
- [Complete command list](references/related-commands.md)
- [Acceptance criteria](references/acceptance-criteria.md)
- [Aliyun CLI installation guide](references/cli-installation-guide.md)
- [Official Alibaba Cloud SLS OSS export help](references/aliyun-help-create-sls-export-oss-task.md)
- [Official Alibaba Cloud OSS Bucket help](references/aliyun-help-oss-bucket.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide or run Alibaba Cloud SDK operations when invoked with user-confirmed cloud parameters and configured credentials.]

## Skill Version(s):

0.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
