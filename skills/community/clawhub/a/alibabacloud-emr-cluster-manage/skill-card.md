## Description: <br>
Manage the full lifecycle of Alibaba Cloud E-MapReduce (EMR) ECS clusters, including creation, scaling, renewal, status queries, and creation-failure diagnosis, while refusing cluster deletion or termination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and cloud operators use this skill to plan and manage Alibaba Cloud EMR on ECS clusters through aliyun CLI workflows for creation, inspection, scaling, renewal, and recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform cloud-changing Alibaba Cloud EMR operations with the active aliyun account. <br>
Mitigation: Use a dedicated least-privilege RAM role or short-lived STS token and review every write action for cost and production impact before confirmation. <br>
Risk: CLI installation and plugin update steps may introduce unreviewed code or tool changes. <br>
Mitigation: Preinstall and approve the Alibaba Cloud CLI and required plugins outside the skill workflow instead of relying on curl-to-bash or automatic plugin updates. <br>
Risk: Database credentials or other sensitive values may be exposed if placed in command lines or chat transcripts. <br>
Mitigation: Avoid sending real passwords through chat or shell history; use secure credential handling and redact sensitive values in shared outputs. <br>
Risk: Incorrect cluster creation, scaling, or renewal choices can affect production availability or spend. <br>
Mitigation: Confirm the account, region, target cluster, configuration, and intended write operation before running cloud-changing commands. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/sdk-team/alibabacloud-emr-cluster-manage) <br>
- [API Parameter Quick Reference](references/api-reference.md) <br>
- [Cluster Full Lifecycle Guide](references/cluster-lifecycle.md) <br>
- [Quick Start: Create Your First EMR Cluster](references/getting-started.md) <br>
- [Scaling: Manual Scaling and Auto Scaling Policy](references/scaling.md) <br>
- [Daily Operations: Inspection, Renewal, Troubleshooting](references/operations.md) <br>
- [RAM Permission Description](references/ram-policies.md) <br>
- [Error Recovery Detailed Guide](references/error-recovery.md) <br>
- [User-Agent Configuration for Non-CLI Invocation Methods](references/user-agent.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline aliyun CLI commands and JSON command arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Alibaba Cloud CLI profile and explicit confirmation before cloud-changing actions.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
