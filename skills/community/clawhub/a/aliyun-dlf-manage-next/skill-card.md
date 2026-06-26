## Description: <br>
Use when managing Alibaba Cloud Data Lake Formation (DlfNext) via OpenAPI/SDK, including DLF Next catalog and governance resource operations, listing resources, create/update flows, status checks, and troubleshooting metadata workflow issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Alibaba Cloud Data Lake Formation Next resources through OpenAPI or SDK workflows, including inventory, configuration changes, status checks, and metadata troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide real Alibaba Cloud DLF Next resource changes when used with cloud credentials. <br>
Mitigation: Use least-privilege credentials and require explicit confirmation of the account, region, resource IDs, and intended action before any create, update, modify, set, or other mutating API call. <br>
Risk: Using an incorrect region or resource identifier can lead to misleading results or changes in the wrong environment. <br>
Mitigation: Confirm region and resource identifiers before execution, and verify outcomes with describe or list APIs after each operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/aliyun-dlf-manage-next) <br>
- [Sources](references/sources.md) <br>
- [Alibaba Cloud DlfNext OpenAPI product page](https://api.aliyun.com/product/DlfNext) <br>
- [DlfNext API metadata list](https://api.aliyun.com/meta/v1/products/DlfNext/versions/2025-03-10/api-docs.json) <br>
- [DlfNext API definition template](https://api.aliyun.com/meta/v1/products/DlfNext/versions/2025-03-10/apis/{ApiName}/api.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files] <br>
**Output Format:** [Markdown with inline shell commands, configuration guidance, Python helper scripts, and saved JSON or Markdown artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated artifacts and API response summaries should be saved under output/aliyun-dlf-manage-next/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
