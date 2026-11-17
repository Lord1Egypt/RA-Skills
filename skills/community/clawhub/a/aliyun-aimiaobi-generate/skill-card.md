## Description:

Use when managing Alibaba Cloud Quan Miao (AiMiaoBi) via OpenAPI/SDK, including listing resources, creating or updating configurations, querying runtime status, and diagnosing API or workflow failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud Quan Miao resources through OpenAPI or SDK workflows, including API discovery, inventory, configuration changes, status checks, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide create, update, modify, or set operations against Alibaba Cloud resources using user credentials.

Mitigation: Use least-privilege Alibaba Cloud AccessKeys and review proposed mutating actions before execution.

Risk: Untrusted product code, API version, or output directory values passed to the helper script may affect what remote metadata is fetched or where artifacts are written.

Mitigation: Use known Alibaba Cloud product and version values, and keep helper output paths inside the dedicated skill output directory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cinience/skills/aliyun-aimiaobi-generate)
- [Sources](references/sources.md)
- [OpenAPI Product Page](https://api.aliyun.com/product/AiMiaoBi)
- [OpenAPI Metadata API List](https://api.aliyun.com/meta/v1/products/AiMiaoBi/versions/2023-08-01/api-docs.json)
- [OpenAPI Single API Definition](https://api.aliyun.com/meta/v1/products/AiMiaoBi/versions/2023-08-01/apis/{ApiName}/api.json)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, markdown]

**Output Format:** [Markdown guidance with inline shell commands, Python helper output, JSON API metadata files, and Markdown API inventory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saved artifacts and API response summaries should be written under output/aliyun-aimiaobi-generate/ for traceability.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
