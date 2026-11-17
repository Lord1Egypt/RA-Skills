## Description:

Manage Alibaba Cloud Quan Miao (AiMiaoBi) via OpenAPI/SDK for resource listing, configuration changes, runtime status queries, and API or workflow diagnosis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud Quan Miao resources through OpenAPI metadata, SDK calls, and OpenAPI Explorer workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents toward Alibaba Cloud Create, Update, Modify, or Set operations that change cloud resources.

Mitigation: Use least-privilege Alibaba Cloud credentials and review all mutating operations before execution.

Risk: Saved API responses or generated artifacts may contain account-specific cloud details.

Mitigation: Keep generated response artifacts under the skill output directory and avoid sharing them when they contain sensitive details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/alicloud-ai-content-aimiaobi)
- [OpenAPI product page](https://api.aliyun.com/product/AiMiaoBi)
- [API list metadata](https://api.aliyun.com/meta/v1/products/AiMiaoBi/versions/2023-08-01/api-docs.json)
- [Single API definition metadata](https://api.aliyun.com/meta/v1/products/AiMiaoBi/versions/2023-08-01/apis/{ApiName}/api.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, API parameters, and generated JSON or Markdown artifact paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated API inventory artifacts are written under output/alicloud-ai-content-aimiaobi/ when requested.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
