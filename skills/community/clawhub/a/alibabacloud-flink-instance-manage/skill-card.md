## Description:

Manage Alibaba Cloud Flink VVP instances and namespaces through create/query operations only, including region, zone, namespace, and tag queries in Chinese or English while rejecting update/delete, Flink SQL/job, and unrelated cloud-service requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to create and query Alibaba Cloud Flink VVP instances and namespaces through a constrained wrapper script with explicit parameter validation, confirmation gates, and read-back verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate paid Alibaba Cloud Flink instance and namespace creation.

Mitigation: Require the agent to show the final command, region, resource size, billing impact, and --confirm flag before any create operation, then verify the result with read-back queries.

Risk: Broad cloud setup guidance can distract from the Flink-only operating scope.

Mitigation: Use only the documented Flink wrapper commands for create/query work and avoid unrelated ECS, plugin, or non-Flink examples.

Risk: Overbroad credentials could allow more cloud actions than the skill needs.

Mitigation: Use a RAM identity limited to the listed stream actions and rely on the default credential chain without exposing plaintext access keys.

Risk: Optional CLI installation or diagnostics can introduce dependency or supply-chain uncertainty.

Mitigation: Prefer a pinned and verified Aliyun CLI installation, or skip optional CLI setup when the Python wrapper and existing credentials are sufficient.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-flink-instance-manage)
- [References Index](references/README.md)
- [Quick Start](references/quick-start.md)
- [Core Execution Flow](references/core-execution-flow.md)
- [Command Templates](references/command-templates.md)
- [Parameter Validation Rules](references/parameter-validation.md)
- [Required Confirmation Model](references/required-confirmation-model.md)
- [Output Handling](references/output-handling.md)
- [RAM Policies for Flink Instance Operations](references/ram-policies.md)
- [Related APIs and Command Mapping](references/related-apis.md)
- [Alibaba Cloud Flink OpenAPI RAM actions](https://help.aliyun.com/zh/flink/realtime-flink/developer-reference/api-foasconsole-2021-10-28-ram)
- [Alibaba Cloud Flink OpenAPI overview](https://help.aliyun.com/zh/flink/realtime-flink/developer-reference/api-foasconsole-2021-10-28-overview)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Create operations require --confirm and read-back verification; command failures return JSON diagnostics and exit code 1.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
