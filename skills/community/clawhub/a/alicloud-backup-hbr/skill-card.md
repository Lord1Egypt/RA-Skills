## Description:

Manage Alibaba Cloud Cloud Backup (HBR) via OpenAPI/SDK. Use whenever the user asks for backup lifecycle operations such as resource listing, policy/config updates, job status queries, and troubleshooting HBR backup or restore workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud Cloud Backup (HBR) lifecycle workflows, including inventory, policy or configuration changes, job status checks, and backup or restore troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide mutating Alibaba Cloud Backup actions such as Create, Update, Modify, or Set operations.

Mitigation: Use a least-privilege Alibaba Cloud RAM user and review mutating actions before execution.

Risk: The skill can generate local API inventory artifacts and response summaries.

Mitigation: Keep generated artifacts in output/alicloud-backup-hbr/ and avoid storing unnecessary sensitive data.

## Reference(s):

- [Skill Sources](references/sources.md)
- [Alibaba Cloud OpenAPI HBR Product Page](https://api.aliyun.com/product/hbr)
- [Alibaba Cloud HBR API Metadata List](https://api.aliyun.com/meta/v1/products/hbr/versions/2017-09-08/api-docs.json)
- [Alibaba Cloud HBR Single API Metadata](https://api.aliyun.com/meta/v1/products/hbr/versions/2017-09-08/apis/{ApiName}/api.json)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands and generated JSON or Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts should be written under output/alicloud-backup-hbr/.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
