## Description: <br>
Operate Alibaba Cloud AgentLoop Dataset resources with aliyun CLI and the AgentLoop API version 2026-05-20. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Alibaba Cloud AgentLoop Dataset resources, update schemas, append structured rows, run read-only SQL or semantic searches, and verify Dataset operations through the Aliyun CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alibaba Cloud RAM does not enforce read-only SQL at the ExecuteQuery permission level. <br>
Mitigation: Scope the Aliyun identity to the intended AgentSpace and Dataset resources, and use ExecuteQuery only for confirmed read-only SELECT or SearchExpr patterns. <br>
Risk: Dataset commands can mutate cloud resources or append data when parameters are incorrect. <br>
Mitigation: Confirm region, AgentSpace, Dataset name, schema, rows, and idempotency token before execution, and use dry runs for complex JSON, writes, updates, or queries. <br>
Risk: Cloud credential material could be exposed during troubleshooting. <br>
Mitigation: Use existing Aliyun CLI profiles or environment credentials, check configuration without printing secrets, and report request IDs without exposing signing material. <br>


## Reference(s): <br>
- [Dataset Management](artifact/references/dataset-management.md) <br>
- [Dataset Data Operations](artifact/references/data-operations.md) <br>
- [Dataset Query Syntax](artifact/references/query-syntax.md) <br>
- [RAM Policies](artifact/references/ram-policies.md) <br>
- [Related CLI Commands](artifact/references/related-commands.md) <br>
- [Verification Method](artifact/references/verification-method.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline bash commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include parameter confirmations, dry-run guidance, request IDs, verification evidence, and credential-handling cautions.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
