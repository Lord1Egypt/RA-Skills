## Description:

Manage Alibaba Cloud AnalyticDB for MySQL (ADB) via OpenAPI/SDK. Use whenever the user needs AnalyticDB resource lifecycle and configuration operations, status checks, or troubleshooting ADB API and cluster workflow issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to discover Alibaba Cloud AnalyticDB for MySQL APIs, manage ADB resource lifecycle and configuration workflows, check status, and troubleshoot cluster operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide Create, Update, Modify, and Set operations against cloud resources.

Mitigation: Review mutating operations before execution and confirm region, resource identifiers, and desired changes.

Risk: Alibaba Cloud credentials are required for real API operations.

Mitigation: Use least-privilege Alibaba Cloud credentials and prefer environment variables or the shared Alibaba Cloud credentials file.

Risk: Generated files and saved API responses may contain cloud resource details.

Mitigation: Store outputs only in the designated skill output directory and handle those files according to the sensitivity of the cloud environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/alicloud-database-analyticdb-mysql)
- [OpenAPI product page](https://api.aliyun.com/product/adb)
- [API list metadata](https://api.aliyun.com/meta/v1/products/adb/versions/2021-12-01/api-docs.json)
- [Single API definition metadata](https://api.aliyun.com/meta/v1/products/adb/versions/2021-12-01/apis/{ApiName}/api.json)
- [Sources](references/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated JSON or Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save API inventory artifacts and response summaries under output/alicloud-database-analyticdb-mysql/.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
