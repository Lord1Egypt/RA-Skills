## Description:

Manage Alibaba Cloud Data Lake Formation (DataLake) via OpenAPI/SDK. Use whenever the user asks for DataLake catalog resource operations, configuration updates, status queries, or troubleshooting DataLake API workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to plan and carry out Alibaba Cloud Data Lake Formation catalog operations, configuration changes, status checks, and troubleshooting with OpenAPI metadata and SDK workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-directed Data Lake Formation changes could create, update, modify, or set cloud resources incorrectly if parameters or intent are wrong.

Mitigation: Use least-privilege Alibaba Cloud credentials and review any Create, Update, Modify, or Set operation before execution.

Risk: Generated outputs may include cloud API responses or operational evidence outside the expected location.

Mitigation: Keep generated outputs under output/alicloud-data-lake-dlf/ and review artifacts before sharing or reuse.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cinience/skills/alicloud-data-lake-dlf)
- [OpenAPI Product Page](https://api.aliyun.com/product/DataLake)
- [DataLake API List Metadata](https://api.aliyun.com/meta/v1/products/DataLake/versions/2020-07-10/api-docs.json)
- [DataLake Single API Definition Metadata](https://api.aliyun.com/meta/v1/products/DataLake/versions/2020-07-10/apis/{ApiName}/api.json)
- [Sources](references/sources.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API calls, Files]

**Output Format:** [Markdown guidance with shell commands, API call plans, JSON response artifacts, and generated Markdown summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts and response summaries should be written under output/alicloud-data-lake-dlf/.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
