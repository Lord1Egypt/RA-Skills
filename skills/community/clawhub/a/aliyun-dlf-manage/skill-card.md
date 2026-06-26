## Description: <br>
Use when managing Alibaba Cloud Data Lake Formation (DataLake) via OpenAPI/SDK, including the user asks for DataLake catalog resource operations, configuration updates, status queries, or troubleshooting DataLake API workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Alibaba Cloud Data Lake Formation catalog resources, configuration, status checks, and troubleshooting workflows through OpenAPI, SDKs, or OpenAPI Explorer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alibaba Cloud credentials can authorize changes to Data Lake Formation resources if used with excessive permissions. <br>
Mitigation: Use least-privilege credentials and verify the active account, region, and resource identifiers before API use. <br>
Risk: Mutating API calls may alter catalog resources or configuration. <br>
Mitigation: Require explicit user approval before create, update, modify, set, or other mutating operations. <br>
Risk: Files written under output/aliyun-dlf-manage/ may contain operational metadata. <br>
Mitigation: Review generated output files before sharing, committing, or reusing them. <br>


## Reference(s): <br>
- [Sources](references/sources.md) <br>
- [Alibaba Cloud DataLake OpenAPI product page](https://api.aliyun.com/product/DataLake) <br>
- [DataLake OpenAPI metadata API list](https://api.aliyun.com/meta/v1/products/DataLake/versions/2020-07-10/api-docs.json) <br>
- [DataLake OpenAPI single API definition template](https://api.aliyun.com/meta/v1/products/DataLake/versions/2020-07-10/apis/{ApiName}/api.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, API calls, files] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON or Markdown artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves API inventory and response evidence under output/aliyun-dlf-manage/ when file output is needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
