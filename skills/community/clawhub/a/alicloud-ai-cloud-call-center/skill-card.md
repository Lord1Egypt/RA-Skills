## Description: <br>
Manage Alibaba Cloud Cloud Call Center (CCC) via OpenAPI/SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations teams use this skill to discover Alibaba Cloud Cloud Call Center APIs, manage CCC resources, update configuration, check status, and troubleshoot call-center API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through credentialed Alibaba Cloud CCC changes. <br>
Mitigation: Use least-privilege RAM credentials and prefer a test or non-production account before using it against production resources. <br>
Risk: Create, Update, Modify, Set, or Delete-style operations may change call-center resources or configuration. <br>
Mitigation: Require explicit user approval before any mutating operation and verify results with describe or list APIs. <br>
Risk: Generated artifacts or API responses may include operational details. <br>
Mitigation: Restrict saved output to output/alicloud-ai-cloud-call-center/ and review artifacts before sharing them. <br>


## Reference(s): <br>
- [Alibaba Cloud CCC OpenAPI product page](https://api.aliyun.com/product/CCC) <br>
- [Alibaba Cloud CCC API metadata list](https://api.aliyun.com/meta/v1/products/CCC/versions/2020-07-01/api-docs.json) <br>
- [Alibaba Cloud CCC single API metadata template](https://api.aliyun.com/meta/v1/products/CCC/versions/2020-07-01/apis/{ApiName}/api.json) <br>
- [ClawHub skill page](https://clawhub.ai/cinience/alicloud-ai-cloud-call-center) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell commands and generated JSON or Markdown artifact paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write API inventory artifacts under output/alicloud-ai-cloud-call-center/ when the helper script is used.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence; bundled skill frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
