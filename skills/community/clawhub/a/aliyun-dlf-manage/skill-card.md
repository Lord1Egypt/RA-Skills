## Description:

Helps agents manage Alibaba Cloud Data Lake Formation (DataLake) resources through Alibaba Cloud OpenAPI/SDK workflows for catalog operations, configuration updates, status queries, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to discover Alibaba Cloud Data Lake Formation APIs, plan DataLake catalog and configuration actions, run supported OpenAPI or SDK workflows, and verify results with list or describe operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alibaba Cloud credentials could allow broader Data Lake Formation access than the task requires.

Mitigation: Use least-privilege Alibaba Cloud credentials and prefer environment variables or the shared credentials file described by the skill.

Risk: Create, update, modify, or set operations can change cloud resources.

Mitigation: Review mutating actions, target regions, and resource identifiers before execution, then verify results with list or describe APIs.

Risk: Saved command outputs and API response summaries may include resource identifiers or operational details.

Mitigation: Keep generated evidence under output/aliyun-dlf-manage/ and handle those files according to the deployment's data handling requirements.

## Reference(s):

- [Source References](references/sources.md)
- [Alibaba Cloud DataLake OpenAPI Product Page](https://api.aliyun.com/product/DataLake)
- [DataLake 2020-07-10 API Metadata](https://api.aliyun.com/meta/v1/products/DataLake/versions/2020-07-10/api-docs.json)
- [DataLake Single API Metadata Template](https://api.aliyun.com/meta/v1/products/DataLake/versions/2020-07-10/apis/{ApiName}/api.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline bash or Python examples, plus JSON or Markdown evidence files when saved.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save API inventories, command outputs, and API response summaries under output/aliyun-dlf-manage/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
