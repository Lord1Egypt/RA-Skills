## Description:

Use when managing Alibaba Cloud ApsaraVideo for Media Processing (MPS/MTS) resources and workflows via OpenAPI/SDK, including media ingest and metadata tasks, transcoding/snapshot jobs, pipeline/template/workflow operations, and MPS job troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations teams use this skill to discover, validate, and manage Alibaba Cloud ApsaraVideo MPS resources, workflows, and jobs through OpenAPI or SDK-backed agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through Alibaba Cloud MPS operations that update, delete, submit, cancel, or bind cloud resources.

Mitigation: Use least-privilege RAM or STS credentials and require explicit approval before any mutating operation.

Risk: Running the skill against the wrong Alibaba Cloud region, media scope, or OSS bucket can affect unintended resources.

Mitigation: Confirm the target region, media scope, pipeline or template IDs, and OSS input/output buckets before changes.

Risk: API discovery and validation may expose operational details in local evidence files.

Mitigation: Save evidence only in the expected output directory and review outputs before sharing or committing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cinience/skills/aliyun-mps-manage)
- [OpenAPI product page](https://api.aliyun.com/product/mts)
- [API list metadata](https://api.aliyun.com/meta/v1/products/Mts/versions/2014-06-18/api-docs.json)
- [API definition metadata](https://api.aliyun.com/meta/v1/products/Mts/versions/2014-06-18/apis/{ApiName}/api.json)
- [ApsaraVideo for Media Processing documentation](https://www.alibabacloud.com/help/en/mts)
- [Source list](references/sources.md)
- [Task templates](references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, API operation names, configuration guidance, and saved JSON or Markdown evidence files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files and execution evidence are expected under output/aliyun-mps-manage/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
