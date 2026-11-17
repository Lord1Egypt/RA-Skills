## Description:

Manage Alibaba Cloud Data Lake Formation (DlfNext) via OpenAPI/SDK. Use whenever the user needs DLF Next catalog/governance resource operations, including listing resources, create/update flows, status checks, and troubleshooting metadata workflow issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to discover Alibaba Cloud DLF Next OpenAPI metadata, plan catalog and governance operations, and verify resource state after list, describe, create, update, or troubleshooting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help perform Alibaba Cloud DLF Next operations that modify cloud resources.

Mitigation: Use least-privilege, preferably short-lived credentials, and confirm the region, resource identifiers, and intended action before any mutation.

Risk: Generated output files may contain cloud metadata or API response details.

Mitigation: Review files written under output/alicloud-data-lake-dlf-next/ before sharing, retaining, or using them as evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/alicloud-data-lake-dlf-next)
- [Sources](references/sources.md)
- [OpenAPI product page](https://api.aliyun.com/product/DlfNext)
- [DlfNext API list metadata](https://api.aliyun.com/meta/v1/products/DlfNext/versions/2025-03-10/api-docs.json)
- [DlfNext single API definition metadata](https://api.aliyun.com/meta/v1/products/DlfNext/versions/2025-03-10/apis/{ApiName}/api.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, API Calls, Files]

**Output Format:** [Markdown guidance with bash commands and generated JSON or Markdown output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API inventory artifacts are written under output/alicloud-data-lake-dlf-next/ when the helper script is run.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
