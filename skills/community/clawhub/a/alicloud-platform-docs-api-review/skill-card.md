## Description: <br>
Automatically review latest Alibaba Cloud product docs and OpenAPI docs by product name, then output detailed prioritized improvement suggestions with evidence and scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, documentation owners, and API maintainers use this skill to audit Alibaba Cloud product and OpenAPI documentation for a named product and receive scored, prioritized improvement recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The visible docs-review script appears read-only, but the skill asks users to configure Alibaba Cloud access keys and mentions mutating operations. <br>
Mitigation: Review the need for credentials before installing or running the skill; if credentials are required, use tightly scoped read-only keys and avoid mutating operations. <br>
Risk: Generated documentation and API recommendations may be incomplete, stale, or misleading. <br>
Mitigation: Review generated findings, source links, and scores before using the recommendations for product or API documentation changes. <br>


## Reference(s): <br>
- [Review Rubric](references/review-rubric.md) <br>
- [Alibaba Cloud OpenAPI Product Metadata (Chinese)](https://api.aliyun.com/meta/v1/products.json?language=ZH_CN) <br>
- [Alibaba Cloud OpenAPI Product Metadata (English)](https://api.aliyun.com/meta/v1/products.json?language=EN_US) <br>
- [Alibaba Cloud Product List](https://www.aliyun.com/product/list) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown report with JSON evidence files and concise user-facing summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes review_evidence.json and review_report.md under output/alicloud-platform-docs-api-review/ when the bundled script is run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
