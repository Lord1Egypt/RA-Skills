## Description:

Manage the full lifecycle of Alibaba Cloud E-MapReduce (EMR) ECS clusters, including creation, scaling, renewal, status queries, and creation-failure diagnosis, while refusing cluster deletion, release, or termination requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and cloud operations teams use this skill to plan, create, inspect, scale, renew, and troubleshoot Alibaba Cloud EMR on ECS clusters through the aliyun CLI. It is intended for EMR cluster lifecycle management and explicitly routes cluster deletion or termination outside the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation and plugin-update guidance can execute unreviewed code.

Mitigation: Replace curl-to-bash and automatic plugin update steps with a verified Alibaba Cloud CLI installation and update path before use.

Risk: The skill uses Alibaba Cloud credentials and may handle RDS connection details during cluster creation.

Mitigation: Use configured CLI profiles or STS credentials, avoid plaintext secrets in command lines or chat, and grant only the RAM actions required for the workflow.

Risk: Cluster creation, scaling, renewal, and node removal can change cloud resources and cost.

Mitigation: Require explicit user confirmations, validate target resource IDs, use idempotency tokens where supported, and review node-removal safety gates before execution.

Risk: Public SSH or public network exposure can increase operational risk.

Mitigation: Disable public access for production clusters unless explicitly required and tightly restricted.

## Reference(s):

- [API Parameter Quick Reference](artifact/references/api-reference.md)
- [Cluster Full Lifecycle: Planning, Creation, Management, Clone](artifact/references/cluster-lifecycle.md)
- [Error Recovery Detailed Guide](artifact/references/error-recovery.md)
- [Quick Start: Create Your First EMR Cluster from Scratch](artifact/references/getting-started.md)
- [Daily Operations: Inspection, Renewal, Troubleshooting](artifact/references/operations.md)
- [RAM Permission Description](artifact/references/ram-policies.md)
- [Scaling: Manual Scaling and Auto Scaling Policy](artifact/references/scaling.md)
- [User-Agent Configuration for Non-CLI Invocation Methods](artifact/references/user-agent.md)
- [Alibaba Cloud EMR Console](https://emr.console.aliyun.com/)
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-emr-cluster-manage)
- [ClawHub Publisher Profile](https://clawhub.ai/user/sdk-team)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline aliyun CLI commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API call plans, confirmation prompts, safety refusals, and troubleshooting guidance.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
