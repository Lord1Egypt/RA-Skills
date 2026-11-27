## Description:

Diagnoses Alibaba Cloud ECS snapshot and backup issues across policy behavior, I/O impact, consistency groups, rollback readiness, and backup strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud support engineers and ECS administrators use this skill to diagnose snapshot and backup behavior, assess recovery readiness, and plan suitable backup approaches. It returns evidence-based guidance, with explicit consent for commands inside an instance and confirmation gates for state-changing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks this release suspicious based on reported undeclared cloud actions and overly broad or mismatched data access; scan coverage was incomplete.

Mitigation: Review before installation and consider avoiding installation until the undeclared snapshot creation and guest-command features, broad queries, and target-mismatch reporting are addressed. The verdict reports weaknesses and is not a conclusion of malicious intent.

Risk: Commands run inside an instance can expose customer system details, and state-changing operations can affect cloud resources.

Mitigation: Obtain consent for each in-instance command and explicit confirmation for each gated state-changing action.

## Reference(s):

- [Alibaba Cloud: Create a Snapshot](https://help.aliyun.com/zh/ecs/user-guide/create-a-snapshot)
- [Alibaba Cloud: Snapshot Overview](https://help.aliyun.com/zh/ecs/user-guide/snapshot-overview)
- [Alibaba Cloud: Automatic Snapshot Policy](https://help.aliyun.com/zh/ecs/user-guide/automatic-snapshot-policy)
- [Alibaba Cloud ECS File Backup FAQ](https://help.aliyun.com/document_detail/2979167.html)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, Markdown]

**Output Format:** [Markdown diagnostic report with command output and recommended checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-based findings; in-instance commands require specific consent, and gated state-changing actions require explicit confirmation.]

## Skill Version(s):

0.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
