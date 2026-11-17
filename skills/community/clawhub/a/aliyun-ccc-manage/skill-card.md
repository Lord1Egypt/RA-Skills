## Description:

Helps agents manage Alibaba Cloud Cloud Call Center (CCC) through Alibaba Cloud OpenAPI/SDK workflows, including resource operations, configuration updates, status checks, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to discover Alibaba Cloud CCC APIs, prepare SDK or OpenAPI Explorer calls, and manage call-center resources. It emphasizes confirming regions, resource IDs, and credentials before live operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live Alibaba Cloud CCC configuration changes using Alibaba credentials.

Mitigation: Use least-privilege credentials and review the region, resource IDs, and intended action before every write operation.

Risk: Saved output artifacts may contain operational resource details.

Mitigation: Store outputs only in the designated output/aliyun-ccc-manage/ directory and treat them as access-controlled operational evidence.

## Reference(s):

- [Alibaba Cloud OpenAPI CCC product page](https://api.aliyun.com/product/CCC)
- [CCC 2020-07-01 API metadata list](https://api.aliyun.com/meta/v1/products/CCC/versions/2020-07-01/api-docs.json)
- [CCC single API metadata endpoint](https://api.aliyun.com/meta/v1/products/CCC/versions/2020-07-01/apis/{ApiName}/api.json)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-ccc-manage)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and generated JSON or Markdown evidence files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write API inventory and evidence artifacts under output/aliyun-ccc-manage/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
