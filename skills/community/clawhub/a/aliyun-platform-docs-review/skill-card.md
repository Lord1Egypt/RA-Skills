## Description:

Reviews Alibaba Cloud product documentation and OpenAPI documentation by product name, then produces scored, evidence-backed improvement recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation owners, and API platform teams use this skill to audit Alibaba Cloud product and OpenAPI documentation for discoverability, completeness, API usability, and prioritized fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The instructions ask users to configure Alibaba Cloud credentials even though the included script only fetches public documentation.

Mitigation: Review the skill before installing in environments that contain Alibaba Cloud credentials, and do not provide cloud access keys unless a future authenticated use case is explicitly documented and scoped.

Risk: The generated review depends on live public documentation and product metadata fetched at run time, so product resolution or coverage may be incomplete.

Mitigation: Review the generated source links, JSON evidence, and prioritized findings before applying documentation or API changes.

## Reference(s):

- [Review rubric](references/review-rubric.md)
- [Alibaba Cloud OpenAPI products metadata (ZH_CN)](https://api.aliyun.com/meta/v1/products.json?language=ZH_CN)
- [Alibaba Cloud OpenAPI products metadata (EN_US)](https://api.aliyun.com/meta/v1/products.json?language=EN_US)
- [Alibaba Cloud product list](https://www.aliyun.com/product/list)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with JSON evidence files and concise response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes review_evidence.json and review_report.md under output/aliyun-platform-docs-review/ for each run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
