## Description: <br>
Manage Alibaba Cloud Flink VVP instances and namespaces through create and query operations only, including regions, zones, tags, and namespace lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to create or query Alibaba Cloud Flink VVP instances, namespaces, regions, zones, and tags through a scoped wrapper workflow. It is not intended for Flink SQL, job execution, update/delete operations, or unrelated Alibaba Cloud services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create billable Alibaba Cloud Flink resources. <br>
Mitigation: Use a dedicated least-privilege RAM role or user and review every create command before providing the required confirmation flag. <br>
Risk: Cloud credentials could be exposed or overprivileged if handled manually. <br>
Mitigation: Use the default credential chain or RAM roles, avoid plaintext AccessKey or SecretKey values in prompts and outputs, and apply only the documented Flink RAM actions. <br>
Risk: Requests outside the supported create/query scope could lead to inappropriate cloud operations or misleading results. <br>
Mitigation: Limit use to Flink VVP instance and namespace create/query workflows, reject update/delete, Flink SQL/job, and unrelated cloud-service requests, and verify create outcomes with read-back checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-flink-instance-manage) <br>
- [Quick Start](references/quick-start.md) <br>
- [Core Execution Flow](references/core-execution-flow.md) <br>
- [Command Templates](references/command-templates.md) <br>
- [Parameter Validation](references/parameter-validation.md) <br>
- [Required Confirmation Model](references/required-confirmation-model.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related APIs](references/related-apis.md) <br>
- [Alibaba Cloud Flink OpenAPI overview](https://help.aliyun.com/zh/flink/realtime-flink/developer-reference/api-foasconsole-2021-10-28-overview) <br>
- [Alibaba Cloud Flink OpenAPI RAM actions](https://help.aliyun.com/zh/flink/realtime-flink/developer-reference/api-foasconsole-2021-10-28-ram) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Create operations require explicit confirmation and read-back verification; query operations return JSON with success, operation, data, and request_id fields.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
