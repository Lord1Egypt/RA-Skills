## Description: <br>
Performs capacity assessment on Alibaba Cloud Kafka instances to determine whether throttling is occurring and recommends instance upgrades when capacity is running high. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations engineers use this skill to assess Alibaba Cloud Kafka v2 and v3 instance capacity incidents, including consumer lag, producer failures, throughput throttling, connection anomalies, and disk pressure. The skill queries read-only instance metadata and CloudMonitor metrics, then produces a diagnostic report with upgrade recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Alibaba Cloud CLI access, and the bundled CLI guide includes broad credential and administration guidance beyond the Kafka capacity assessment task. <br>
Mitigation: Use a dedicated RAM user with only alikafka:GetInstanceList and cms:DescribeMetricList, configure credentials outside the agent session, and avoid copying command-line secret examples. <br>
Risk: Granting broad Alibaba Cloud permissions would exceed the skill's stated read-only behavior. <br>
Mitigation: Do not grant ECS or full-access policies for this skill; use the minimum RAM policy documented in references/ram-policies.md. <br>
Risk: Kafka instance specifications and limit policies may change after the bundled knowledge base update. <br>
Mitigation: Prefer current official Alibaba Cloud documentation and live OpenAPI or CloudMonitor responses when they conflict with bundled reference material. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-kafka-capacity-assessment) <br>
- [Knowledge Base Notes](references/README.md) <br>
- [Kafka v2 Instance Specification and Capacity Policy](references/kafka-v2-spec-and-capacity.md) <br>
- [Kafka v3 Instance Specification, Elastic Strategy, and Capacity Policy](references/kafka-v3-spec-and-capacity.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related Commands](references/related-commands.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Alibaba Cloud Kafka Instance Editions](https://help.aliyun.com/zh/apsaramq-for-kafka/cloud-message-queue-for-kafka/product-overview/instance-editions) <br>
- [Alibaba Cloud Kafka Usage Limits](https://help.aliyun.com/zh/apsaramq-for-kafka/cloud-message-queue-for-kafka/product-overview/limits) <br>
- [Alibaba Cloud Kafka v3 Elastic Strategy](https://help.aliyun.com/zh/apsaramq-for-kafka/cloud-message-queue-for-kafka/user-guide/elastic-strategy) <br>
- [Alibaba Cloud GetInstanceList API](https://help.aliyun.com/zh/apsaramq-for-kafka/cloud-message-queue-for-kafka/developer-reference/api-alikafka-2019-09-16-getinstancelist) <br>
- [Alibaba Cloud DescribeMetricList API](https://help.aliyun.com/zh/cms/cloudmonitor-1-0/developer-reference/api-cms-2019-01-01-describemetriclist) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown diagnostic report with inline Aliyun CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only assessment output; includes instance details, anomalous metrics, diagnostic conclusion, and upgrade recommendations.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
