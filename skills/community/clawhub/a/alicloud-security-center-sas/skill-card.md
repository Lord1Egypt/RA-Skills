## Description: <br>
Manage Alibaba Cloud Security Center (Sas) via OpenAPI/SDK for Security Center resource operations, configuration updates, status queries, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud operators, and security engineers use this skill to discover Alibaba Cloud Security Center APIs, prepare SDK or OpenAPI Explorer calls, manage Security Center resources, and verify results with list, describe, get, or query operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide create, update, modify, or set operations against Alibaba Cloud Security Center resources. <br>
Mitigation: Use a dedicated least-privilege Alibaba Cloud AccessKey and confirm mutating actions before execution. <br>
Risk: Discovery output can contain security-resource details. <br>
Mitigation: Review files under output/alicloud-security-center-sas/ before sharing them. <br>
Risk: Running without a clear region can target the wrong Alibaba Cloud region. <br>
Mitigation: Confirm the intended region before mutating operations when ALICLOUD_REGION_ID is unset or ambiguous. <br>


## Reference(s): <br>
- [OpenAPI product page for Sas](https://api.aliyun.com/product/Sas) <br>
- [Sas 2021-01-14 API metadata list](https://api.aliyun.com/meta/v1/products/Sas/versions/2021-01-14/api-docs.json) <br>
- [Sas API definition metadata template](https://api.aliyun.com/meta/v1/products/Sas/versions/2021-01-14/apis/{ApiName}/api.json) <br>
- [ClawHub skill page](https://clawhub.ai/cinience/alicloud-security-center-sas) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration notes, and generated JSON or Markdown discovery files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes API inventory artifacts under output/alicloud-security-center-sas/ when its discovery script is run.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
