## Description: <br>
Helps agents manage Alibaba Cloud AIRec resources through OpenAPI or SDK workflows, including discovery, list/create/update operations, status inspection, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to guide AIRec resource management in Alibaba Cloud, including metadata-first API discovery, credential setup, resource changes, and validation of results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide credentialed Alibaba Cloud AIRec API actions, including create, update, modify, and set operations. <br>
Mitigation: Use least-privilege Alibaba Cloud credentials and require explicit approval before mutating resources. <br>
Risk: Incorrect region or resource identifiers could cause operations against unintended AIRec resources. <br>
Mitigation: Confirm region, resource IDs, and intended action before execution, and use describe/list APIs to verify results. <br>
Risk: Saved API responses or generated artifacts may contain operational details that should not be shared broadly. <br>
Mitigation: Review files written under output/aliyun-airec-manage/ before sharing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cinience/aliyun-airec-manage) <br>
- [Alibaba Cloud AIRec OpenAPI product page](https://api.aliyun.com/product/Airec) <br>
- [AIRec API list metadata](https://api.aliyun.com/meta/v1/products/Airec/versions/2020-11-26/api-docs.json) <br>
- [AIRec single API metadata template](https://api.aliyun.com/meta/v1/products/Airec/versions/2020-11-26/apis/{ApiName}/api.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, plus JSON and Markdown files under output/aliyun-airec-manage/ when metadata is fetched.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Metadata inventory artifacts may include API names, source URLs, region or resource identifiers, and validation evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
