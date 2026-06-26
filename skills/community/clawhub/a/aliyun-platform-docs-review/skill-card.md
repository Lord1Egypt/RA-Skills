## Description: <br>
Reviews Alibaba Cloud product documentation and OpenAPI documentation by product name, producing scored findings, evidence, and prioritized P0/P1/P2 improvement recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Documentation owners, API platform teams, developers, and technical writers use this skill to review Alibaba Cloud product and API documentation quality, collect source evidence, and prioritize fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the skill asks users to configure Alibaba Cloud access keys even though the visible workflow fetches public documentation pages. <br>
Mitigation: Run the review without credentials when possible, and do not provide Alibaba Cloud access keys unless the publisher documents why they are needed, which read-only permissions are required, and what operations will use them. <br>
Risk: The script fetches live Alibaba Cloud product pages and OpenAPI metadata, so results can change when remote documentation changes or is unavailable. <br>
Mitigation: Review the generated source links and JSON evidence before relying on recommendations, and rerun the review when documentation versions or source availability change. <br>


## Reference(s): <br>
- [Review Rubric](references/review-rubric.md) <br>
- [Alibaba Cloud OpenAPI products metadata (Chinese)](https://api.aliyun.com/meta/v1/products.json?language=ZH_CN) <br>
- [Alibaba Cloud OpenAPI products metadata (English)](https://api.aliyun.com/meta/v1/products.json?language=EN_US) <br>
- [Alibaba Cloud product list](https://www.aliyun.com/product/list) <br>
- [ClawHub skill page](https://clawhub.ai/cinience/aliyun-platform-docs-review) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, JSON, guidance, shell commands] <br>
**Output Format:** [Markdown report plus JSON evidence files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes review_report.md and review_evidence.json under output/aliyun-platform-docs-review/ for each run.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
