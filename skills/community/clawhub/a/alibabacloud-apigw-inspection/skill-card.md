## Description: <br>
Performs inspection of Alibaba Cloud Cloud-Native API Gateway, AI Gateway, and dedicated API Gateway instances by querying instance details and monitoring metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to inspect Alibaba Cloud gateway health, confirm resource utilization, and prepare metric-backed inspection reports for CPU, memory, connections, network IO, bandwidth, rate limiting, traffic, and QPS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires local Aliyun CLI and plugin installation or update steps before inspection. <br>
Mitigation: Approve each local install or plugin update explicitly, and avoid automatic global plugin changes unless they are acceptable for the environment. <br>
Risk: The workflow depends on Alibaba Cloud credentials and cloud API queries. <br>
Mitigation: Use temporary or tightly scoped read-only RAM credentials, avoid broad AccessKeys, and approve each cloud query before execution. <br>
Risk: Credential setup guidance can lead to persistent local credentials if followed without review. <br>
Mitigation: Configure credentials outside the agent session, never reveal secret values, and remove or rotate credentials when inspection is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-apigw-inspection) <br>
- [RAM Permission Policy](references/ram-policies.md) <br>
- [Inspection Verification Method](references/verification-method.md) <br>
- [Related Commands](references/related-commands.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [AI Gateway available regions](https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/supported-regions) <br>
- [Cloud-Native API Gateway available regions](https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/product-overview/regions) <br>
- [API Gateway endpoint reference](https://help.aliyun.com/zh/api-gateway/traditional-api-gateway/developer-reference/api-cloudapi-2016-07-14-endpoint) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown inspection report with Alibaba Cloud CLI commands and metric summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-confirmed product type, region, instance ID, and time range before cloud queries.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
