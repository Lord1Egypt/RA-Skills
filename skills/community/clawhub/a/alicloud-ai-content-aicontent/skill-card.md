## Description:

Manage Alibaba Cloud AIContent resources through Alibaba Cloud OpenAPI or SDK workflows for content generation, asset listing, generation configuration, task status checks, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to work with Alibaba Cloud AIContent APIs, discover operation schemas, run metadata-first workflows, and validate AI content generation or workflow tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials may authorize Alibaba Cloud AIContent changes beyond the intended task.

Mitigation: Use least-privilege Alibaba Cloud credentials and confirm region and resource identifiers before API calls.

Risk: Create, update, modify, or set API calls can change cloud resources or workflow configuration.

Mitigation: Review proposed mutating calls and parameters before execution; prefer list, describe, get, or query calls for discovery and troubleshooting.

Risk: Untrusted product-code, version, or output-dir values passed to the metadata script can fetch unexpected metadata or write files in unintended locations.

Mitigation: Use trusted metadata arguments and keep generated files under output/alicloud-ai-content-aicontent/.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/alicloud-ai-content-aicontent)
- [Sources](references/sources.md)
- [Alibaba Cloud AIContent OpenAPI product page](https://api.aliyun.com/product/AiContent)
- [AIContent API metadata list](https://api.aliyun.com/meta/v1/products/AiContent/versions/20240611/api-docs.json)
- [AIContent single API metadata schema](https://api.aliyun.com/meta/v1/products/AiContent/versions/20240611/apis/{ApiName}/api.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands, configuration guidance, and optional JSON or Markdown output artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save API metadata, command outputs, and API response summaries under output/alicloud-ai-content-aicontent/.]

## Skill Version(s):

1.0.4 (source: server release evidence; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
