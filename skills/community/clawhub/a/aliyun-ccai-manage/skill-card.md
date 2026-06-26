## Description: <br>
Use when managing Alibaba Cloud Contact Center AI (ContactCenterAI) via OpenAPI/SDK, including resource lifecycle operations, configuration changes, status queries, and troubleshooting failed ContactCenterAI API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to discover Alibaba Cloud Contact Center AI OpenAPI metadata, plan resource operations, run SDK or OpenAPI Explorer workflows, and verify results with describe or list APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent run credentialed Alibaba Cloud commands that create, change, delete, scale, or incur charges. <br>
Mitigation: Use least-privilege RAM credentials, prefer temporary credentials where possible, and require explicit review before any mutating or billable command runs. <br>
Risk: Incorrect region or resource identifiers can cause operations to target the wrong Contact Center AI resources. <br>
Mitigation: Confirm region, resource identifiers, and intended action before execution; ask the user when the region is unclear. <br>


## Reference(s): <br>
- [OpenAPI product page](https://api.aliyun.com/product/ContactCenterAI) <br>
- [ContactCenterAI API list metadata](https://api.aliyun.com/meta/v1/products/ContactCenterAI/versions/2024-06-03/api-docs.json) <br>
- [ContactCenterAI single API metadata](https://api.aliyun.com/meta/v1/products/ContactCenterAI/versions/2024-06-03/apis/{ApiName}/api.json) <br>
- [ClawHub release page](https://clawhub.ai/cinience/aliyun-ccai-manage) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and generated JSON or Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write API inventory artifacts under output/aliyun-ccai-manage/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
