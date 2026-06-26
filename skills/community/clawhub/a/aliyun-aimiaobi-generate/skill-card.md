## Description: <br>
Use when managing Alibaba Cloud Quan Miao (AiMiaoBi) via OpenAPI/SDK, including the user asks for Alibaba Cloud MiaoBi content operations, including listing resources, creating/updating configurations, querying runtime status, and diagnosing API or workflow failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to discover Alibaba Cloud AiMiaoBi OpenAPI metadata, manage Quan Miao resources, update configurations, query runtime status, and diagnose API or workflow failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud resource changes may create, update, modify, or set Alibaba Cloud AiMiaoBi resources. <br>
Mitigation: Use least-privilege Alibaba Cloud credentials, confirm target region and resource IDs, and require explicit approval plus a clear summary before mutating operations. <br>
Risk: Incorrect region or resource identifiers may lead to actions against the wrong cloud resources. <br>
Mitigation: Ask for clarification when the region is unclear and verify results with describe or list APIs after operations. <br>


## Reference(s): <br>
- [Skill sources](references/sources.md) <br>
- [Alibaba Cloud AiMiaoBi OpenAPI product page](https://api.aliyun.com/product/AiMiaoBi) <br>
- [AiMiaoBi OpenAPI metadata](https://api.aliyun.com/meta/v1/products/AiMiaoBi/versions/2023-08-01/api-docs.json) <br>
- [AiMiaoBi single API definition metadata](https://api.aliyun.com/meta/v1/products/AiMiaoBi/versions/2023-08-01/apis/{ApiName}/api.json) <br>
- [ClawHub skill page](https://clawhub.ai/cinience/aliyun-aimiaobi-generate) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated JSON or Markdown artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated artifacts should be saved under output/aliyun-aimiaobi-generate/ with key parameters recorded for reproducibility.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
