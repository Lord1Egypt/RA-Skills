## Description: <br>
Manage Alibaba Cloud Data Lake Formation (DlfNext) resources via OpenAPI and SDK workflows, including discovery, listing, updates, status checks, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Alibaba Cloud DLF Next catalog and governance resources, discover API schemas, run inventory and status checks, and plan controlled resource changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud credentials and mutating DLF Next operations can change Alibaba Cloud resources. <br>
Mitigation: Use a least-privilege RAM user or role and explicitly approve create, update, modify, or set operations before execution. <br>
Risk: Incorrect region or resource identifiers can target the wrong DLF Next resources. <br>
Mitigation: Confirm the region and resource IDs before API calls, then verify results with describe or list APIs. <br>


## Reference(s): <br>
- [Alibaba Cloud DLF Next OpenAPI product page](https://api.aliyun.com/product/DlfNext) <br>
- [DLF Next OpenAPI metadata API list](https://api.aliyun.com/meta/v1/products/DlfNext/versions/2025-03-10/api-docs.json) <br>
- [DLF Next OpenAPI single API definition template](https://api.aliyun.com/meta/v1/products/DlfNext/versions/2025-03-10/apis/{ApiName}/api.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated JSON or Markdown API inventory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write API inventory artifacts under output/alicloud-data-lake-dlf-next/.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
