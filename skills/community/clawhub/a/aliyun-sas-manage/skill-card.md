## Description:

Use when managing Alibaba Cloud Security Center (Sas) via OpenAPI/SDK, including the user needs Security Center resource operations, configuration updates, status queries, and troubleshooting Sas API or security workflow issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security operators use this skill to manage Alibaba Cloud Security Center resources through Alibaba Cloud OpenAPI or SDK workflows, including inventory, configuration changes, status checks, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutating Alibaba Cloud Security Center operations can change security resources or configuration in the selected account and region.

Mitigation: Use least-privilege credentials, review the target region and resource identifiers, and require explicit confirmation before Create, Update, Modify, or Set operations in production.

Risk: Saved API responses and evidence files may include operational security details such as regions, resource identifiers, or API response summaries.

Mitigation: Write outputs only under output/aliyun-sas-manage/, control access to generated files, and redact sensitive details before sharing evidence externally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-sas-manage)
- [Sources](references/sources.md)
- [Alibaba Cloud OpenAPI Security Center product page](https://api.aliyun.com/product/Sas)
- [Alibaba Cloud Security Center API metadata](https://api.aliyun.com/meta/v1/products/Sas/versions/2021-01-14/api-docs.json)
- [Alibaba Cloud Security Center single API metadata](https://api.aliyun.com/meta/v1/products/Sas/versions/2021-01-14/apis/{ApiName}/api.json)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, API calls, markdown]

**Output Format:** [Markdown guidance with shell commands, configuration notes, and generated JSON or Markdown API inventory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts should be written under output/aliyun-sas-manage/.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
