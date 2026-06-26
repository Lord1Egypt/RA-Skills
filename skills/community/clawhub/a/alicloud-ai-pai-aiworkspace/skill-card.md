## Description: <br>
Manage Alibaba Cloud PAI AIWorkspace (AIWorkSpace) via OpenAPI/SDK for workspace and project inventory, lifecycle actions, status queries, permission troubleshooting, configuration troubleshooting, and automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Alibaba Cloud PAI AIWorkspace resources, discover API metadata, prepare OpenAPI or SDK calls, and save command outputs or API response summaries for reproducibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use Alibaba Cloud credentials to perform management actions against AIWorkspace resources. <br>
Mitigation: Use least-privilege AccessKeys and review any create, update, modify, or set operation before execution. <br>
Risk: Running with the wrong Alibaba Cloud region can target unintended resources or produce misleading results. <br>
Mitigation: Set the intended region explicitly or ask the user to confirm the region before mutating operations. <br>
Risk: Saved outputs may include resource IDs or API response details. <br>
Mitigation: Inspect and remove sensitive files under output/alicloud-ai-pai-aiworkspace/ when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/alicloud-ai-pai-aiworkspace) <br>
- [Sources](references/sources.md) <br>
- [Alibaba Cloud AIWorkSpace OpenAPI product page](https://api.aliyun.com/product/AIWorkSpace) <br>
- [AIWorkSpace API metadata](https://api.aliyun.com/meta/v1/products/AIWorkSpace/versions/2021-02-04/api-docs.json) <br>
- [AIWorkSpace single API metadata template](https://api.aliyun.com/meta/v1/products/AIWorkSpace/versions/2021-02-04/apis/{ApiName}/api.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Files, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands plus JSON and Markdown files saved under output/alicloud-ai-pai-aiworkspace/] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Alibaba Cloud AccessKey credentials and region settings supplied by the user or environment.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
