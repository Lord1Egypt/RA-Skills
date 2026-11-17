## Description:

Use when managing Alibaba Cloud Intelligent Cloud Editing (ICE) media workflows via OpenAPI/SDK, including media processing jobs, template/workflow orchestration, editing and production pipelines, and job status troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media operations engineers use this skill to discover Alibaba Cloud ICE OpenAPI operations, validate workflow prerequisites, submit or monitor media processing jobs, and collect execution evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved output may contain secrets, signed URLs, customer data, or sensitive media metadata.

Mitigation: Review files under output/aliyun-ice-manage/ before retaining, sharing, or committing them.

Risk: ICE workflow and job operations can affect cloud media processing resources.

Mitigation: Use least-privilege RAM or STS credentials, confirm the region and workflow scope, and query current state with read-only APIs before mutation.

## Reference(s):

- [Alibaba Cloud ICE product documentation](https://www.alibabacloud.com/help/en/ice)
- [Alibaba Cloud ICE OpenAPI product page](https://api.aliyun.com/product/ice)
- [Alibaba Cloud ICE OpenAPI metadata](https://api.aliyun.com/meta/v1/products/ice/versions/2020-11-09/api-docs.json)
- [Source list](references/sources.md)
- [ICE task templates](references/templates.md)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-ice-manage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, API operation names, configuration notes, and saved evidence file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs generated API inventory and execution evidence to output/aliyun-ice-manage/.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
