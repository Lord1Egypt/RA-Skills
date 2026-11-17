## Description:

Use when managing Alibaba Cloud PAI AIWorkspace (AIWorkSpace) via OpenAPI/SDK, including the user is operating AIWorkspace resources such as workspace/project inventory, create/update actions, status queries, permission or configuration troubleshooting, or automation around PAI workspace lifecycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud PAI AIWorkspace resources through OpenAPI or SDK workflows, including inventory, create/update actions, status checks, permission troubleshooting, and automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud mutating operations can create, update, modify, or set PAI AIWorkspace resources incorrectly if the region, resource identifiers, or desired action are wrong.

Mitigation: Confirm region, resource identifiers, and desired action before mutating operations, and use describe or list APIs to verify results.

Risk: Alibaba Cloud credentials can grant access to live cloud resources.

Mitigation: Use least-privilege Alibaba Cloud credentials and review proposed create, update, modify, or set operations before execution.

Risk: Saved API responses and generated artifacts may contain operational details.

Mitigation: Keep generated outputs under output/aliyun-pai-workspace/ as documented and review artifacts before sharing them.

## Reference(s):

- [Skill sources](references/sources.md)
- [Alibaba Cloud AIWorkSpace OpenAPI product page](https://api.aliyun.com/product/AIWorkSpace)
- [AIWorkSpace 2021-02-04 API metadata](https://api.aliyun.com/meta/v1/products/AIWorkSpace/versions/2021-02-04/api-docs.json)
- [AIWorkSpace single API metadata template](https://api.aliyun.com/meta/v1/products/AIWorkSpace/versions/2021-02-04/apis/{ApiName}/api.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown with inline bash code blocks, API call guidance, and generated artifact file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated outputs and API response summaries should be saved under output/aliyun-pai-workspace/.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
