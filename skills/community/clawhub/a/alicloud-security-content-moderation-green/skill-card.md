## Description: <br>
Manage Alibaba Cloud Content Moderation (Green) via OpenAPI/SDK for resource and policy operations, status inspection, and moderation workflow troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to discover Alibaba Cloud Content Moderation APIs, manage moderation resources and policies, and troubleshoot moderation workflow failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward Alibaba Cloud Content Moderation create, update, modify, or set operations. <br>
Mitigation: Use least-privilege Alibaba Cloud credentials and require explicit user confirmation before any mutating cloud action. <br>
Risk: Generated output files may include internal cloud resource details or API response summaries. <br>
Mitigation: Review generated files under output/alicloud-security-content-moderation-green/ and delete or protect sensitive artifacts after use. <br>
Risk: Running the skill without a clear region can target an unintended Alibaba Cloud region. <br>
Mitigation: Confirm the region before execution when ALICLOUD_REGION_ID is unset or ambiguous. <br>


## Reference(s): <br>
- [Alibaba Cloud OpenAPI product page for Green](https://api.aliyun.com/product/Green) <br>
- [Alibaba Cloud Green API metadata list](https://api.aliyun.com/meta/v1/products/Green/versions/2022-09-26/api-docs.json) <br>
- [Alibaba Cloud Green single API metadata endpoint](https://api.aliyun.com/meta/v1/products/Green/versions/2022-09-26/apis/{ApiName}/api.json) <br>
- [ClawHub release page](https://clawhub.ai/cinience/alicloud-security-content-moderation-green) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration notes, and generated local JSON or Markdown inventory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write API inventory and evidence files under output/alicloud-security-content-moderation-green/.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
