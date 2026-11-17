## Description:

Manages Alibaba Cloud DataAnalysisGBI resources through OpenAPI or SDK workflows for lifecycle operations, configuration changes, status inspection, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to discover DataAnalysisGBI OpenAPI metadata, prepare API calls, and manage or troubleshoot Alibaba Cloud analytics resources with configured credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alibaba Cloud credentials could be used with broader access than the task requires.

Mitigation: Configure least-privilege Alibaba Cloud credentials and use environment variables or the shared credentials file only for the intended account.

Risk: Mutating OpenAPI operations could create, update, modify, set, or remove the wrong resource.

Mitigation: Confirm the intended region, resource IDs, and operation before running mutating calls, and verify results with describe or list APIs.

Risk: Missing or incorrect region context can cause calls to target the wrong service endpoint or resource set.

Mitigation: Use ALICLOUD_REGION_ID when available, and ask the user for the region when it is unclear before performing changes.

## Reference(s):

- [Sources](references/sources.md)
- [Alibaba Cloud DataAnalysisGBI OpenAPI product page](https://api.aliyun.com/product/DataAnalysisGBI)
- [DataAnalysisGBI OpenAPI metadata API list](https://api.aliyun.com/meta/v1/products/DataAnalysisGBI/versions/2024-08-23/api-docs.json)
- [DataAnalysisGBI single API metadata schema](https://api.aliyun.com/meta/v1/products/DataAnalysisGBI/versions/2024-08-23/apis/{ApiName}/api.json)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-gbi-analytics)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and generated JSON or Markdown artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save OpenAPI metadata, command outputs, and API response summaries under output/aliyun-gbi-analytics/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
