## Description: <br>
Helps agents manage Alibaba Cloud ECS disk snapshot lifecycle tasks, including snapshot creation, inspection, automatic snapshot policies, cost estimation, lifecycle planning, and guidance-only handling for deletion and rollback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operators, developers, and support engineers use this skill to plan, create, audit, and cost-manage Alibaba Cloud ECS disk snapshots. It supports non-destructive cloud operations directly while keeping deletion, rollback, and policy unbinding as guidance-only workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide creation of snapshots and auto-snapshot policies that may incur cloud charges. <br>
Mitigation: Verify region, retention settings, pricing assumptions, and cleanup plans before creating resources; use the bundled cost references and calculators for estimates. <br>
Risk: Network troubleshooting guidance includes proxy-clearing retries that may bypass configured proxy controls in a high-impact cloud-operations context. <br>
Mitigation: Do not use proxy-clearing retries in environments where proxy or egress controls are mandatory; follow local network policy instead. <br>
Risk: Deletion, rollback, and policy unbinding are destructive or high-impact workflows. <br>
Mitigation: Keep those operations guidance-only, perform read-only checks first, use official Alibaba Cloud channels, and create fresh backups before rollback. <br>


## Reference(s): <br>
- [ECS Snapshot API Reference](references/api-reference.md) <br>
- [Snapshot Lifecycle Best Practices](references/best-practices.md) <br>
- [Alibaba Cloud CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Snapshot Cost Formulas and Optimization](references/cost-formulas.md) <br>
- [Snapshot Error Code Handbook](references/error-code-handbook.md) <br>
- [RAM Permission Policies for Snapshot Management](references/ram-policies.md) <br>
- [Snapshot Workflow Decision Tree](references/workflow-decision-tree.md) <br>
- [Alibaba Cloud ECS CreateSnapshot API documentation](https://www.alibabacloud.com/help/zh/ecs/developer-reference/api-ecs-2014-05-26-createsnapshot) <br>
- [Alibaba Cloud CLI documentation](https://www.alibabacloud.com/help/en/cli) <br>
- [Alibaba Cloud credential configuration documentation](https://www.alibabacloud.com/help/en/cli/configure-credentials) <br>
- [Alibaba Cloud ECS pricing page](https://www.aliyun.com/price/detail) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, tables, and JSON where needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include read-only API results, cost estimates, lifecycle recommendations, and guidance-only treatment for destructive operations.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
