## Description:

Use when managing Alibaba Cloud DevOps (Yunxiao 2020) via OpenAPI/SDK, including project/repository/pipeline resource discovery, read-only inspection, and safe change planning before mutating operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to inspect Alibaba Cloud DevOps projects, repositories, pipelines, work items, and related API metadata before planning or executing DevOps changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials may grant broad access to Alibaba Cloud DevOps resources.

Mitigation: Use a least-privilege Alibaba Cloud identity, preferably read-only for inventory tasks.

Risk: Mutating DevOps APIs can change projects, repositories, pipelines, work items, or test resources.

Mitigation: Require explicit owner approval, a confirmed change window, read-only baseline checks, and a rollback plan before mutation.

Risk: Unpinned SDK dependencies can introduce supply-chain drift.

Mitigation: Pin SDK versions or use a controlled package mirror when supply-chain assurance is required.

## Reference(s):

- [DevOps API Quick Map](references/api_quick_map.md)
- [DevOps Operation Templates](references/templates.md)
- [DevOps Official Sources](references/sources.md)
- [Alibaba Cloud DevOps API Explorer](https://api.aliyun.com/product/devops)
- [Alibaba Cloud DevOps OpenAPI Metadata](https://api.aliyun.com/meta/v1/products/devops/versions/2021-06-25/api-docs.json)
- [Alibaba Cloud DevOps Documentation](https://www.alibabacloud.com/help/en/yunxiao)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python script guidance, and optional JSON or text output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated outputs and API response summaries are intended to be saved under output/aliyun-devops-manage/ with key parameters for reproducibility.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
