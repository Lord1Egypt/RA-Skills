## Description: <br>
Manage Alibaba Cloud Quan Miao (AiMiaoBi) via OpenAPI/SDK for content operations, including resource listing, configuration changes, runtime status queries, and API or workflow diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to discover and run Alibaba Cloud AiMiaoBi OpenAPI workflows, inspect resources, update configurations, check service status, and troubleshoot API failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide live Alibaba Cloud operations, including create, update, modify, set, and delete-style actions. <br>
Mitigation: Use least-privilege Alibaba Cloud credentials and explicitly confirm the region, resource ID, and intended change before any mutating operation. <br>
Risk: Incorrect region or resource identifiers can cause changes against the wrong Alibaba Cloud resource. <br>
Mitigation: Start with read-only list or describe APIs, record key parameters in evidence files, and verify results before making changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/alicloud-ai-content-aimiaobi) <br>
- [OpenAPI product page: AiMiaoBi](https://api.aliyun.com/product/AiMiaoBi) <br>
- [AiMiaoBi API list metadata](https://api.aliyun.com/meta/v1/products/AiMiaoBi/versions/2023-08-01/api-docs.json) <br>
- [AiMiaoBi single API metadata template](https://api.aliyun.com/meta/v1/products/AiMiaoBi/versions/2023-08-01/apis/{ApiName}/api.json) <br>
- [Artifact sources](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, markdown, API Calls] <br>
**Output Format:** [Markdown guidance with shell commands, Python snippets, JSON/API response summaries, and saved artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated or fetched artifacts should be saved under output/alicloud-ai-content-aimiaobi/.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
