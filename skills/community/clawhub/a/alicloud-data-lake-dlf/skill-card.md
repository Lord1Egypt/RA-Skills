## Description: <br>
Manage Alibaba Cloud Data Lake Formation (DataLake) via OpenAPI/SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to discover Alibaba Cloud Data Lake Formation APIs, manage DataLake catalog resources, update configuration, query status, and troubleshoot API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alibaba Cloud credentials may be exposed or overprivileged during API workflows. <br>
Mitigation: Use least-privilege or short-lived credentials, prefer environment variables, and avoid sharing saved outputs until reviewed. <br>
Risk: Create, update, modify, or set operations can change cloud resources. <br>
Mitigation: Confirm region, resource identifiers, and intended changes before running mutating API calls, then verify results with describe or list APIs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/alicloud-data-lake-dlf) <br>
- [OpenAPI product page](https://api.aliyun.com/product/DataLake) <br>
- [DataLake API metadata](https://api.aliyun.com/meta/v1/products/DataLake/versions/2020-07-10/api-docs.json) <br>
- [DataLake API definition template](https://api.aliyun.com/meta/v1/products/DataLake/versions/2020-07-10/apis/{ApiName}/api.json) <br>
- [sources.md](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and code snippets; optional JSON and Markdown files under output/alicloud-data-lake-dlf/] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save API inventory artifacts and response summaries for reproducibility.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
