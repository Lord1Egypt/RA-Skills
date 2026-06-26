## Description: <br>
Manage Alibaba Cloud Backup and Disaster Recovery Center (BDRC) via OpenAPI/SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and cloud administrators use this skill to inventory, configure, check status, and troubleshoot Alibaba Cloud Backup and Disaster Recovery Center resources through OpenAPI/SDK workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward Alibaba Cloud BDRC operations that create, update, modify, or set cloud resources. <br>
Mitigation: Use a dedicated least-privilege AccessKey and explicitly approve any mutating action after verifying the account, region, and resource IDs. <br>
Risk: Generated local files may contain API inventory details or response summaries from the user's cloud environment. <br>
Mitigation: Review or delete files in output/alicloud-backup-bdrc/ before sharing the workspace. <br>


## Reference(s): <br>
- [Alibaba Cloud BDRC OpenAPI Product Page](https://api.aliyun.com/product/BDRC) <br>
- [Alibaba Cloud BDRC API List Metadata](https://api.aliyun.com/meta/v1/products/BDRC/versions/2023-08-08/api-docs.json) <br>
- [Alibaba Cloud BDRC Single API Metadata](https://api.aliyun.com/meta/v1/products/BDRC/versions/2023-08-08/apis/{ApiName}/api.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/cinience/alicloud-backup-bdrc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python snippets, API call guidance, and generated output files when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write API inventory artifacts and response summaries under output/alicloud-backup-bdrc/.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
