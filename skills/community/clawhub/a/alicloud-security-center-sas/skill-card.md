## Description:

Manage Alibaba Cloud Security Center (Sas) via OpenAPI/SDK for Security Center resource operations, configuration updates, status queries, and security workflow troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud security operators use this skill to discover Alibaba Cloud Security Center SAS APIs, prepare least-privilege API calls, perform inventory or configuration workflows, and verify results with describe/list/status APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide API calls that create, update, modify, or set Alibaba Cloud Security Center resources.

Mitigation: Use least-privilege Alibaba Cloud credentials and review proposed mutating operations, target regions, and resource IDs before execution.

Risk: Ambiguous region or resource identifiers can lead to operations against the wrong Alibaba Cloud scope.

Mitigation: Explicitly confirm the target region, resource identifiers, and desired action before running API calls; ask the user when the region is unclear.

## Reference(s):

- [Alibaba Cloud Security Center SAS Skill Page](https://clawhub.ai/cinience/skills/alicloud-security-center-sas)
- [OpenAPI product page](https://api.aliyun.com/product/Sas)
- [SAS API list metadata](https://api.aliyun.com/meta/v1/products/Sas/versions/2021-01-14/api-docs.json)
- [SAS single API definition metadata](https://api.aliyun.com/meta/v1/products/Sas/versions/2021-01-14/apis/{ApiName}/api.json)
- [sources.md](references/sources.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, markdown, JSON]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON or Markdown output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write API inventory artifacts and response summaries under output/alicloud-security-center-sas/.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
