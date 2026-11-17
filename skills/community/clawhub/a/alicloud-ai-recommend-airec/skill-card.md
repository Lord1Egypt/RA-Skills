## Description:

Manage Alibaba Cloud AIRec (Airec) via OpenAPI/SDK for recommendation-engine resource operations in Alibaba Cloud, including list/create/update flows, status inspection, and troubleshooting AIRec configuration or runtime issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud AIRec recommendation service resources, inspect status, troubleshoot configuration or runtime issues, and generate reproducible operation evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through Alibaba Cloud AIRec operations that may read or change cloud resources.

Mitigation: Install it only for AIRec work and use a least-privilege AccessKey scoped to the specific resources needed.

Risk: Incorrect region or resource identifiers could target the wrong AIRec resources during mutating operations.

Mitigation: Confirm region and resource IDs before create, update, modify, set, or delete style operations.

Risk: Generated files may contain operational details or API response summaries.

Mitigation: Review files written under output/alicloud-ai-recommend-airec/ before sharing or committing them.

## Reference(s):

- [Skill sources](references/sources.md)
- [Alibaba Cloud AIRec OpenAPI product page](https://api.aliyun.com/product/Airec)
- [Alibaba Cloud AIRec API metadata list](https://api.aliyun.com/meta/v1/products/Airec/versions/2020-11-26/api-docs.json)
- [Alibaba Cloud AIRec single API metadata template](https://api.aliyun.com/meta/v1/products/Airec/versions/2020-11-26/apis/{ApiName}/api.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON or Markdown artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated or captured artifacts should be written under output/alicloud-ai-recommend-airec/.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
