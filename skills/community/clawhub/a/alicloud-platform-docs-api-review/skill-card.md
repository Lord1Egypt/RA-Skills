## Description:

Automatically reviews Alibaba Cloud product documentation and OpenAPI documentation by product name, then produces prioritized improvement suggestions with evidence and scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation owners, and API platform teams use this skill to audit Alibaba Cloud product and API documentation for completeness, usability, and actionable improvement opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to configure Alibaba Cloud credentials even though the reviewed implementation fetches public documentation and does not need cloud access keys.

Mitigation: Do not provide Alibaba Cloud access keys for this version; remove or tightly scope the credential prerequisite before routine use.

## Reference(s):

- [Alibaba Cloud documentation review rubric](references/review-rubric.md)
- [Alibaba Cloud OpenAPI product metadata (Chinese)](https://api.aliyun.com/meta/v1/products.json?language=ZH_CN)
- [Alibaba Cloud OpenAPI product metadata (English)](https://api.aliyun.com/meta/v1/products.json?language=EN_US)
- [Alibaba Cloud product list](https://www.aliyun.com/product/list)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report and JSON evidence files, with concise text guidance for the agent response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes review_evidence.json and review_report.md under output/alicloud-platform-docs-api-review/.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
