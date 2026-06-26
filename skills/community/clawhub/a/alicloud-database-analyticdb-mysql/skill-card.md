## Description: <br>
Manage Alibaba Cloud AnalyticDB for MySQL (ADB) via OpenAPI/SDK for resource lifecycle and configuration operations, status checks, and troubleshooting ADB API and cluster workflow issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to discover Alibaba Cloud AnalyticDB for MySQL APIs, run inventory or status checks, and prepare create, update, modify, set, or delete operations with explicit review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide create, update, modify, set, or delete operations that affect billable Alibaba Cloud resources. <br>
Mitigation: Use least-privilege RAM credentials and require explicit approval before mutating operations. <br>
Risk: Incorrect region or resource identifiers can cause actions to target the wrong AnalyticDB resources. <br>
Mitigation: Confirm region and resource IDs before API calls, and ask the user when the region is unclear. <br>


## Reference(s): <br>
- [OpenAPI product page](https://api.aliyun.com/product/adb) <br>
- [AnalyticDB for MySQL API metadata list](https://api.aliyun.com/meta/v1/products/adb/versions/2021-12-01/api-docs.json) <br>
- [AnalyticDB for MySQL single API metadata template](https://api.aliyun.com/meta/v1/products/adb/versions/2021-12-01/apis/{ApiName}/api.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON or Markdown output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated API inventory artifacts are saved under output/alicloud-database-analyticdb-mysql/ when the helper script is run.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
