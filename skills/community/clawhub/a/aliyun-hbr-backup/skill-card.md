## Description:

Use when managing Alibaba Cloud Cloud Backup (HBR) via OpenAPI/SDK, including backup lifecycle operations such as resource listing, policy/config updates, job status queries, and troubleshooting HBR backup or restore workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud engineers, and operators use this skill to plan and run Alibaba Cloud Backup workflows through OpenAPI or SDK calls. It supports inventory, policy and configuration changes, job status checks, and troubleshooting for backup and restore tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide cloud backup operations that may change Alibaba Cloud resources.

Mitigation: Review mutating API calls before execution and use a least-privilege Alibaba Cloud identity.

Risk: Cloud credentials may be needed for user-directed operations.

Mitigation: Prefer environment-based credentials and avoid exposing access keys in prompts, logs, or saved outputs.

Risk: Generated outputs may contain operational details about backup resources.

Mitigation: Keep generated files under output/aliyun-hbr-backup/ and review them before sharing.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/cinience/skills/aliyun-hbr-backup)
- [Sources](references/sources.md)
- [Alibaba Cloud HBR OpenAPI product page](https://api.aliyun.com/product/hbr)
- [Alibaba Cloud HBR API metadata list](https://api.aliyun.com/meta/v1/products/hbr/versions/2017-09-08/api-docs.json)
- [Alibaba Cloud HBR single API metadata schema](https://api.aliyun.com/meta/v1/products/hbr/versions/2017-09-08/apis/{ApiName}/api.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline shell commands, code snippets, API call guidance, and optional JSON or Markdown artifact files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated API inventory, command outputs, and API response summaries under output/aliyun-hbr-backup/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
