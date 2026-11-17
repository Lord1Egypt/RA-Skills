## Description:

Byted EMR Skills helps agents manage Volcengine E-MapReduce resources across EMR on ECS, EMR on VKE, EMR Serverless queues, compute groups, jobs, and EMR Agent diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robinliew](https://clawhub.ai/user/robinliew)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and EMR operators use this skill to query, operate, and troubleshoot Volcengine EMR resources. It supports Serverless job submission, cluster and service administration, user and permission management, monitoring, audit lookups, and EMR Agent diagnostic or knowledge workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful Volcengine credentials and can perform sensitive EMR management operations.

Mitigation: Run it only in an isolated environment with least-privilege, short-lived Volcengine credentials scoped to the intended EMR resources.

Risk: Custom endpoints could direct signed requests to an untrusted destination.

Mitigation: Use only approved Volcengine endpoints and avoid passing user-supplied custom endpoint values.

Risk: Password-changing and credential-bearing flows may expose secrets through logs or command history.

Mitigation: Avoid password-changing flows unless logging is disabled or redacted, and do not store AK/SK, passwords, or request bodies in shared logs.

Risk: The Serverless SDK is bundled or downloaded as a wheel before use.

Mitigation: Verify the wheel through a trusted channel before installation and install it in a disposable or isolated Python environment.

## Reference(s):

- [Skill source](artifact/SKILL.md)
- [EMR Agent interaction guide](artifact/references/emr_agent/emr_agent_guide.md)
- [EMR on ECS application guide](artifact/references/emr_on_ecs/application/emr_on_ecs_application_guide.md)
- [EMR on ECS application configuration guide](artifact/references/emr_on_ecs/application_config/emr_on_ecs_application_config_guide.md)
- [EMR on ECS cluster guide](artifact/references/emr_on_ecs/cluster/emr_on_ecs_cluster_guide.md)
- [EMR on ECS node group guide](artifact/references/emr_on_ecs/cluster_group/emr_on_ecs_cluster_group_guide.md)
- [EMR on ECS operation audit guide](artifact/references/emr_on_ecs/operation/emr_on_ecs_operation_guide.md)
- [EMR on ECS user guide](artifact/references/emr_on_ecs/user/emr_on_ecs_user_guide.md)
- [EMR on ECS user group guide](artifact/references/emr_on_ecs/user_group/emr_on_ecs_user_group_guide.md)
- [EMR on VKE guide](artifact/references/emr_on_vke/emr_on_vke_guide.md)
- [EMR Serverless compute guide](artifact/references/emr_serverless/compute/emr_serverless_compute_guide.md)
- [EMR Serverless job guide](artifact/references/emr_serverless/job/emr_serverless_job_guide.md)
- [EMR Serverless job instance guide](artifact/references/emr_serverless/job_instance/emr_serverless_job_instance_guide.md)
- [EMR Serverless operation audit guide](artifact/references/emr_serverless/operation_audit/emr_serverless_operation_audit_guide.md)
- [EMR Serverless privilege guide](artifact/references/emr_serverless/privilege/emr_serverless_privilege_guide.md)
- [EMR Serverless queue guide](artifact/references/emr_serverless/queue/emr_serverless_queue_guide.md)
- [Volcengine EMR Serverless product documentation](https://www.volcengine.com/docs/6491/1164733)
- [Volcengine EMR Serverless API reference](https://www.volcengine.com/docs/6491/1164734)
- [Volcengine EMR Serverless queue management best practices](https://www.volcengine.com/docs/6491/1164735)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, Python snippets, and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Volcengine API actions, command invocations, operational summaries, and diagnostic guidance.]

## Skill Version(s):

1.0.5 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
