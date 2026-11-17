## Description:

Helps agents manage Alibaba Cloud Data Lake Formation (DlfNext) resources through OpenAPI/SDK workflows, including discovery, create/update flows, status checks, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inventory, configure, and troubleshoot Alibaba Cloud Data Lake Formation (DlfNext) catalog and governance resources through OpenAPI metadata, SDK calls, and OpenAPI Explorer workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Create, update, modify, or set operations may change Alibaba Cloud DlfNext resource state.

Mitigation: Require explicit review before mutating operations and confirm the target region, resource identifiers, and intended action.

Risk: Overbroad or misdirected cloud credentials can expose resources outside the intended task.

Mitigation: Use least-privilege Alibaba Cloud credentials and verify credential source and region before executing API calls.

## Reference(s):

- [Sources](references/sources.md)
- [Alibaba Cloud OpenAPI DlfNext product page](https://api.aliyun.com/product/DlfNext)
- [DlfNext OpenAPI metadata API list](https://api.aliyun.com/meta/v1/products/DlfNext/versions/2025-03-10/api-docs.json)
- [DlfNext single API definition metadata](https://api.aliyun.com/meta/v1/products/DlfNext/versions/2025-03-10/apis/{ApiName}/api.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON or Markdown artifact files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated API inventory artifacts are written under output/aliyun-dlf-manage-next/ when the metadata discovery script is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
