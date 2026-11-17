## Description:

Manages Alibaba Cloud AIRec recommendation resources through OpenAPI and SDK workflows, including inventory, create and update operations, status inspection, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to manage Alibaba Cloud AIRec resources, discover supported APIs, execute resource operations, and collect troubleshooting evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Overbroad Alibaba Cloud credentials or unreviewed mutating API calls could change AIRec resources unexpectedly.

Mitigation: Use least-privilege credentials, confirm region and resource identifiers, and review Create, Update, Modify, and Set calls before execution.

Risk: Generated API inventories and response summaries may contain operational details.

Mitigation: Keep generated artifacts in the declared output directory and review contents before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-airec-manage)
- [Sources](references/sources.md)
- [Alibaba Cloud AIRec OpenAPI product page](https://api.aliyun.com/product/Airec)
- [AIRec API metadata list](https://api.aliyun.com/meta/v1/products/Airec/versions/2020-11-26/api-docs.json)
- [AIRec single API metadata definition](https://api.aliyun.com/meta/v1/products/Airec/versions/2020-11-26/apis/{ApiName}/api.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, and generated JSON or Markdown artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts are expected under output/aliyun-airec-manage/.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
