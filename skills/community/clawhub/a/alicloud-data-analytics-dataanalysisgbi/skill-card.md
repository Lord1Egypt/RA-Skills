## Description:

Manage Alibaba Cloud DataAnalysisGBI via OpenAPI/SDK for resource lifecycle operations, configuration changes, status inspection, and troubleshooting for analytics service workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to discover Alibaba Cloud DataAnalysisGBI APIs, prepare required parameters, run lifecycle or configuration operations, and verify service state with list, describe, get, or query APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alibaba Cloud credentials may grant broader access than the DataAnalysisGBI task requires.

Mitigation: Use least-privilege Alibaba Cloud credentials and prefer the documented environment variables or shared credentials file only for the intended account and region.

Risk: Create, Update, Modify, or Set operations can change cloud resources or service configuration.

Mitigation: Review the target region, resource identifiers, parameters, and proposed mutating API call before execution; ask for clarification when the region is unclear.

Risk: Saved API responses and generated artifacts may contain operational details.

Mitigation: Write generated API-response artifacts only under output/alicloud-data-analytics-dataanalysisgbi/ and handle that directory according to the user's data retention requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cinience/skills/alicloud-data-analytics-dataanalysisgbi)
- [OpenAPI product page](https://api.aliyun.com/product/DataAnalysisGBI)
- [API list metadata](https://api.aliyun.com/meta/v1/products/DataAnalysisGBI/versions/2024-08-23/api-docs.json)
- [API definition metadata](https://api.aliyun.com/meta/v1/products/DataAnalysisGBI/versions/2024-08-23/apis/{ApiName}/api.json)
- [Artifact sources](references/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, code snippets, configuration names, and generated file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated API inventory artifacts and response summaries should be written under output/alicloud-data-analytics-dataanalysisgbi/.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
